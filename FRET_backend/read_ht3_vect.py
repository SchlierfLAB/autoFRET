import numpy as np
import io

# Todo: Check wether the output should be generated here or in getBurstAll
#outputfile = io.open("/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/OutputData/"
#                     "BData1.bin", "w+", encoding="utf-16le")
'''isT2 = False
version = 2
oflcorrection = 0'''

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

def count_true(array):
    counter = 0
    for ele in array:
        if ele:
            counter += 1

    print(counter)
    return counter




if __name__ == '__main__':

    inputfile = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/Sample_Data/A08_1.ht3'
    #edges2,hGII,hGT,hRII,hRT,interPhT, numCh, midCh = read_ht3(inputfile=inputfile)
    roiRG = [100,1250]
    roiRO = [1300,2500]
    Photons_Raw = read_ht3_raw(inputfile, False)
    print(Photons_Raw)
    Photons = Photons_Raw[(Photons_Raw[:,0] != 15) & ((Photons_Raw[:,1] >= roiRG[0]) & (Photons_Raw[:,1] <= roiRG[1]) |
                                                      ((Photons_Raw[:,1] >= roiRO[0]) & (Photons_Raw[:,1] <= roiRO[1])))]
