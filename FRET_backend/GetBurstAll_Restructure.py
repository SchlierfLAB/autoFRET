import os.path

from FRET_backend.read_ht3_vect import read_ht3_raw
from FRET_backend.Read_PTU_Obj import Read_PTU
from FRET_backend.lee_filter import leeFilter
from FRET_backend.burst_locator import burstLoc

from FRET_backend.LifeMLE import LifeMLE

import numpy as np
import pandas as pd
from numpy import c_
import scipy.io as sio
from pathlib import Path
from joblib import Parallel, delayed, parallel
from OnTheFlyBurst_Scripts.get_burst_input import get_input

import contextlib


import time
from numba import jit, njit
import collections

# Todo: Solve it dont ignore it --> This is explicitly for debugging
import warnings
warnings.filterwarnings("ignore")

from tqdm import tqdm




def get_files(folder):
    ht3_locations = dict()
    try:
        for path, subdirs, files in os.walk(folder):
            for name in files:
                if name.endswith('.ht3') or name.endswith('.ptu'):
                    try:
                        ht3_locations[name[0:3]] = ht3_locations[name[0:3]] + [os.path.join(path, name)]
                    except KeyError:
                        ht3_locations[name[0:3]] = [os.path.join(path, name)]

    except FileNotFoundError:
        return

    def sort_fun_key(string):
        string = string.split('/')[-1]
        if len(string) == 10:
            return string[0:6]
        else:
            return string[0:4] + '0' + string[4]

    # sort the folders
    for keys in ht3_locations.keys():
        ht3_locations[keys] = sorted(ht3_locations[keys], key=sort_fun_key)

    ht3_locations = collections.OrderedDict(sorted(ht3_locations.items()))

    return ht3_locations

@njit
def KDE(T1, arrT2, tau):
    expFrac = (np.abs(arrT2-T1) / tau)

    return np.sum(np.exp(-expFrac[expFrac<=5]))

@njit
def nbKDE(T1, arrT1, tau):
    expFrac = (np.abs(arrT1-T1) / tau)

    return ((1+2/np.array(len(arrT1))) * (np.sum(np.exp(-expFrac[expFrac<=5]))-1))

@njit
def FRET_2CDE(tA, tD, tau):

    KDE_DiA = np.zeros(len(tD))
    nbKDE_DiD = np.zeros(len(tD))

    for i in range(len(tD)):

        KDE_DiA[i] = KDE(tD[i],tA, tau)
        nbKDE_DiD[i] = nbKDE(tD[i], tD, tau)

    fracNAN1 = KDE_DiA / (KDE_DiA+nbKDE_DiD)
    frac1 = fracNAN1[~np.isnan(fracNAN1)]

    if len(frac1) != 0:
        ED = (1/np.array(len(frac1))) * np.sum(frac1)
    else:
        ED = 0


    KDE_AiD = np.zeros(len(tA))
    nbKDE_AiA = np.zeros(len(tA))

    for i in range(len(tA)):
        KDE_AiD[i] = KDE(tA[i], tD, tau)
        nbKDE_AiA[i] = nbKDE(tA[i], tA, tau)

    fracNAN2 = KDE_AiD / (KDE_AiD+nbKDE_AiA)
    frac2 = fracNAN2[~np.isnan(fracNAN2)]

    if len(frac2) != 0:
        OneMinusEA = (1/np.array(len(frac2))) * np.sum(frac2)
    else:
        OneMinusEA = 0


    value = 110-100*(ED + OneMinusEA)

    if (np.isnan(value)) | (value < 0):
        value = 0
    return value

@njit
def Alex_2CDE(tAex, tDex, tau):

    KDE_DexiAlex = np.zeros(len(tDex))
    KDE_DexiDex = np.zeros(len(tDex))

    for i in range(len(tDex)):
        KDE_DexiAlex[i] = KDE(tDex[i], tAex, tau)
        KDE_DexiDex[i] = KDE(tDex[i], tDex, tau)

    if len(tAex) == 0:
        BR_Dex = 0
    else:
        BR_Dex = (1/len(tAex)) * np.sum(KDE_DexiAlex/KDE_DexiDex)

    KDE_AexiDex = np.zeros(len(tAex))
    KDE_AexiAex = np.zeros(len(tAex))

    for i in range(len(tAex)):

        KDE_AexiDex[i] = KDE(tAex[i], tDex, tau)
        KDE_AexiAex[i] = KDE(tAex[i], tAex, tau)

    if len(tDex) == 0:
        BR_Aex = 0
    else:
        BR_Aex = (1/len(tDex)) * np.sum(KDE_AexiDex/KDE_AexiAex)

    return (100-50*(BR_Dex+BR_Aex))



def histc(Inp, bin):
    """Clone of MATLAB's histc function. From: https://stackoverflow.com/a/56062759

    Args:
        Inp (ndarray): Input array/matrix
        bin (ndarray): Array of bin values

    Returns:
        Array of ndarray: Counts and mapping to bin values
    """
    bin_map = np.digitize(Inp, bin)
    count = np.zeros(bin.shape)
    for i in bin_map:
        count[i-1] += 1
    return [count, bin_map]


import numpy as np
import pickle
from pathlib import Path


