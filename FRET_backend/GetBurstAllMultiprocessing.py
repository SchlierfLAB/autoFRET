import os.path

from FRET_backend.read_ht3_vect import read_ht3_raw
from FRET_backend.lee_filter import leeFilter
from FRET_backend.burst_locator import burstLoc

from FRET_backend.LifeMLE import LifeMLE

import numpy as np
from numpy import c_
import scipy.io as sio
from pathlib import Path
from joblib import Parallel, delayed
from OnTheFlyBurst_Scripts.get_burst_input import get_input

import time
from numba import jit, njit
import collections


def get_files(folder):
    ht3_locations = dict()
    try:
        for path, subdirs, files in os.walk(folder):
            for name in files:
                if name.endswith('.ht3'):
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





def third_loop(roiRG, roiR0, interPhT, bLengthLong, bStartLong, Bursts, PhotonsSGR0):
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

        arrFRET_2CDE_[i] = FRET_2CDE(macroR * 1e-6, macroG * 1e-6, 0.0125)
        arrAlex_2CDE_[i] = Alex_2CDE(macroR0 * 1e-6, macroGR * 1e-6, 0.075)

    return arrAlex_2CDE_, arrFRET_2CDE_, NG_, NGII_, NGT_, NR_, NRII_, NRT_, NR0_, NR0II_, NR0T_, TBurst_, TGR_, TR0_



