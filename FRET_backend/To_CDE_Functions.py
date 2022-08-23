import numpy as np

def KDE(T1, arrT2, tau):
    expFrac = (np.abs(arrT2-T1) / tau)

    return np.sum(np.exp(-expFrac[expFrac<=5]))

def nbKDE(T1, arrT1, tau):
    expFrac = (np.abs(arrT1-T1) / tau)

    return ((1+2/np.array(len(arrT1))) * (np.sum(np.exp(-expFrac[expFrac<=5]))-1))

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

if __name__ == '__main__':
    print('In main')