def getBurstAll(filename, pathname, suffix, lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT,
                newIRF_G_II, newIRF_G_T, meanIRFG_II, meanIRFG_T, newIRF_R_II, newIRF_R_T,
                meanIRFR_II, meanIRFR_T, roiMLE_G, roiMLE_R, dtBin, setLeeFilter, boolFLA, boolTotal,
                minGR, minR0, boolPostA, checkInner, tauFRET, tauALEX, method='intensity_based'):
    """
    Process photon burst data using either time-based or intensity-based thresholding.

    Parameters:
        method: str
            - 'time_based': Use inter-photon time filtering
            - 'intensity_based': Use intensity thresholding
    """

    # Load and preprocess photon data
    Photons, Photons_Raw, PhotonsSGR0 = load_photon_data(pathname, filename, roiRG, roiR0, return_raw=True)

    # Define binning range for intensity-based method
    edges = np.arange(1, 4097, 1)  # 1 ms binning

    # Detect bursts with the selected method
    if method == 'time_based':
        bStartLong, bLengthLong, bStartLongN, bLengthLongN = detect_bursts_time_based(
            PhotonsSGR0, Photons_Raw, threIT, threIT2, minPhs, checkInner, boolTotal, setLeeFilter, edges
        )

    elif method == 'intensity_based':
        BurstBackIDXs = detect_bursts_intensity_based(
            Photons, minPhs, minGR, minR0, edges
        )
        # Todo: Get flags from GUI to decide which bursts and background IDX to take (all vs. donor vs. acceptor)
        #  for testing using only idx from all and naming convention from time based method
        bStartLong, bLengthLong = BurstBackIDXs['TotalBurstIDX']
        bStartLongN, bLengthLongN = BurstBackIDXs['TotalBackgroundIDX']

    else:
        raise ValueError("Invalid method. Choose 'time_based' or 'intensity_based'.")



    # Extract bursts and background
    Bursts = process_bursts(PhotonsSGR0, Photons_Raw, bStartLong, bLengthLong,  edges, pathname)
    Background = compute_background(pathname, PhotonsSGR0, bStartLongN, bLengthLongN, roiRG, roiR0, edges)


    # If no valid bursts are found, return empty
    if len(Bursts['Bursts']) == 0:
        print(f'The file {filename} has too much background and will not be analyzed.')
        return []

    # seperate photons
    seperated_photons = seperate_photons(PhotonsSGR0, Bursts['Bursts'], bLengthLong, bStartLong, roiRG, roiR0, tauFRET, tauALEX)

    # Compute burst statistics (FRET, ALEX, lifetimes) and add everything to final output matrix for saving
    output_mat = compute_final_statistic(Bursts['Bursts'], seperated_photons, boolTotal, threAveT, minGR, minR0, roiR0, roiMLE_G, roiMLE_R,
                            newIRF_G_II, meanIRFG_II, newIRF_G_T, meanIRFG_T, newIRF_R_II, meanIRFR_II, newIRF_R_T,
                            meanIRFR_T, dtBin, boolFLA, Background, edges, lastBN)


    # Save burst data
    save_burst_data(pathname, suffix, output_mat, boolPostA)

    return output_mat


# ---- Sub-functions ---- #

def load_photon_data(pathname, filename, roiRG, roiR0, return_raw=False):
    """ Load and filter raw photon data from a PTU file. """
    file_instance = Read_PTU(pathname + '/' + filename)
    Photons_Raw = file_instance.RawData

    # Filter photons by valid regions
    Photons = Photons_Raw[(Photons_Raw[:, 0] != 15) & (
            (Photons_Raw[:, 1] >= roiRG[0]) & (Photons_Raw[:, 1] <= roiRG[1]) |
            (Photons_Raw[:, 1] >= roiR0[0]) & (Photons_Raw[:, 1] <= roiR0[1]))]

    # keep just real data and seperate them in channels
    PhotonsSGR0 = Photons[(Photons[:, 0] == 1) | (Photons[:, 0] == 2) | (Photons[:, 0] == 3) | (Photons[:, 0] == 4),
                  0:3]

    if return_raw:
        return Photons, Photons_Raw, PhotonsSGR0
    else:
        return Photons, PhotonsSGR0


def detect_bursts_time_based(PhotonsSGR0, Photons_Raw, threIT, threIT2, minPhs, checkInner, boolTotal, setLeeFilter, edges):
    """Burst detection based on inter-photon time filtering."""

    # Extract inter-photon times and apply Lee Filter
    interPhT = PhotonsSGR0[1:, 2] - PhotonsSGR0[:-1, 2]
    interLee = leeFilter(interPhT, setLeeFilter)

    # Identify burst-related events based on inter-photon times
    indexSig = np.argwhere((0.4 < interLee) & (interLee < (threIT * 1e6)))
    indexSigN = np.argwhere(interLee > (threIT2 * 1e6))

    if indexSig.size == 0 or indexSigN.size == 0:
        # Print relevant file and return empty
        print(f'The Current file has to much background and will not be analyzed')
        return []

    # Detect bursts and background
    bStart, bLength = burstLoc(indexSig, 1)
    bStartN, bLengthN = burstLoc(indexSigN, 1)

    # Filter bursts
    if boolTotal == 1:
        if checkInner == 1:
            bStartLong = bStart[bLength >= minPhs] + 30
            bLengthLong = bLength[bLength >= minPhs] - 60
        else:
            bStartLong = bStart[bLength >= minPhs]
            bLengthLong = bLength[bLength >= minPhs]
    else:
        if checkInner == 1:
            bStartLong = bStart + 30
            bLengthLong = bLength - 60
        else:
            bStartLong = bStart
            bLengthLong = bLength

    # Background burst filtering
    bStartLongN = bStartN[bLengthN >= 160] + 30
    bLengthLongN = bLengthN[bLengthN >= 160] - 60

    return bStartLong, bLengthLong, bStartLongN, bLengthLongN

