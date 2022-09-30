import os.path

#from FRET_backend.read_ht3_vect import read_ht3_raw
#from FRET_backend.lee_filter import leeFilter
#from FRET_backend.burst_locator import burstLoc
#from FRET_backend.To_CDE_Functions import FRET_2CDE, Alex_2CDE
from FRET_backend.LifeMLE import LifeMLE

import numpy as np
import scipy.io as sio
from pathlib import Path

from scipy.ndimage.measurements import variance
from scipy import ndimage
from scipy.interpolate import CubicSpline, interp1d

import cv2
import copy

# numba imports
from numba import jit


@jit(nopython=True)
def LifeMLE(IRF, meanIRF, Data, meanData, dtBin, boolFLA, roiLeft):

    if any(Data) and (np.sum(Data) != 0):

        numCh = len(Data)
        N = np.sum(Data)
        ies = np.arange(1,numCh+1,1)

        if (boolFLA == 0) and (np.sum(Data) >= 10):
            tau1 = np.arange(0,10.2,0.2)+0.01
            logMLE = np.zeros(len(tau1))

            for i in range(len(tau1)):
                func = np.exp(-ies * dtBin / tau1[i] / 1000)
                fold = convol(IRF, func)
                g = fold / np.sum(fold) * N
                ind = (g>0) & (Data > 0)
                logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
            del i

            # split fit
            t = np.arange(0.01, 10.02, 0.1)
            SplFunc = CubicSpline(x=tau1, y=logMLE) # piecewise cubic polynomial which is twice continuously differentiable
            Spl = SplFunc(t) # get y values from fit function
            v = np.min(Spl)

            # Todo: Well just confirm with others if this is the way
            # not to sure about the [0] but as it seems matlab [val, index] = min(someStuff) does only return
            # the index of a singl/first occuring minimum item. If one do this on a list of zeros the index
            # returned is just 1 (first element because of MATLAB counting system) but np.where gives a array
            # with all elements --> so by [0] only first index element is selected (does work if there is only
            # a single element
            # wow lots of comments for a simple expression lets ad another
            # höhö
            indMin = np.where(Spl == v)[0][0]

            minTau1 = t[indMin]


            tau2 = np.arange(minTau1-1, minTau1+1.1,0.1)
            del logMLE, func, g, ind # clear var before assigning new values
            logMLE = np.zeros(len(tau2))

            for i in range(len(tau2)):

                if tau2[i] > 0:
                    func = np.exp(-ies * dtBin / tau2[i] / 1000)
                    fold = convol(IRF, func)
                    g = fold / np.sum(fold) * N
                    ind = (g>0) & (Data > 0)
                    logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
                else:
                    logMLE[i] = np.inf
            del i

            # split fit
            t = np.arange(tau2[0], tau2[-1] + ((tau2[-1] - tau2[0]) / 100), (tau2[-1] - tau2[0]) / 100)
            # fill by extrapolation to have proper interpolation range
            # Todo: Danger this way Spl will contain nan values while in Matlab it inserts inf
            # Todo: If in Matlab some nan would occure this will be the smallest value (v)
            # Todo: In this case the result will differ from python since here i ignore all nan values with nanmin
            SplFunc = interp1d(x=tau2, y=logMLE, fill_value="extrapolate")
            Spl = SplFunc(t) # get y values from fit function
            v = np.nanmin(Spl)

            indMin = np.where(Spl == v)[0][0]
            minTau2 = t[indMin]

            tau3 = np.arange(minTau2-0.1, minTau2+0.11,0.01)
            del logMLE, func, g, ind # clear var before assigning new values
            logMLE = np.zeros(len(tau3))

            for i in range(len(tau3)):

                if tau3[i] > 0:
                    func = np.exp(-ies * dtBin / tau3[i] / 1000)
                    fold = convol(IRF, func)
                    g = fold / np.sum(fold) * N
                    ind = (g>0) & (Data > 0)
                    logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
                else:
                    logMLE[i] = np.inf
            del i

            # spline fit
            t = np.arange(tau3[0], tau3[-1] + ((tau3[-1] - tau3[0]) / 100), (tau3[-1] - tau3[0]) / 100)

            # Todo: I guess this wont resolve the problem since Matlab somehow can handle non finite values in
            # Todo: the spline --> Still wack
            try:
                SplFunc = CubicSpline(x=tau3, y=logMLE) # piecewise cubic polynomial which is twice continuously differentiable
                Spl = SplFunc(t) # get y values from fit function
                v = np.min(Spl)
                indMin = np.where(Spl == v)[0][0]
                trueTau = t[indMin]
            except ValueError:
                trueTau = t[0]


        else:
            trueTau = meanData * dtBin / 1000 - meanIRF
    else:
        trueTau = 0

    return trueTau

