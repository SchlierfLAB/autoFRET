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
                minGR, minR0, boolPostA, checkInner, tauFRET, tauALEX, method='time_based'):
    """
    Process photon burst data using either time-based or intensity-based thresholding.

    Parameters:
        method: str
            - 'time_based': Use the original burst detection method (inter-photon time)
            - 'intensity_based': Use the new intensity-based thresholding method
    """

    # Load and preprocess photon data
    Photons = load_photon_data(pathname, filename, roiRG, roiR0)

    # Detect burst with method based on user input
    if method == 'time_based':
        Bursts, background_data = detect_bursts_time_based(Photons, threIT, threIT2, minPhs, checkInner, boolTotal, setLeeFilter)
    elif method == 'intensity_based':
        # Todo: Decide on which bursts exactly shoudl be used
        Bursts, background_data = detect_bursts_intensity_based(Photons, minPhs, minGR)
    else:
        raise ValueError("Invalid method. Choose 'time_based' or 'intensity_based'.")

    # If no valid bursts are found, return empty
    if len(Bursts) == 0:
        print(f'The file {filename} has too much background and will not be analyzed.')
        return []

    # Compute burst statistics (FRET, ALEX, lifetimes)
    BurstData = process _burst_statistics(Bursts, background_data, roiMLE_G, roiMLE_R, dtBin, boolFLA,
                                         newIRF_G_II, newIRF_G_T, meanIRFG_II, meanIRFG_T,
                                         newIRF_R_II, newIRF_R_T, meanIRFR_II, meanIRFR_T,
                                         tauFRET, tauALEX)

    # Save burst data
    save_burst_data(pathname, suffix, BurstData, boolPostA)

    return BurstData


# ---- Sub-functions ---- #

def load_photon_data(pathname, filename, roiRG, roiR0):
    """ Load and filter raw photon data from a PTU file. """
    file_instance = Read_PTU(pathname + '/' + filename)
    Photons_Raw = file_instance.RawData

    # Filter photons by valid regions
    Photons = Photons_Raw[(Photons_Raw[:, 0] != 15) & (
            (Photons_Raw[:, 1] >= roiRG[0]) & (Photons_Raw[:, 1] <= roiRG[1]) |
            (Photons_Raw[:, 1] >= roiR0[0]) & (Photons_Raw[:, 1] <= roiR0[1]))]

    return Photons


def detect_bursts_time_based(Photons, threIT, threIT2, minPhs, checkInner, boolTotal, setLeeFilter):
    """ Original burst detection based on inter-photon time filtering. """
    # Extract inter-photon times
    interPhT = Photons[1:, 2] - Photons[:-1, 2]
    interLee = leeFilter(interPhT, setLeeFilter)

    # Apply first filtering step (inter-photon time threshold)
    indexSig = np.argwhere((0.4 < interLee) & (interLee < (threIT * 1e6)))
    indexSigN = np.argwhere(interLee > (threIT2 * 1e6))

    if indexSig.size == 0 or indexSigN.size == 0:
        return [], {}

    # Identify bursts based on detected events
    bStart, bLength = burstLoc(indexSig, 1)
    bStartN, bLengthN = burstLoc(indexSigN, 1)

    # Apply additional burst-length filtering
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

    return bStartLong, bLengthLong