def detect_bursts_intensity_based(Photons, minPhs, minGR, minR0, edges):
    """Burst detection using intensity thresholding, returning burst indices and background."""

    # Keep only real data (channels 1–4)
    PhotonsSGR0 = Photons[np.isin(Photons[:, 0], [1, 2, 3, 4]), 0:3]

    # Separate Donor (SGR) and Acceptor (R0) Channels
    subarray_1_3 = PhotonsSGR0[np.isin(PhotonsSGR0[:, 0], [1, 3])]  # Donor (SGR)
    subarray_2_4 = PhotonsSGR0[np.isin(PhotonsSGR0[:, 0], [2, 4])]  # Acceptor (R0)

    # ---- Intensity Binning ---- #

    # Bin total intensity (all channels)
    BinsSGR0 = histc(PhotonsSGR0[:, 1], edges)
    valid_bins = np.where(BinsSGR0[0] >= minPhs)[0]

    # Bin donor (1 & 3) and acceptor (2 & 4) separately
    Bins_1_3 = histc(subarray_1_3[:, 1], edges)
    valid_bins_1_3 = np.where(Bins_1_3[0] >= minGR)[0]

    Bins_2_4 = histc(subarray_2_4[:, 1], edges)
    valid_bins_2_4 = np.where(Bins_2_4[0] >= minR0)[0]

    # ---- Burst Detection ---- #

    # Find burst indices (total, donor, acceptor)
    bStart, bLength = burstLoc(valid_bins, 1)
    bStart_1_3, bLength_1_3 = burstLoc(valid_bins_1_3, 1)
    bStart_2_4, bLength_2_4 = burstLoc(valid_bins_2_4, 1)

    # ---- Background Estimation ---- #

    # Identify background regions (bins below threshold)
    background_bins = np.where(BinsSGR0[0] < minPhs)[0]
    bStartN, bLengthN = burstLoc(background_bins, 1)

    background_bins_1_3 = np.where(Bins_1_3[0] < minGR)[0]
    bStartN_1_3, bLengthN_1_3 = burstLoc(background_bins_1_3, 1)

    background_bins_2_4 = np.where(Bins_2_4[0] < minR0)[0]
    bStartN_2_4, bLengthN_2_4 = burstLoc(background_bins_2_4, 1)

    return {'TotalBurstIDX': [bStart, bLength],
            'DonorBurstIDX': [bStart_1_3, bLength_1_3],
            'AcceptorBurstIDX': [bStart_2_4, bLength_2_4],
            'TotalBackgroundIDX': [bStartN, bLengthN],
            'DonorBackgroundIDX': [bStartN_1_3, bLengthN_1_3],
            'AcceptorBackgroundIDX': [bStartN_2_4, bLengthN_2_4]
        }

def process_bursts(PhotonsSGR0, Photons_Raw, bStartLong, bLengthLong,  edges, pathname):
    """Process bursts and compute histograms, background rates, and save results."""

    if bStartLong is None or bLengthLong is None:
        return None

    # ---- Extract Bursts Data ---- #
    Bursts = np.zeros([int(np.sum(bLengthLong)), 4])
    lInd = 0

    for i in range(len(bStartLong)):
        Bursts[lInd:lInd + int(bLengthLong[i]), :] = np.c_[
            np.ones(int(bLengthLong[i])) * (i + 1),
            PhotonsSGR0[int(bStartLong[i]) + 1: int(bStartLong[i]) + int(bLengthLong[i]) + 1, 0:4]
        ]
        lInd += int(bLengthLong[i])

    # ---- Compute Photon Histograms ---- #

    # channel histogram
    strAllHIST = pathname + '/allHIST.npy'
    dataAll = np.load(strAllHIST, allow_pickle=True)

    for i in range(len(bStartLong)):
        hAll, _ = histc(
            Photons_Raw[
                (Photons_Raw[:, 0] != 15) & ((Photons_Raw[:, 0] == 1) | (Photons_Raw[:, 0] == 3)) &
                ((Photons_Raw[:, 2] >= PhotonsSGR0[bStartLong[i], 2]) &
                 (Photons_Raw[:, 2] <= PhotonsSGR0[bStartLong[i] + int(bLengthLong[i]), 2])),
                1
            ],
            edges
        )

        dataAll.item().get('photonHIST')[:, 0] += hAll

        hAll, _ = histc(
            Photons_Raw[
                (Photons_Raw[:, 0] != 15) & ((Photons_Raw[:, 0] == 2) | (Photons_Raw[:, 0] == 4)) &
                ((Photons_Raw[:, 2] >= PhotonsSGR0[bStartLong[i], 2]) &
                 (Photons_Raw[:, 2] <= PhotonsSGR0[bStartLong[i] + int(bLengthLong[i]), 2])),
                1
            ],
            edges
        )
        dataAll.item().get('photonHIST')[:,1] += hAll

    strAllHIST = pathname + '/allHIST.npy'

    # channel background histogram and background counts
    np.save(strAllHIST, dataAll)


    return {
        "Bursts": Bursts,
        "Histograms": dataAll
    }