@jit(nopython=True)
def convol(irf, x):

    irf = np.array(irf)
    mm = np.mean(irf[-11:])

    '''part from matlab that does not seem required for python
    if size(x,1) == 1 | size(x,2) == 1
        irf = irf(:) 
        x = x(:)'''

    '''if len(x.shape) == 1:
        p = 1
    else:
        p = x.shape[1]'''
    n = len(irf)
    p = len(x)

    # required because matlab gives an error if one would to know dimension of 1D vectore by using
    # x.shape[1] while matlab will return 1 for size(x,2)
    try:
        xSize = x.shape[1]
    except IndexError:
        xSize = 1


    if p>n:
        irf = [irf, mm*np.ones(np.abs(p-n))]
    else:
        irf = irf[0:p]

    y = (np.fft.ifft((np.fft.fft(irf) * np.ones([xSize,xSize])) * np.fft.fft(x))).real[0]

    t = (((np.arange(n) % p) + p) % p)

    y = y[t]

    return y

@jit(nopython=True)
def KDE(T1, arrT2, tau):
    expFrac = (np.abs(arrT2-T1) / tau)

    return np.sum(np.exp(-expFrac[expFrac<=5]))


@jit(nopython=True)
def nbKDE(T1, arrT1, tau):
    expFrac = (np.abs(arrT1-T1) / tau)

    return ((1+2/np.array(len(arrT1))) * (np.sum(np.exp(-expFrac[expFrac<=5]))-1))


@jit(nopython=True)
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


@jit(nopython=True)
def Alex_2CDE(tAex, tDex, tau):

    KDE_DexiAlex = np.zeros(len(tDex))
    KDE_DexiDex =  np.zeros(len(tDex))

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

@jit(nopython=True)
def burstLoc(Arr, minDistace):
    '''
    Clone of the matlab burstLoc function from ?Andreas?

    Args:
        Arr: Array of positions
        minDistace: minimume distance (int)
    Returns:
    '''

    Arr = np.append(Arr, Arr[-1])
    bIndex = np.argwhere((Arr[1:] - Arr[0:-1]) >1)+1
    bIndex = np.insert(bIndex, 0, 0, axis=0)
    bLength = np.zeros(len(bIndex))
    bStart = Arr[bIndex]

    for iterator in range(len(bIndex)):
        length = 1
        index = bIndex[iterator]

        while Arr[index+1] == (Arr[index]+1):
            length += 1
            index += 1

        bLength[iterator] = length

    bStartAcc = bStart[0]
    bLengthAcc = bLength[0]

    del iterator

    for iterator in range(1,len(bStart)):

        if (bStart[iterator] - (bStart[iterator-1] + bLength[iterator-1] - 1)) > minDistace:
            bStartAcc = np.append(bStartAcc, bStart[iterator])
            bLengthAcc = np.append(bLengthAcc, bLength[iterator])


    return bStartAcc, bLengthAcc

@jit(nopython=True)
def lee_filter_uniform(img ,filter_ , size=4):
    img_mean = ndimage.mean(img)
    img_sqr_mean = getattr(ndimage,filter_)(img**2,size)
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = variance(img)

    img_weights = img_variance / (img_variance + overall_variance)
    img_output = img_mean + img_weights * (img - img_mean)

    return img_output

@jit(nopython=True)
def fspecial_average(window_size):
    '''
    Clone of matlabs f special function to create a kernel of type average
    Args:
        window_size:
    Returns: Smoothing filter kernel
    '''

    h = np.ones([window_size,window_size],np.float64)/np.prod([window_size,window_size])

    return h

@jit(nopython=True)
def im_filterish_function(I,window_size):
    '''
    Args:
        I: inter photon time (some array :D)
        window_size: int

    Returns: filtered array

    --> Basically it is imfilter with replicate border condition
    '''

    # Todo: The border condition is not 100% same first element differs (actually the second is where it would start in
    # Todo: matlab and the last is missing (second last in matlab)
    means = cv2.filter2D(np.float64(I), -1, fspecial_average(window_size), borderType=cv2.BORDER_REPLICATE)

    return np.append(means[1:],means[0]).T