def getBurstAll(filename, pathname, suffix, lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, IRF_G,
                meanIRFG, IRF_R, meanIRFR, roiMLE_G, roiMLE_R, dtBin, setLeeFilter, boolFLA, gGG, gRR, boolTotal, minGR, minR0,
                boolPostA, checkInner):


    Photons_Raw = read_ht3_raw(pathname + '/' + filename, False)


    Photons = Photons_Raw[(Photons_Raw[:,0] != 15) & ((Photons_Raw[:,1] >= roiRG[0]) & (Photons_Raw[:,1] <= roiRG[1]) |
                                                      ((Photons_Raw[:,1] >= roiR0[0]) & (Photons_Raw[:,1] <= roiR0[1])))]


    # keep just real data and seperate them in channels
    PhotonsSGR0 = Photons[(Photons[:,0]==1) | (Photons[:,0]==2) | (Photons[:,0]==3) | (Photons[:,0]==4), 0:3]


    # inter-photon time
    interPhT = PhotonsSGR0[1:,2] - PhotonsSGR0[0:-1,2]
    interLee = leeFilter(interPhT, setLeeFilter)



    # 1st filter
    # threshold for inter photon time
    indexSig = np.argwhere((0.4 < interLee) & (interLee < (threIT*1000000)))
    indexSigN = np.argwhere(interLee > (threIT2*1000000))

    # channel histogram
    strAllHIST = pathname + '/allHIST.npy'
    dataAll = np.load(strAllHIST, allow_pickle=True)
    edges = np.arange(1,4097,1)


    if indexSig.size != 0:
        bStart, bLength = burstLoc(indexSig,1)
        bStartN, bLengthN = burstLoc(indexSigN, 1)

        # second filter
        # minimum photons per burst

        if boolTotal == 1:

            if checkInner == 1:
                bStartLong = bStart[bLength >= minPhs]+30
                bLengthLong = bLength[bLength >= minPhs]-60
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

        bStartLongN = bStartN[bLengthN >= 160] + 30
        bLengthLongN = bLengthN[bLengthN >= 160] - 60

        # collect Photons
        # Bursts = [BurstNumber, Channel, Microtime, Macrotime]

        Bursts = np.zeros([int(np.sum(bLengthLong)),4])
        lInd = 0


        for i in range(np.size(bStartLong)):

            Bursts[lInd:lInd+int(bLengthLong[i]),:] = np.c_[np.ones(int(bLengthLong[i])).T * (i+1),
                                                            PhotonsSGR0[int(bStartLong[i])+1:int(bStartLong[i])+
                                                                                             int(bLengthLong[i])+1,0:4]]
            lInd = lInd + int(bLengthLong[i])

            hAll,_ = histc(Photons_Raw[(Photons_Raw[:,0] != 15)
                                       & ((Photons_Raw[:,0] == 1) | (Photons_Raw[:,0]==3))
                                       & ((Photons_Raw[:,2] >= PhotonsSGR0[bStartLong[i],2])
                                          & (Photons_Raw[:,2] <= PhotonsSGR0[bStartLong[i] + int(bLengthLong[i]), 2])),1]
                           , edges)

            dataAll.item().get('photonHIST')[:,0] = dataAll.item().get('photonHIST')[:,0] + hAll
            hAll,_ = histc(Photons_Raw[(Photons_Raw[:,0] != 15)
                                       & ((Photons_Raw[:,0] == 2) | (Photons_Raw[:,0]==4))
                                       & ((Photons_Raw[:,2] >= PhotonsSGR0[bStartLong[i],2])
                                          & (Photons_Raw[:,2] <= PhotonsSGR0[bStartLong[i] + int(bLengthLong[i]), 2])),1]
                           , edges)
            dataAll.item().get('photonHIST')[:,1] = dataAll.item().get('photonHIST')[:,1] + hAll

        del Photons_Raw

        # channel background histogram and background counts
        np.save(strAllHIST, dataAll)


        BackNGII = 0
        BackNGT = 0
        BackNRII = 0
        BackNRT = 0
        BackNR0II = 0
        BackNR0T = 0
        BackT = 0

        # channel background histogram and background counts
        strHIST = pathname + '/backHIST.npy'
        dataN = np.load(strHIST, allow_pickle=True)

        for i in range(len(bStartLongN)):

            GapPhotons = PhotonsSGR0[bStartLongN[i]+1:bStartLongN[i]+int(bLengthLongN[i])+1,0:3]
            BackT = BackT + GapPhotons[-1,2] - GapPhotons[0,2]

            GapPhGII = GapPhotons[(GapPhotons[:,0] == 2)
                                  & (GapPhotons[:,1] >= roiRG[0])
                                  & (GapPhotons[:,1] <= roiRG[1])]

            GapPhGT = GapPhotons[(GapPhotons[:,0] == 4)
                                 & (GapPhotons[:,1] >= roiRG[0])
                                 & (GapPhotons[:,1] <= roiRG[1])]

            GapPhRII = GapPhotons[(GapPhotons[:,0] == 1)
                                  & (GapPhotons[:,1] >= roiRG[0])
                                  & (GapPhotons[:,1] <= roiRG[1])]

            GapPhRT = GapPhotons[(GapPhotons[:,0] == 3)
                                 & (GapPhotons[:,1] >= roiRG[0])
                                 & (GapPhotons[:,1] <= roiRG[1])]

            GapPhR0II = GapPhotons[(GapPhotons[:,0] == 1)
                                   & (GapPhotons[:,1] >= roiR0[0])
                                   & (GapPhotons[:,1] <= roiR0[1])]

            GapPhR0T = GapPhotons[(GapPhotons[:,0] == 3)
                                  & (GapPhotons[:,1] >= roiR0[0])
                                  & (GapPhotons[:,1] <= roiR0[1])]

            BackNGII = BackNGII+len(GapPhGII)
            BackNGT = BackNGT+len(GapPhGT)
            BackNRII = BackNRII+len(GapPhRII)
            BackNRT = BackNRT+len(GapPhRT)
            BackNR0II = BackNR0II+len(GapPhR0II)
            BackNR0T = BackNR0T+len(GapPhR0T)

            hGapPhGII,_ = histc(GapPhotons[(GapPhotons[:,0] == 2)
                                           & (GapPhotons[:,1] >= roiRG[0])
                                           & (GapPhotons[:,1] <= roiRG[1]),1],edges)

            hGapPhGT,_ = histc(GapPhotons[(GapPhotons[:,0] == 4)
                                          & (GapPhotons[:,1] >= roiRG[0])
                                          & (GapPhotons[:,1] <= roiRG[1]),1],edges)


            dataN.item().get('backHIST')[:,0] = dataN.item().get('backHIST')[:,0]+hGapPhGII
            dataN.item().get('backHIST')[:,1] = dataN.item().get('backHIST')[:,1]+hGapPhGT
            dataN.item().get('time')[0] = dataN.item().get('time')[0]+BackT/1e9


        # Save dataN
        np.save(strHIST, dataN)

        # Todo: Decide on how to save the var(dataAll)


        if BackT:

            BGII = BackNGII / BackT*1e9
            BGT = BackNGT / BackT*1e9
            BRII = BackNRII / BackT*1e9
            BRT = BackNRT / BackT*1e9
            BR0II = BackNR0II / BackT*1e9
            BR0T = BackNR0T / BackT*1e9

        else:
            BGII = 0
            BGT = 0
            BRII = 0
            BRT = 0
            BR0II = 0
            BR0T = 0

        # separate all number of photons

        arrAlex_2CDE_, arrFRET_2CDE_, NG_, NGII_, NGT_, NR_, NRII_, NRT_, NR0_, NR0II_, NR0T_, TBurst_, TGR_, TR0_ = \
            third_loop(roiRG, roiR0, interPhT, bLengthLong, bStartLong, Bursts, PhotonsSGR0)

        # 3rd filter
        # acceptor bleaching


        dTGR_TR0_ = TGR_ - TR0_
        dTGR_TR0_[np.isnan(TR0_)] = 9.9

        if boolTotal == 1:
            accBIndex = np.argwhere(np.abs(dTGR_TR0_) < threAveT)
        else:
            accBIndex = np.argwhere((np.abs(dTGR_TR0_) < threAveT) & ((NG_ + NR_) >= minGR) & (NR0_ >= minR0))


        dtGR_TR0 = dTGR_TR0_[accBIndex]

        NG = NG_[accBIndex]
        NGII = NGII_[accBIndex]
        NGT = NGT_[accBIndex]
        NR = NR_[accBIndex]
        NRII = NRII_[accBIndex]
        NRT = NRT_[accBIndex]
        NR0 = NR0_[accBIndex]
        NR0II = NR0II_[accBIndex]
        NR0T = NR0T_[accBIndex]
        TBurst = TBurst_[accBIndex]
        TGR = TGR_[accBIndex]
        arrFRET_2CDE = arrFRET_2CDE_[accBIndex]
        arrAlex_2CDE = arrAlex_2CDE_[accBIndex]

        accBursts = np.array([])

        tauArrD = np.zeros(len(accBIndex))
        tauArrA = np.zeros(len(accBIndex))

        edges = np.arange(1, 4097)

        # Alert alert: We are dealing with indexes here. accBIndex scales in python format from 0 to +inf
        # while the first column in Bursts gives the positions in matlab format from 1 to +inf
        # --> To get correct result one needs to cope that with a -1 or +1 operation

        accBursts = np.zeros([np.sum(np.isin(Bursts[:,0],accBIndex+1)),4])
        actIndex = 0


        for i in range(len(accBIndex)):

            sglBData = Bursts[Bursts[:,0] == (accBIndex[i]+1), 1:4]
            numB = len(sglBData)

            accBursts[actIndex:(actIndex+numB),:] = np.c_[np.ones(numB) * (i+1+lastBN), Bursts[Bursts[:,0]==(accBIndex[i]+1),1:4]]

            actIndex += numB

            accMicroGII = Bursts[(Bursts[:,0] == accBIndex[i]+1)
                                 & (Bursts[:,1] == 2), 2]
            accMicroGT = Bursts[(Bursts[:,0] == accBIndex[i]+1)
                                & (Bursts[:,1] == 4), 2]
            accMicroRII = Bursts[(Bursts[:,0] == accBIndex[i]+1)
                                 & ((Bursts[:,1] == 1)
                                    & (Bursts[:,2]>=roiR0[0])
                                    & (Bursts[:,2]<= roiR0[1])), 2]
            accMicroRT = Bursts[(Bursts[:,0] == accBIndex[i]+1)
                                & ((Bursts[:,1] == 3)
                                   & (Bursts[:,2]>=roiR0[0])
                                   & (Bursts[:,2]<= roiR0[1])), 2]

            hMicroGII, _ = histc(accMicroGII,edges)
            hMicroGT, _ = histc(accMicroGT, edges)
            hMicroG = gGG * hMicroGII[:] + hMicroGT[:]

            hMicroRII, _ = histc(accMicroRII,edges)
            hMicroRT, _ = histc(accMicroRT, edges)
            hMicroR = gRR * hMicroRII[:] + hMicroRT[:]
            roihMicroG = hMicroG[(roiMLE_G[0]-1):roiMLE_G[1]]


            roi_accMicroGII = accMicroGII[(roiMLE_G[0] <= accMicroGII)
                                          & (accMicroGII <= roiMLE_G[1])]
            roi_accMicroGT = accMicroGT[(roiMLE_G[0] <= accMicroGT)
                                        & (accMicroGT <= roiMLE_G[1])]
            mean_roiMicroG = np.sum(np.append(gGG * roi_accMicroGII, roi_accMicroGT)) / \
                             (gGG*len(roi_accMicroGII) + len(roi_accMicroGT))


            roihMicroR = hMicroR[roiMLE_R[0]:roiMLE_R[1]]

            roi_accMicroRII = accMicroRII[(roiMLE_R[0] <= accMicroRII)
                                          & (accMicroRII <= roiMLE_R[1])]
            roi_accMicroRT = accMicroRT[(roiMLE_R[0] <= accMicroRT)
                                        & (accMicroRT <= roiMLE_R[1])]
            mean_roiMicroR = np.sum(np.append(gRR * roi_accMicroRII, roi_accMicroRT)) / \
                             (gRR*len(roi_accMicroRII) + len(roi_accMicroRT))


            if any(roihMicroG):
                tauArrD[i] = LifeMLE(IRF_G, meanIRFG, roihMicroG, mean_roiMicroG, dtBin, boolFLA, roiRG[0])
            else:
                tauArrD[i] = 0
            if any(roihMicroR):
                tauArrA[i] = LifeMLE(IRF_R, meanIRFR, roihMicroR, mean_roiMicroR, dtBin, boolFLA,0)
            else:
                tauArrA[i] = 0


        BurstData = np.array([(lastBN + np.arange(len(NG))+1).tolist(),
                                  [el[0] for el in NG],
                                  [el[0] for el in NGII],
                                  [el[0] for el in NGT],
                                  [el[0] for el in NR],
                                  [el[0] for el in NRII],
                                  [el[0] for el in NRT],
                                  [el[0] for el in NR0],
                                  [el[0] for el in NR0II],
                                  [el[0] for el in NR0T],
                                  (np.ones(len(NG)) * BGII).tolist(),
                                  (np.ones(len(NG)) * BGT).tolist(),
                                  (np.ones(len(NG)) * BRII).tolist(),
                                  (np.ones(len(NG)) * BRT).tolist(),
                                  (np.ones(len(NG)) * BR0II).tolist(),
                                  (np.ones(len(NG)) * BR0T).tolist(),
                                  [el[0] for el in TBurst],
                                  [el[0] for el in arrFRET_2CDE],
                                  [el[0] for el in arrAlex_2CDE],
                                  [el[0] for el in dtGR_TR0],
                                  tauArrD,
                                  tauArrA,
                                  [el[0] for el in TGR]]).T


        # save burst data
        fileB = pathname + '/' + 'BData' + str(suffix)+'.bin'

        #print('\n\n')
        #print('Save BData to: ', fileB)
        with Path(fileB).open('ab') as f:
            np.save(f, BurstData, allow_pickle=True)
            print(f'Saved to: {fileB}')



        if boolPostA:
            # save data to file
            # Major compatibility can occure because Matlap -> Column Major and Python -> Row Major
            # https://scottstaniewicz.com/articles/python-matlab-binary/ --> For Matlab python comparison
            fileP = pathname + '/' + 'PData' + str(suffix)+'.bin'

            # append to the single file
            # https://stackoverflow.com/questions/30376581/save-numpy-array-in-append-mode

            #print(accBursts)
            #print('Save PData to: ', fileP)
            with Path(fileP).open('ab') as f:
                np.save(f, accBursts, allow_pickle=True)

        return BurstData

    return []