def compute_background(pathname, PhotonsSGR0, bStartLongN, bLengthLongN, roiRG, roiR0, edges):
    # ---- Compute Background Data ---- #
    BackNGII, BackNGT, BackNRII, BackNRT, BackNR0II, BackNR0T, BackT = 0, 0, 0, 0, 0, 0, 0

    strHIST = pathname + '/backHIST.npy'
    background_data = np.load(strHIST, allow_pickle=True)

    for i in range(len(bStartLongN)):
        GapPhotons = PhotonsSGR0[bStartLongN[i] + 1: bStartLongN[i] + int(bLengthLongN[i]) + 1, 0:3]
        BackT += GapPhotons[-1, 2] - GapPhotons[0, 2]

        GapPhGII = GapPhotons[(GapPhotons[:, 0] == 2)
                              & (GapPhotons[:, 1] >= roiRG[0])
                              & (GapPhotons[:, 1] <= roiRG[1])]

        GapPhGT = GapPhotons[(GapPhotons[:, 0] == 4)
                             & (GapPhotons[:, 1] >= roiRG[0])
                             & (GapPhotons[:, 1] <= roiRG[1])]

        GapPhRII = GapPhotons[(GapPhotons[:, 0] == 1)
                              & (GapPhotons[:, 1] >= roiRG[0])
                              & (GapPhotons[:, 1] <= roiRG[1])]

        GapPhRT = GapPhotons[(GapPhotons[:, 0] == 3)
                             & (GapPhotons[:, 1] >= roiRG[0])
                             & (GapPhotons[:, 1] <= roiRG[1])]

        GapPhR0II = GapPhotons[(GapPhotons[:, 0] == 1)
                               & (GapPhotons[:, 1] >= roiR0[0])
                               & (GapPhotons[:, 1] <= roiR0[1])]

        GapPhR0T = GapPhotons[(GapPhotons[:, 0] == 3)
                              & (GapPhotons[:, 1] >= roiR0[0])
                              & (GapPhotons[:, 1] <= roiR0[1])]

        BackNGII += len(GapPhGII)
        BackNGT += len(GapPhGT)
        BackNRII += len(GapPhRII)
        BackNRT += len(GapPhRT)
        BackNR0II += len(GapPhR0II)
        BackNR0T += len(GapPhR0T)

        hGapPhGII, _ = histc(GapPhotons[(GapPhotons[:, 0] == 2)
                                        & (GapPhotons[:, 1] >= roiRG[0])
                                        & (GapPhotons[:, 1] <= roiRG[1]), 1], edges)

        hGapPhGT, _ = histc(GapPhotons[(GapPhotons[:, 0] == 4)
                                       & (GapPhotons[:, 1] >= roiRG[0])
                                       & (GapPhotons[:, 1] <= roiRG[1]), 1], edges)

        background_data.item().get('backHIST')[:,0] += hGapPhGII
        background_data.item().get('backHIST')[:,1] += hGapPhGT
        background_data.item().get('time')[0] += BackT / 1e9

    np.save(strHIST, background_data)

    if BackT:
        BGII = BackNGII / BackT * 1e9
        BGT = BackNGT / BackT * 1e9
        BRII = BackNRII / BackT * 1e9
        BRT = BackNRT / BackT * 1e9
        BR0II = BackNR0II / BackT * 1e9
        BR0T = BackNR0T / BackT * 1e9
    else:
        BGII = BGT = BRII = BRT = BR0II = BR0T = 0

    return {"Background Rates":
                {"BGII": BGII, "BGT": BGT, "BRII": BRII, "BRT": BRT, "BR0II": BR0II, "BR0T": BR0T},
            "Background Histograms": background_data
        }