def detect_bursts_intensity_based(Photons, minPhs, minGR):
    """ New burst detection based on intensity thresholding with background estimation. """

    # Define binning range (1 ms binning)
    edges = np.arange(1, 4097, 1)

    # Keep only real data (channels 1–4)
    PhotonsSGR0 = Photons[np.isin(Photons[:, 0], [1, 2, 3, 4]), 0:3]

    # Separate Donor (SGR) and Acceptor (R0) Channels
    subarray_1_3 = PhotonsSGR0[np.isin(PhotonsSGR0[:, 0], [1, 3])]  # Donor (SGR)
    subarray_2_4 = PhotonsSGR0[np.isin(PhotonsSGR0[:, 0], [2, 4])]  # Acceptor (R0)

    # Save data for debugging
    # Todo: remove when done
    with open('PhotonsSGR0.pkl', 'wb') as f:
        pickle.dump(PhotonsSGR0, f)

    # ---- Intensity Binning ---- #

    # Bin total intensity (all channels)
    BinsSGR0 = histc(PhotonsSGR0[:, 1], edges)
    valid_bins = np.where(BinsSGR0[0] >= minPhs)[0]
    IntensityTrace = PhotonsSGR0[np.isin(BinsSGR0[0], valid_bins)]

    # Bin donor channel intensity (1 & 3)
    Bins_1_3 = histc(subarray_1_3[:, 1], edges)
    valid_bins_1_3 = np.where(Bins_1_3[0] >= minGR)[0]
    Intensity_1_3 = subarray_1_3[np.isin(Bins_1_3[0], valid_bins_1_3)]

    # Bin acceptor channel intensity (2 & 4)
    Bins_2_4 = histc(subarray_2_4[:, 1], edges)
    valid_bins_2_4 = np.where(Bins_2_4[0] >= minGR)[0]
    Intensity_2_4 = subarray_2_4[np.isin(Bins_2_4[0], valid_bins_2_4)]

    # ---- Background Estimation ---- #

    # Identify background regions (bins below threshold)
    background_bins = np.where(BinsSGR0[0] < minPhs)[0]
    BackgroundTrace = PhotonsSGR0[np.isin(BinsSGR0[0], background_bins)]

    # Background for Donor (1&3)
    background_bins_1_3 = np.where(Bins_1_3[0] < minGR)[0]
    Background_1_3 = subarray_1_3[np.isin(Bins_1_3[0], background_bins_1_3)]

    # Background for Acceptor (2&4)
    background_bins_2_4 = np.where(Bins_2_4[0] < minGR)[0]
    Background_2_4 = subarray_2_4[np.isin(Bins_2_4[0], background_bins_2_4)]

    # Return structured burst and background data
    return {
        "Bursts": {
            "Total": IntensityTrace,
            "Donor (1&3)": Intensity_1_3,
            "Acceptor (2&4)": Intensity_2_4
        },
        "Background": {
            "Total": BackgroundTrace,
            "Donor (1&3)": Background_1_3,
            "Acceptor (2&4)": Background_2_4
        }
    }