def burst_fun(folder, ht3_locations, suffix, Brd_GGR,Brd_RR, threIT,threITN, minPhs, newIRF_G, meanIRFG, \
              newIRF_R,  meanIRFR, dtBin, setLeeFilter, boolFLA, gGG, gRR,boolTotal ,minGR ,minR0, \
              boolPostA):

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

    lastBN = 0
    print(f'\nWorker on folder: {folder}\n')

    for file in ht3_locations[folder]:

        file = file.translate(str.maketrans({'/': '\\'}))
        fileName = file.split('\\')[-1]
        folderName = '/'.join(file.split('\\')[0:-1])

        BurstData = getBurstAll(fileName, folderName,suffix, lastBN, Brd_GGR,Brd_RR, threIT \
                                    ,threITN, minPhs, 10,  newIRF_G, meanIRFG, newIRF_R, \
                                    meanIRFR, Brd_GGR, Brd_RR, dtBin,setLeeFilter, \
                                boolFLA,gGG,gRR,boolTotal,minGR,minR0, \
                                boolPostA, checkInner)
        lastBN += len(BurstData)


def get_files(folder):
    ht3_locations = dict()
    try:
        for path, subdirs, files in os.walk(folder):
            for name in files:
                if name.endswith('.ht3'):
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


def par_burst(eval_folder_path, suffix, Brd_GGR, Brd_RR, threIT, threIT2, minPhs, IRF_G, meanIRFG, IRF_R, \
              meanIRFR, dtBin, setLeeFilter, boolFLA, gGG, gRR, boolTotal, minGR, minR0, boolPostA, \
              threads=-2):

    print('In par burst')

    eval_folder = get_files(eval_folder_path)

    print(eval_folder)

    print(f'Test parrallel on {threads} threads')

    start_multi_run = time.time()


    Parallel(n_jobs=threads, prefer='processes')(delayed(burst_fun)(folder, eval_folder, suffix, Brd_GGR, Brd_RR, \
                                                                   threIT, threIT2, minPhs, \
                                                                   IRF_G, meanIRFG, IRF_R, meanIRFR, \
                                                                   dtBin, setLeeFilter, boolFLA, gGG, gRR, \
                                                                   boolTotal, minGR, minR0, boolPostA) \
                                                for folder in eval_folder.keys())

    print(f'Multi thread run with {threads} threads took: ', time.time() - start_multi_run)


if __name__ == '__main__':
    test_folder_path = '/Users/philipp/Desktop/Work/WHK Schlierf Group/smFRET_Software/speed_tests/eval_folder'


    threIT, threIT2, minPhs, threAveT, IRF_G, meanIRFG, IRF_R, meanIRFR, dtBin, setLeeFilter, boolFLA, \
    gGG, gRR, boolTotal, minGR, minR0, boolPostA, checkInner = get_input()

    threads = -3  # multiprocessing.cpu_count()  # often confused with cores

    par_burst(test_folder_path, 'test', np.array([12,1387]), np.array([1687,1913]), threIT[0], threIT2[0], minPhs[0], IRF_G[0], meanIRFG[0], IRF_R[0], \
              meanIRFR[0], dtBin[0], setLeeFilter[0][0], boolFLA[0], gGG[0], gRR[0], boolTotal[0], minGR[0], minR0[0], boolPostA[0], \
              threads=-2)