def seperate_photons(PhotonsSGR0, Bursts, bLengthLong, bStartLong, roiRG, roiR0, tauFRET, tauALEX):

    # compute interphoton time
    interPhT = PhotonsSGR0[1:, 2] - PhotonsSGR0[0:-1, 2]

    # prefill = np.zeros(len(bLengthLong))
    arrAlex_2CDE_ = np.zeros(len(bLengthLong))
    arrFRET_2CDE_ = np.zeros(len(bLengthLong))
    NG_ = np.zeros(len(bLengthLong))
    NGII_ = np.zeros(len(bLengthLong))
    NGT_ = np.zeros(len(bLengthLong))
    NR_ = np.zeros(len(bLengthLong))
    NRII_ = np.zeros(len(bLengthLong))
    NRT_ = np.zeros(len(bLengthLong))
    NR0_ = np.zeros(len(bLengthLong))
    NR0II_ = np.zeros(len(bLengthLong))
    NR0T_ = np.zeros(len(bLengthLong))
    TBurst_ = np.zeros(len(bLengthLong))
    TGR_ = np.zeros(len(bLengthLong))  # averaged macrotime of total 530nm excited burst photons
    TR0_ = np.zeros(len(bLengthLong))  # averaged macrotime of red 640nm exited burst photons


    for i in range(len(bStartLong)):
        N_ = Bursts[Bursts[:, 0] == (i + 1), 1:4]

        NGII_[i] = np.count_nonzero(N_ == 2)

        NGT_[i] = np.count_nonzero(N_ == 4)

        NG_[i] = NGII_[i] + NGT_[i]

        NRII_[i] = len(N_[(N_[:, 0] == 1)
                          & (N_[:, 1] >= roiRG[0])
                          & (N_[:, 1] <= roiRG[1]), 0])

        NRT_[i] = len(N_[(N_[:, 0] == 3)
                         & (N_[:, 1] >= roiRG[0])
                         & (N_[:, 1] <= roiRG[1]), 0])

        NR_[i] = NRII_[i] + NRT_[i]

        NR0II_[i] = len(N_[(N_[:, 0] == 1)
                           & (N_[:, 1] >= roiR0[0])
                           & (N_[:, 1] <= roiR0[1]), 0])

        NR0T_[i] = len(N_[(N_[:, 0] == 3)
                          & (N_[:, 1] >= roiR0[0])
                          & (N_[:, 1] <= roiR0[1]), 0])

        NR0_[i] = NR0II_[i] + NR0T_[i]

        TBurst_[i] = np.sum(interPhT[bStartLong[i]:bStartLong[i] + int(bLengthLong[i]) - 1] * 1e-9)

        phBurst = PhotonsSGR0[bStartLong[i] + 1:bStartLong[i] + int(bLengthLong[i]) + 1, 0:3]

        macroGR = phBurst[(phBurst[:, 0] == 2)
                          | (phBurst[:, 0] == 4)
                          | (((phBurst[:, 0] == 1) | (phBurst[:, 0] == 3)) & (phBurst[:, 1] >= roiRG[0]) & (
                    phBurst[:, 1] <= roiRG[1])), 2]

        macroR0 = phBurst[((phBurst[:, 0] == 1) | (phBurst[:, 0] == 3))
                          & (phBurst[:, 1] >= roiR0[0])
                          & (phBurst[:, 1] <= roiR0[1]), 2]

        macroR = phBurst[((phBurst[:, 0] == 1) | (phBurst[:, 0] == 3))
                         & (phBurst[:, 1] >= roiRG[0])
                         & (phBurst[:, 1] <= roiRG[1]), 2]

        macroG = phBurst[(phBurst[:, 0] == 2) | (phBurst[:, 0] == 4), 2]

        TGR_[i] = np.sum(macroGR) / len(macroGR) * 1e-6
        TR0_[i] = np.sum(macroR0) / len(macroR0) * 1e-6

        # print((np.sum(macroGR) / len(macroGR) * 1e-6)-(np.sum(macroR0) / len(macroR0) * 1e-6))

        arrFRET_2CDE_[i] = FRET_2CDE(macroR * 1e-6, macroG * 1e-6, tauFRET/1000)
        arrAlex_2CDE_[i] = Alex_2CDE(macroR0 * 1e-6, macroGR * 1e-6, tauALEX/1000)

    seperated_photons = {'arrAlex_2CDE':arrAlex_2CDE_, 'arrFRET_2CDE':arrFRET_2CDE_, 'NG':NG_, 'NGII':NGII_,
                        'NGT':NGT_, 'NR':NR_, 'NRII':NRII_, 'NRT':NRT_, 'NR0':NR0_, 'NR0II':NR0II_, 'NR0T':NR0T_,
                        'TBurst':TBurst_, 'TGR':TGR_, 'TR0':TR0_}

    return seperated_photons