#@jit(nopython=True)
def leeFilter(I_, window_size):

    # Todo: Direct comparison of matlab and python output
    '''
    Matlab clone of Grzegorz Mianowski
    https://de.mathworks.com/matlabcentral/fileexchange/28046-lee-filter

    Args:
        I:
        window_size:

    Returns:

    '''

    I_ = np.float64(I_)
    OIm = copy.deepcopy(I_)
    means_ = im_filterish_function(I_, window_size)
    sigmas = np.sqrt((I_ - means_)**2 / window_size**2)
    sigmas = im_filterish_function(sigmas, window_size)

    ENLs = (means_/sigmas)**2
    sx2s = ((ENLs * sigmas **2) - means_**2) / (ENLs +1)
    # at this point the last three elements are "wrong" compare to matlab due to mismatching boundaries
    # in fbar only last element is wrong
    fbar = means_ + (sx2s * (I_-means_) / (sx2s + (means_**2 / ENLs)))

    OIm[means_ != 0] = fbar[fbar != 0]

    return OIm

#@jit(nopython=True)
def read_ht3_raw(inputfile, all_out=True):

    global oflcorrection
    global version
    global isT2
    global globRes

    isT2 = False
    version = 2
    oflcorrection = 0


    SyncRate=25000000
    syncperiod = 1E9/SyncRate
    globRes = 16

    T3WRAPAROUND=1024

    dlen = 0
    #outputfile.write("\n-----------------------\n")
    #outputfile.write("HydraHarp V1 T3 data\n")
    #outputfile.write("\nrecord# chan   nsync truetime/ns dtime\n")

    file = open(inputfile, 'rb')
    data = np.fromfile(file, dtype='<u4')
    file.close()
    RawData = []


    for recNum, element in enumerate(data):

        recordData = "{0:0{1}b}".format(element, 32)


        special = int(recordData[0:1], base=2)
        channel = int(recordData[1:7], base=2)
        dtime = int(recordData[7:22], base=2)
        nsync = int(recordData[22:32], base=2)
        if special == 1:
            if channel == 0x3F: # Overflow
                # Number of overflows in nsync. If 0 or old version, it's an
                # old style single overflow
                if nsync == 0 or version == 1:
                    oflcorrection += T3WRAPAROUND
                    #gotOverflow(1, recNum)
                else:
                    oflcorrection += T3WRAPAROUND * nsync
                    #gotOverflow(nsync, recNum)
            if channel >= 1 and channel <= 15: # markers
                truensync = oflcorrection + nsync
                #gotMarker(truensync, channel, recNum)
        else: # regular input channel
            truensync = oflcorrection + nsync
            #gotPhoton(truensync, channel, dtime, recNum)
            truetime = truensync*syncperiod
            RawData.append([channel+1,dtime,truetime])

    RawData = np.array(RawData)

    if all_out:
        measT = np.floor((RawData[-1][2]-RawData[0][2])*1e-6)
        edges = np.arange(0,measT,1)
        coarseMacro = np.floor(RawData[:,2]*1e-6)
        RawInt = histc(coarseMacro, edges)

        return {'RawData':RawData, 'RawInt':RawInt, 'SyncRate':SyncRate, 'varout4':16}
    else:
        return RawData


@jit(nopython=True)
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


#@jit(nopython=False)
def NgetBurstAll(filename, pathname, suffix, lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, IRF_G,
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

        #del Photons_Raw

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
        #with Path(fileB).open('ab') as f:
        #    np.save(f, BurstData, allow_pickle=True)
        #    print(f'Saved to: {fileB}')



        if boolPostA:
            # save data to file
            # Major compatibility can occure because Matlap -> Column Major and Python -> Row Major
            # https://scottstaniewicz.com/articles/python-matlab-binary/ --> For Matlab python comparison
            fileP = pathname + '/' + 'PData' + str(suffix)+'.bin'

            # append to the single file
            # https://stackoverflow.com/questions/30376581/save-numpy-array-in-append-mode

            #print(accBursts)
            #print('Save PData to: ', fileP)
            #with Path(fileP).open('ab') as f:
            #    np.save(f, accBursts, allow_pickle=True)

        return BurstData

    return []


if __name__ == '__main__':
    print('Main run getBurstAll.py')

