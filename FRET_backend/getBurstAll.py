import os.path

from FRET_backend.read_ht3_vect import read_ht3_raw
from FRET_backend.lee_filter import leeFilter
from FRET_backend.burst_locator import burstLoc
from FRET_backend.To_CDE_Functions import FRET_2CDE, Alex_2CDE
from FRET_backend.LifeMLE import LifeMLE

import numpy as np
import scipy.io as sio
from pathlib import Path


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

def getBurstAll(filename, pathname, suffix, lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, IRF_G,
                meanIRFG, IRF_R, meanIRFR, roiMLE_G, roiMLE_R, dtBin, setLeeFilter, boolFLA, gGG, gRR, boolTotal, minGR, minR0,
                boolPostA, checkInner):

    Photons_Raw = read_ht3_raw(pathname + '/' + filename, False)
    Photons = Photons_Raw[(Photons_Raw[:,0] != 15) & ((Photons_Raw[:,1] >= roiRG[0]) & (Photons_Raw[:,1] <= roiRG[1]) |
                                                      ((Photons_Raw[:,1] >= roiR0[0]) & (Photons_Raw[:,1] <= roiR0[1])))]

    # keep just real data and seperate them in channels
    PhotonsSGR0 = Photons[(Photons[:,0]==1) | (Photons[:,0]==2) | (Photons[:,0]==3) | (Photons[:,0]==4), 0:3]
    PhotonsSG = Photons[(Photons[:,0]==2) | (Photons[:,0]==4) ,1:3]
    PhotonsSR = Photons[((Photons[:,0]==1) | (Photons[:,0]==3)) & (Photons[:,1]>=roiRG[0]) & (Photons[:,1]<=roiRG[1]) ,1:3]
    PhotonsSR0 = Photons[((Photons[:,0]==1) | (Photons[:,0]==3)) & (Photons[:,1] >= roiR0[0]) & (Photons[:,1] <= roiR0[1]),1:3]

    #del Photons


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
        #print(np.size(bStartLong))
        for i in range(np.size(bStartLong)):

            Bursts[lInd:lInd+int(bLengthLong[i]),:] = np.c_[np.ones(int(bLengthLong[i])).T * (i+1),
                                                            PhotonsSGR0[int(bStartLong[i])+1:int(bStartLong[i])+
                                                                                             int(bLengthLong[i])+1,0:4]]
            lInd = lInd + int(bLengthLong[i])

            hAll,_ = histc(Photons_Raw[(Photons_Raw[:,0] != 15)
                                       & ((Photons_Raw[:,0] == 1) | (Photons_Raw[:,0]==3))
                                       & ((Photons_Raw[:,2] >= PhotonsSGR0[bStartLong[i],2])
                                          &  (Photons_Raw[:,2] <= PhotonsSGR0[bStartLong[i] + int(bLengthLong[i]), 2])),1]
                           , edges)

            dataAll.item().get('photonHIST')[:,0] = dataAll.item().get('photonHIST')[:,0] + hAll
            hAll,_ = histc(Photons_Raw[(Photons_Raw[:,0] != 15)
                                       & ((Photons_Raw[:,0] == 2) | (Photons_Raw[:,0]==4))
                                       & ((Photons_Raw[:,2] >= PhotonsSGR0[bStartLong[i],2])
                                          &  (Photons_Raw[:,2] <= PhotonsSGR0[bStartLong[i] + int(bLengthLong[i]), 2])),1]
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

        #prefill = np.zeros(len(bLengthLong))
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
        TGR_ = np.zeros(len(bLengthLong)) # averaged macrotime of total 530nm excited burst photons
        TR0_ = np.zeros(len(bLengthLong)) # averaged macrotime of red 640nm exited burst photons

        for i in range(len(bStartLong)):

            N_ = Bursts[Bursts[:,0] == (i+1), 1:4]

            NGII_[i] = len(N_[N_ == 2])

            NGT_[i] = len(N_[N_ == 4])

            NG_[i] = NGII_[i] + NGT_[i]

            NRII_[i] = len(N_[(N_[:,0] == 1)
                              & (N_[:,1] >= roiRG[0])
                              & (N_[:,1] <= roiRG[1]),0])

            NRT_[i] = len(N_[(N_[:,0] == 3)
                             & (N_[:,1] >= roiRG[0])
                             & (N_[:,1] <= roiRG[1]),0])

            NR_[i] = NRII_[i] + NRT_[i]

            NR0II_[i] = len(N_[(N_[:,0] == 1)
                               & (N_[:,1] >= roiR0[0])
                               & (N_[:,1] <= roiR0[1]),0])

            NR0T_[i] = len(N_[(N_[:,0] == 3)
                              & (N_[:,1] >= roiR0[0])
                              & (N_[:,1] <= roiR0[1]),0])

            NR0_[i] = NR0II_[i] + NR0T_[i]

            TBurst_[i] = np.sum(interPhT[bStartLong[i]:bStartLong[i]+int(bLengthLong[i])-1]*1e-9)

            phBurst = PhotonsSGR0[bStartLong[i]+1:bStartLong[i]+int(bLengthLong[i])+1,0:3]

            macroGR = phBurst[(phBurst[:,0]==2)
                              | (phBurst[:,0]==4)
                              | (((phBurst[:,0]==1) | (phBurst[:,0]==3)) & (phBurst[:,1] >= roiRG[0]) & (phBurst[:,1]<=roiRG[1])), 2]


            macroR0 = phBurst[((phBurst[:,0] == 1) | (phBurst[:,0] == 3))
                              & (phBurst[:,1] >= roiR0[0])
                              & (phBurst[:,1] <= roiR0[1]), 2]

            macroR = phBurst[((phBurst[:,0] == 1) | (phBurst[:,0] == 3))
                             & (phBurst[:,1] >= roiRG[0])
                             & (phBurst[:,1] <= roiRG[1]), 2]

            macroG = phBurst[(phBurst[:,0] == 2) | (phBurst[:,0] == 4), 2]


            TGR_[i] =  np.sum(macroGR) / len(macroGR) * 1e-6
            TR0_[i] = np.sum(macroR0) / len(macroR0) * 1e-6

            #print((np.sum(macroGR) / len(macroGR) * 1e-6)-(np.sum(macroR0) / len(macroR0) * 1e-6))

            arrFRET_2CDE_[i] = FRET_2CDE(macroR * 1e-6, macroG * 1e-6, 0.0125)
            arrAlex_2CDE_[i] = Alex_2CDE(macroR0 * 1e-6, macroGR * 1e-6, 0.075)

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


if __name__ == '__main__':
    print('Main run getBurstAll.py')