def compute_final_statistic(Bursts, seperate_photons, boolTotal, threAveT, minGR, minR0, roiR0, roiMLE_G, roiMLE_R,
                            newIRF_G_II, meanIRFG_II, newIRF_G_T, meanIRFG_T, newIRF_R_II, meanIRFR_II, newIRF_R_T,
                            meanIRFR_T, dtBin, boolFLA, Background, edges, lastBN):

    dTGR_TR0_ = seperate_photons['TGR'] - seperate_photons['TR0']
    dTGR_TR0_[np.isnan(seperate_photons['TR0'])] = 9.9

    if boolTotal == 1:
        accBIndex = np.argwhere(np.abs(dTGR_TR0_) < threAveT)
    else:
        accBIndex = np.argwhere((np.abs(dTGR_TR0_) < threAveT) & ((seperate_photons['NG'] + seperate_photons['NR'])
                                                                  >= minGR) & (seperate_photons['NR0'] >= minR0))

    dtGR_TR0 = dTGR_TR0_[accBIndex]

    NG = seperate_photons['NG'][accBIndex]
    NGII = seperate_photons['NGII'][accBIndex]
    NGT = seperate_photons['NGT'][accBIndex]
    NR = seperate_photons['NR'][accBIndex]
    NRII = seperate_photons['NRII'][accBIndex]
    NRT = seperate_photons['NRT'][accBIndex]
    NR0 = seperate_photons['NR0'][accBIndex]
    NR0II = seperate_photons['NR0II'][accBIndex]
    NR0T = seperate_photons['NR0T'][accBIndex]
    TBurst = seperate_photons['TBurst'][accBIndex]
    TGR = seperate_photons['TGR'][accBIndex]
    arrFRET_2CDE = seperate_photons['arrFRET_2CDE'][accBIndex]
    arrAlex_2CDE = seperate_photons['arrAlex_2CDE'][accBIndex]

    # Taus parallel II and perpendicular T
    tauArrD_II = np.zeros(len(accBIndex))
    tauArrD_T = np.zeros(len(accBIndex))
    tauArrA_II = np.zeros(len(accBIndex))
    tauArrA_T = np.zeros(len(accBIndex))


    accBursts = np.zeros([np.sum(np.isin(Bursts[:, 0], accBIndex + 1)), 4])
    actIndex = 0

    for i in range(len(accBIndex)):

        sglBData = Bursts[Bursts[:, 0] == (accBIndex[i] + 1), 1:4]
        numB = len(sglBData)

        accBursts[actIndex:(actIndex + numB), :] = np.c_[
            np.ones(numB) * (i + 1 + lastBN), Bursts[Bursts[:, 0] == (accBIndex[i] + 1), 1:4]]

        actIndex += numB

        accMicroGII = Bursts[(Bursts[:, 0] == accBIndex[i] + 1)
                             & (Bursts[:, 1] == 2), 2]
        accMicroGT = Bursts[(Bursts[:, 0] == accBIndex[i] + 1)
                            & (Bursts[:, 1] == 4), 2]
        accMicroRII = Bursts[(Bursts[:, 0] == accBIndex[i] + 1)
                             & ((Bursts[:, 1] == 1)
                                & (Bursts[:, 2] >= roiR0[0])
                                & (Bursts[:, 2] <= roiR0[1])), 2]
        accMicroRT = Bursts[(Bursts[:, 0] == accBIndex[i] + 1)
                            & ((Bursts[:, 1] == 3)
                               & (Bursts[:, 2] >= roiR0[0])
                               & (Bursts[:, 2] <= roiR0[1])), 2]

        hMicroGII, _ = histc(accMicroGII, edges)
        hMicroGT, _ = histc(accMicroGT, edges)
        hMicroG = hMicroGII[:] + hMicroGT[:]

        hMicroRII, _ = histc(accMicroRII, edges)
        hMicroRT, _ = histc(accMicroRT, edges)
        hMicroR = hMicroRII[:] + hMicroRT[:]

        # function defined IRF_G, meanIRFG, IRF_R, meanIRFR, roiMLE_G, roiMLE_R

        roihMicroGII = hMicroGII[(roiMLE_G[0] - 1):roiMLE_G[1]]
        roihMicroGT = hMicroGT[(roiMLE_G[0] - 1):roiMLE_G[1]]

        roihMicroG = hMicroG[(roiMLE_G[0] - 1):roiMLE_G[1]]

        roi_accMicroGII = accMicroGII[(roiMLE_G[0] <= accMicroGII)
                                      & (accMicroGII <= roiMLE_G[1])]
        roi_accMicroGT = accMicroGT[(roiMLE_G[0] <= accMicroGT)
                                    & (accMicroGT <= roiMLE_G[1])]
        mean_roiMicroGII = np.sum(roi_accMicroGII) / len(roi_accMicroGII)

        mean_roiMicroGT = np.sum(roi_accMicroGT) / len(roi_accMicroGT)

        roihMicroR = hMicroR[roiMLE_R[0]:roiMLE_R[1]]

        roihMicroRII = hMicroRII[roiMLE_R[0]:roiMLE_R[1]]
        roihMicroRT = hMicroRT[roiMLE_R[0]:roiMLE_R[1]]

        roi_accMicroRII = accMicroRII[(roiMLE_R[0] <= accMicroRII)
                                      & (accMicroRII <= roiMLE_R[1])]
        roi_accMicroRT = accMicroRT[(roiMLE_R[0] <= accMicroRT)
                                    & (accMicroRT <= roiMLE_R[1])]

        mean_roiMicroRII = np.sum(roi_accMicroRII) / len(roi_accMicroRII)

        mean_roiMicroRT = np.sum(roi_accMicroRT) / len(roi_accMicroRT)

        # Def. conditions while differentiating GREEN (G) RED (R) and PRALLEL (II) + PERPENDICULAR (T)
        # for each case

        if any(roihMicroGII):
            tauArrD_II[i] = LifeMLE(newIRF_G_II, meanIRFG_II, roihMicroGII, mean_roiMicroGII, dtBin, boolFLA)
        else:
            tauArrD_II[i] = 0
        if any(roihMicroGT):
            tauArrD_T[i] = LifeMLE(newIRF_G_T, meanIRFG_T, roihMicroGT, mean_roiMicroGT, dtBin, boolFLA)
        else:
            tauArrD_T[i] = 0

        if any(roihMicroRII):
            tauArrA_II[i] = LifeMLE(newIRF_R_II, meanIRFR_II, roihMicroRII, mean_roiMicroRII, dtBin, boolFLA)
        else:
            tauArrA_II[i] = 0
        if any(roihMicroRT):
            tauArrA_T[i] = LifeMLE(newIRF_R_T, meanIRFR_T, roihMicroRT, mean_roiMicroRT, dtBin, boolFLA)
        else:
            tauArrA_T[i] = 0

    backgroundRates = Background['Background Rates']

    BurstData = np.array([(lastBN + np.arange(len(NG)) + 1).tolist(),
                          [el[0] for el in NG],
                          [el[0] for el in NGII],
                          [el[0] for el in NGT],
                          [el[0] for el in NR],
                          [el[0] for el in NRII],
                          [el[0] for el in NRT],
                          [el[0] for el in NR0],
                          [el[0] for el in NR0II],
                          [el[0] for el in NR0T],
                          (np.ones(len(NG)) * backgroundRates['BGII']).tolist(),
                          (np.ones(len(NG)) * backgroundRates['BGT']).tolist(),
                          (np.ones(len(NG)) * backgroundRates['BRII']).tolist(),
                          (np.ones(len(NG)) * backgroundRates['BRT']).tolist(),
                          (np.ones(len(NG)) * backgroundRates['BR0II']).tolist(),
                          (np.ones(len(NG)) * backgroundRates['BR0T']).tolist(),
                          [el[0] for el in TBurst],
                          [el[0] for el in arrFRET_2CDE],
                          [el[0] for el in arrAlex_2CDE],
                          [el[0] for el in dtGR_TR0],
                          tauArrD_II,
                          tauArrD_T,
                          tauArrA_II,
                          tauArrA_T,
                          [el[0] for el in TGR]]).T


    return BurstData