def process_burst_statistics(Bursts, background_data, roiMLE_G, roiMLE_R, dtBin, boolFLA,
                             newIRF_G_II, newIRF_G_T, meanIRFG_II, meanIRFG_T,
                             newIRF_R_II, newIRF_R_T, meanIRFR_II, meanIRFR_T,
                             tauFRET, tauALEX):
    """Compute relevant statistics for each burst (FRET, ALEX, lifetimes)."""

    num_bursts = len(np.unique(Bursts[:, 0]))

    # Initialize storage arrays
    NG, NGII, NGT, NR, NRII, NRT, NR0, NR0II, NR0T = [np.zeros(num_bursts) for _ in range(9)]
    TBurst, TGR, TR0 = np.zeros(num_bursts), np.zeros(num_bursts), np.zeros(num_bursts)
    arrFRET_2CDE, arrAlex_2CDE = np.zeros(num_bursts), np.zeros(num_bursts)
    tauArrD_II, tauArrD_T, tauArrA_II, tauArrA_T = np.zeros(num_bursts), np.zeros(num_bursts), np.zeros(
        num_bursts), np.zeros(num_bursts)

    for i, burst_id in enumerate(np.unique(Bursts[:, 0])):
        # Extract single burst
        sglBData = Bursts[Bursts[:, 0] == burst_id, 1:4]

        # Count photons per channel
        NGII[i] = np.count_nonzero(sglBData[:, 0] == 2)
        NGT[i] = np.count_nonzero(sglBData[:, 0] == 4)
        NG[i] = NGII[i] + NGT[i]

        NRII[i] = np.count_nonzero(
            (sglBData[:, 0] == 1) & (roiMLE_G[0] <= sglBData[:, 1]) & (sglBData[:, 1] <= roiMLE_G[1]))
        NRT[i] = np.count_nonzero(
            (sglBData[:, 0] == 3) & (roiMLE_G[0] <= sglBData[:, 1]) & (sglBData[:, 1] <= roiMLE_G[1]))
        NR[i] = NRII[i] + NRT[i]

        NR0II[i] = np.count_nonzero(
            (sglBData[:, 0] == 1) & (roiMLE_R[0] <= sglBData[:, 1]) & (sglBData[:, 1] <= roiMLE_R[1]))
        NR0T[i] = np.count_nonzero(
            (sglBData[:, 0] == 3) & (roiMLE_R[0] <= sglBData[:, 1]) & (sglBData[:, 1] <= roiMLE_R[1]))
        NR0[i] = NR0II[i] + NR0T[i]

        # Compute burst duration (sum of inter-photon times)
        TBurst[i] = np.sum(np.diff(sglBData[:, 2])) * 1e-9  # Convert to seconds

        # Compute macrotime averages
        macroGR = sglBData[(sglBData[:, 0] == 2) | (sglBData[:, 0] == 4), 2]
        macroR0 = sglBData[((sglBData[:, 0] == 1) | (sglBData[:, 0] == 3)) & (roiMLE_R[0] <= sglBData[:, 1]) & (
                    sglBData[:, 1] <= roiMLE_R[1]), 2]

        if len(macroGR) > 0:
            TGR[i] = np.mean(macroGR) * 1e-6  # Convert to microseconds
        if len(macroR0) > 0:
            TR0[i] = np.mean(macroR0) * 1e-6  # Convert to microseconds

        # Compute FRET and ALEX efficiency
        arrFRET_2CDE[i] = FRET_2CDE(macroR0 * 1e-6, macroGR * 1e-6, tauFRET / 1000)
        arrAlex_2CDE[i] = Alex_2CDE(macroR0 * 1e-6, macroGR * 1e-6, tauALEX / 1000)

        # Fluorescence Lifetime Estimation
        edges = np.arange(1, 4097)  # Define binning range for histograms
        accMicroGII = sglBData[sglBData[:, 0] == 2, 2]
        accMicroGT = sglBData[sglBData[:, 0] == 4, 2]
        accMicroRII = sglBData[
            (sglBData[:, 0] == 1) & (roiMLE_G[0] <= sglBData[:, 1]) & (sglBData[:, 1] <= roiMLE_G[1]), 2]
        accMicroRT = sglBData[
            (sglBData[:, 0] == 3) & (roiMLE_G[0] <= sglBData[:, 1]) & (sglBData[:, 1] <= roiMLE_G[1]), 2]

        # Compute histograms
        hMicroGII, _ = np.histogram(accMicroGII, bins=edges)
        hMicroGT, _ = np.histogram(accMicroGT, bins=edges)
        hMicroRII, _ = np.histogram(accMicroRII, bins=edges)
        hMicroRT, _ = np.histogram(accMicroRT, bins=edges)

        # Lifetime estimation (apply IRF correction)
        if any(hMicroGII):
            tauArrD_II[i] = LifeMLE(newIRF_G_II, meanIRFG_II, hMicroGII, np.mean(accMicroGII), dtBin, boolFLA)
        if any(hMicroGT):
            tauArrD_T[i] = LifeMLE(newIRF_G_T, meanIRFG_T, hMicroGT, np.mean(accMicroGT), dtBin, boolFLA)
        if any(hMicroRII):
            tauArrA_II[i] = LifeMLE(newIRF_R_II, meanIRFR_II, hMicroRII, np.mean(accMicroRII), dtBin, boolFLA)
        if any(hMicroRT):
            tauArrA_T[i] = LifeMLE(newIRF_R_T, meanIRFR_T, hMicroRT, np.mean(accMicroRT), dtBin, boolFLA)

    # Return processed data
    return np.column_stack(
        [NG, NGII, NGT, NR, NRII, NRT, NR0, NR0II, NR0T, TBurst, TGR, TR0, arrFRET_2CDE, arrAlex_2CDE, tauArrD_II,
         tauArrD_T, tauArrA_II, tauArrA_T])


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

            BurstData = getBurstAllIntensity(fileName, folderName, suffix, lastBN, Brd_GGR, Brd_RR, threIT, \
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
    test_folder_path = '/Users/philipp/Desktop/Work/WHK Schlierf Group/smFRET_Software/speed_tests' \
                       '/DeadLockMEas/DeadLockFull/E11'

    with open('/Users/philipp/Desktop/Work/WHK Schlierf Group/autoFRET_SchliefGroupGit/autoFRET/Test_Data/SampleBurstIn.pkl', 'rb') as f:
        sample_data = pickle.load(f)


    par_burst(eval_folder=sample_data[0], suffix=sample_data[1], Brd_GGR=sample_data[2], Brd_RR=sample_data[3],
              threIT=sample_data[4], threIT2=sample_data[5], minPhs=sample_data[6], IRF_G_II=sample_data[7],
              IRF_G_T=sample_data[8], meanIRFG_II=sample_data[9], meanIRFG_T=sample_data[10], IRF_R_II=sample_data[11],
              IRF_R_T=sample_data[12], meanIRFR_II=sample_data[13], meanIRFR_T=sample_data[14], dtBin=sample_data[15],
              setLeeFilter=sample_data[16], boolFLA=sample_data[17], boolTotal=sample_data[18], minGR=sample_data[19],
              minR0=sample_data[20], boolPostA=sample_data[21], tauFRET=sample_data[22], tauALEX=sample_data[23],
              settings=sample_data[24], threads=1, )

    '''getBurstAll(filename=list(sample_data[0].keys())[0], pathname=sample_data[0], suffix, lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, newIRF_G_II, \
                newIRF_G_T, meanIRFG_II, meanIRFG_T, newIRF_R_II, newIRF_R_T, meanIRFR_II, meanIRFR_T, roiMLE_G, \
                roiMLE_R, dtBin, setLeeFilter, boolFLA, boolTotal, minGR, minR0, boolPostA, checkInner, tauFRET,
                tauALEX)'''