def save_burst_data(pathname, suffix, BurstData, boolPostA):
    """ Save burst data to a binary file. """
    fileB = Path(pathname) / f'BData{suffix}.bin'
    with fileB.open('ab') as f:
        np.save(f, BurstData, allow_pickle=True)

    if boolPostA:
        fileP = Path(pathname) / f'PData{suffix}.bin'
        with fileP.open('ab') as f:
            np.save(f, BurstData, allow_pickle=True)

def burst_fun(folder, ht3_locations, suffix, Brd_GGR,Brd_RR, threIT,threITN, minPhs, newIRF_G_II, newIRF_G_T, meanIRFG_II, meanIRFG_T,\
              newIRF_R_II, newIRF_R_T,  meanIRFR_II, meanIRFR_T, dtBin, setLeeFilter, boolFLA,boolTotal ,minGR ,minR0, \
              boolPostA, tauFRET, tauALEX, settingsDict, threshold_burst_detect=False):

    checkInner = np.array([0])
    arrData = []

    # get folder dir from file dir --> Robust since if the file can be handeld the folder is also correct
    folder_path = '/'.join(ht3_locations[folder][0].translate(str.maketrans({'/': '\\'})).split('\\')[0:-1])

    # save empty file for usage in getBurstAll
    dataAll = dict()
    dataAll['photonHIST'] = np.zeros([4096, 2])
    str_path_dA = folder_path + '/allHIST.npy'
    np.save(str_path_dA, dataAll)

    dataN = dict()
    dataN['backHIST'] = np.zeros([4096, 2])
    dataN['time'] = [0]
    str_pathdN = folder_path + '/backHIST.npy'
    np.save(str_pathdN, dataN)

    # Save settings in each folder
    settings_path = folder_path + f'/settings_{suffix}.csv'
    pd.DataFrame([settingsDict]).to_csv(settings_path, index=False)

    lastBN = 0

    if not threshold_burst_detect:
        for file in ht3_locations[folder]:#ht3_file_fps:

            file = file.translate(str.maketrans({'/': '\\'}))
            fileName = file.split('\\')[-1]
            folderName = '/'.join(file.split('\\')[0:-1])

            BurstData = getBurstAll(fileName, folderName, suffix, lastBN, Brd_GGR, Brd_RR, threIT,\
                                    threITN, minPhs, 10, newIRF_G_II, newIRF_G_T, meanIRFG_II, meanIRFG_T,\
                                    newIRF_R_II, newIRF_R_T, meanIRFR_II, meanIRFR_T, Brd_GGR, Brd_RR, dtBin,setLeeFilter,\
                                    boolFLA, boolTotal,minGR,minR0, boolPostA, checkInner, tauFRET, tauALEX)

            lastBN += len(BurstData)
        #ht3_file_fps.update()
    elif threshold_burst_detect:
        for file in ht3_locations[folder]:  # ht3_file_fps:
            file = file.translate(str.maketrans({'/': '\\'}))
            fileName = file.split('\\')[-1]
            folderName = '/'.join(file.split('\\')[0:-1])

            BurstData = getBurstAll(fileName, folderName, suffix, lastBN, Brd_GGR, Brd_RR, threIT, \
                                    threITN, minPhs, 10, newIRF_G_II, newIRF_G_T, meanIRFG_II, meanIRFG_T, \
                                    newIRF_R_II, newIRF_R_T, meanIRFR_II, meanIRFR_T, Brd_GGR, Brd_RR, dtBin, setLeeFilter, \
                                    boolFLA, boolTotal, minGR, minR0, boolPostA, checkInner, tauFRET, tauALEX)

            #lastBN += len(BurstData)



def get_files(folder):
    ht3_locations = dict()
    try:
        for path, subdirs, files in os.walk(folder):
            for name in files:
                if name.endswith('.ht3') or name.endswith('.ptu'):
                    try:
                        ht3_locations[name[0:3]] = ht3_locations[name[0:3]] + [os.path.join(path, name)]
                    except KeyError:
                        ht3_locations[name[0:3]] = [os.path.join(path, name)]
    except FileNotFoundError:
        return

    def sort_fun_key(string):
        string = string.split('/')[-1]
        if len(string) == 10:
            return string[0:6]
        else:
            return string[0:4] + '0' + string[4]

    # sort the folders
    for keys in ht3_locations.keys():
        ht3_locations[keys] = sorted(ht3_locations[keys], key=sort_fun_key)

    ht3_locations = collections.OrderedDict(sorted(ht3_locations.items()))

    return ht3_locations

def check_for_bdata_files(eval_folder, suffix):
    # Function that returns True if Bdata or Pdata files are present in the analysis folder
    # False if not

    for key in eval_folder.keys():
        bdata_file = '/'.join(eval_folder[key][0].translate(str.maketrans({'/': '\\'})) \
                              .split('\\')[0:-1]) + f'/Bdata{suffix}.bin'
        pdata_file = '/'.join(eval_folder[key][0].translate(str.maketrans({'/': '\\'})) \
                              .split('\\')[0:-1]) + f'/Bdata{suffix}.bin'

        if os.path.isfile(bdata_file) or os.path.isfile(pdata_file):
            return True

    return False

@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    # Source:
    # https://stackoverflow.com/questions/24983493/tracking-progress-of-joblib-parallel-execution/58936697#58936697
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    class TqdmBatchCompletionCallback(parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = parallel.BatchCompletionCallBack
    parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def par_burst(eval_folder, suffix, Brd_GGR, Brd_RR, threIT, threIT2, minPhs, IRF_G_II, IRF_G_T, meanIRFG_II,\
              meanIRFG_T, IRF_R_II, IRF_R_T, meanIRFR_II, meanIRFR_T, dtBin, setLeeFilter, boolFLA, boolTotal, minGR,\
              minR0, boolPostA, tauFRET, tauALEX, settings, threads=-2):


    #start_multi_run = time.time()
    with tqdm_joblib(tqdm(desc="Folders finished: ", total=len(eval_folder.keys()))) as progress_bar:
        Parallel(n_jobs=threads, prefer='processes')(delayed(burst_fun)(folder, eval_folder, suffix, Brd_GGR, Brd_RR, \
                                                                       threIT, threIT2, minPhs, \
                                                                       IRF_G_II, IRF_G_T, meanIRFG_II, meanIRFG_T, IRF_R_II,
                                                                       IRF_R_T, meanIRFR_II,meanIRFR_T, \
                                                                       dtBin, setLeeFilter, boolFLA, \
                                                                       boolTotal, minGR, minR0, boolPostA, tauFRET, tauALEX, settings,
                                                                       True)\
                                                    for folder in eval_folder.keys())

    #print(f'Multi thread run with {threads} threads took: ', time.time() - start_multi_run)


if __name__ == '__main__':
    import pickle

    with open('/Users/philipp/Desktop/Work/WHK Schlierf Group/autoFRET_SchliefGroupGit/autoFRET/Test_Data/SampleBurstIn.pkl', 'rb') as f:
        sample_data = pickle.load(f)


    par_burst(eval_folder=sample_data[0], suffix=sample_data[1], Brd_GGR=sample_data[2], Brd_RR=sample_data[3],
              threIT=sample_data[4], threIT2=sample_data[5], minPhs=sample_data[6], IRF_G_II=sample_data[7],
              IRF_G_T=sample_data[8], meanIRFG_II=sample_data[9], meanIRFG_T=sample_data[10], IRF_R_II=sample_data[11],
              IRF_R_T=sample_data[12], meanIRFR_II=sample_data[13], meanIRFR_T=sample_data[14], dtBin=sample_data[15],
              setLeeFilter=sample_data[16], boolFLA=sample_data[17], boolTotal=sample_data[18], minGR=sample_data[19],
              minR0=sample_data[20], boolPostA=sample_data[21], tauFRET=sample_data[22], tauALEX=sample_data[23],
              settings=sample_data[24], threads=1)

    '''getBurstAll(filename=list(sample_data[0].keys())[0], pathname=sample_data[0], suffix, lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, newIRF_G_II, \
                newIRF_G_T, meanIRFG_II, meanIRFG_T, newIRF_R_II, newIRF_R_T, meanIRFR_II, meanIRFR_T, roiMLE_G, \
                roiMLE_R, dtBin, setLeeFilter, boolFLA, boolTotal, minGR, minR0, boolPostA, checkInner, tauFRET,
                tauALEX)'''