import numpy as np
import os
import struct

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

def read_ht3_header(file_path, all_out=True):
    input_file = open(file_path, 'rb')

    ####### ASCII file header ########

    Ident = input_file.read(16).decode("utf-8").strip('\0')

    FormatVersion = input_file.read(6).decode("utf-8").strip('\0')

    # not sure what this is
    CreatorName = input_file.read(18).decode("utf-8").strip('\0')

    # not sure what this is
    CreatorVersion = input_file.read(12).decode("utf-8").strip('\0')

    FileTime = input_file.read(18).decode("utf-8").strip('\0')

    # jump to next line
    #next(input_file)

    CRLF = input_file.read(2).decode("utf-8").strip('\0')

    Comment = input_file.read(256).decode("utf-8").strip('\0')


    ####### Binary file header ########

    NumberOfCurves, = struct.unpack('i', input_file.read(4))

    BitsPerRecord, = struct.unpack('i', input_file.read(4))

    ActiveCurve, = struct.unpack('i', input_file.read(4))

    MeasurementMode, = struct.unpack('i', input_file.read(4))

    SubMode, = struct.unpack('i', input_file.read(4))

    Binning, = struct.unpack('i', input_file.read(4))

    Resolution, = struct.unpack('d', input_file.read(8))

    Offset, = struct.unpack('i', input_file.read(4))

    Tacq, = struct.unpack('i', input_file.read(4))

    StopAt, = struct.unpack('I', input_file.read(4))

    StopOnOvfl, = struct.unpack('i', input_file.read(4))

    Restart, = struct.unpack('i', input_file.read(4))

    DispLinLog, = struct.unpack('i', input_file.read(4))

    DispTimeAxisFrom, = struct.unpack('I', input_file.read(4))

    DispTimeAxisTo, = struct.unpack('I', input_file.read(4))

    DispCountAxisFrom, = struct.unpack('I', input_file.read(4))

    DispCountAxisTo, = struct.unpack('I', input_file.read(4))

    DispCurveMapTo = np.zeros(8)
    DispCurveShow = np.zeros(8)
    ParamStart = np.zeros(3)
    ParamStep = np.zeros(3)
    ParamEnd = np.zeros(3)

    for i in np.arange(8):
        DispCurveMapTo[i] = (struct.unpack('i', input_file.read(4))[0])
        DispCurveShow[i] = (struct.unpack('i', input_file.read(4))[0])

    for i in np.arange(3):
        ParamStart[i] = (struct.unpack('f', input_file.read(4))[0])
        ParamStep[i] = (struct.unpack('f', input_file.read(4))[0])
        ParamEnd[i] = (struct.unpack('f', input_file.read(4))[0])

    RepeatMode, = (struct.unpack('i', input_file.read(4)))

    RepeatsPerCurve, = (struct.unpack('i', input_file.read(4)))

    RepeatTime, = (struct.unpack('i', input_file.read(4)))

    RepeatWaitTime, = (struct.unpack('i', input_file.read(4)))

    ScriptName = input_file.read(20).decode()


    ####### Hardware information header ########

    HardwareIdent = input_file.read(16).decode()

    HardwarePartNo = input_file.read(8).decode()

    HardwareSerial, = (struct.unpack('i', input_file.read(4)))

    nModulesPresent, = (struct.unpack('i', input_file.read(4)))

    ModelCode = np.zeros(10)
    VersionCode = np.zeros(10)
    for i in np.arange(10):
        ModelCode[i], = (struct.unpack('i', input_file.read(4)))
        VersionCode[i], = (struct.unpack('i', input_file.read(4)))


    BaseResolution, = (struct.unpack('d', input_file.read(8)))

    InputsEnabled, = (struct.unpack('Q', input_file.read(8)))

    InpChansPresent, = (struct.unpack('i', input_file.read(4)))

    RefClockSource, = (struct.unpack('i', input_file.read(4)))

    ExtDevices, = (struct.unpack('i', input_file.read(4)))

    MarkerSettings, = (struct.unpack('i', input_file.read(4)))

    SyncDivider, = (struct.unpack('i', input_file.read(4)))

    SyncCFDLevel, = (struct.unpack('i', input_file.read(4)))

    SyncCFDZeroCross, = (struct.unpack('i', input_file.read(4)))

    SyncOffset, = (struct.unpack('i', input_file.read(4)))

    ####### Channels information header ########

    InputModuleIndex = np.zeros(InpChansPresent)
    InputCFDLevel = np.zeros(InpChansPresent)
    InputCFDZeroCross = np.zeros(InpChansPresent)
    InputOffset = np.zeros(InpChansPresent)

    for i in np.arange(InpChansPresent):
        InputModuleIndex[i] = (struct.unpack('i', input_file.read(4)))[0]
        InputCFDLevel[i] = (struct.unpack('i', input_file.read(4)))[0]
        InputCFDZeroCross[i] = (struct.unpack('i', input_file.read(4)))[0]
        InputOffset[i] = (struct.unpack('i', input_file.read(4)))[0]


    ####### Time tagging mode specific header ########

    InputRate = np.zeros(InpChansPresent)

    for i in np.arange(InpChansPresent):
        InputRate[i] = (struct.unpack('i', input_file.read(4)))[0]

    SyncRate = (struct.unpack('i', input_file.read(4)))[0]
    StopAfter = (struct.unpack('i', input_file.read(4)))[0]
    StopReason = (struct.unpack('i', input_file.read(4)))[0]
    ImgHdrSize = (struct.unpack('i', input_file.read(4)))[0]
    nRecords = (struct.unpack('i', input_file.read(4)))[0]


    ####### Special imaging header ########

    #ImgHdr = (struct.unpack('i', input_file.read(ImgHdrSize)))[0]


    ####### Read data ########

    #print(f'Current pointer position after Header: {input_file.tell()}')

    oflcorrection = 0
    syncperiod = 1E9 / SyncRate
    globRes = 16

    T3WRAPAROUND = 1024

    data = np.fromfile(input_file, dtype='<u4')

    RawData = []

    for recNum, element in enumerate(data):

        recordData = "{0:0{1}b}".format(element, 32)

        special = int(recordData[0:1], base=2)
        channel = int(recordData[1:7], base=2)
        dtime = int(recordData[7:22], base=2)
        nsync = int(recordData[22:32], base=2)
        if special == 1:
            if channel == 0x3F:  # Overflow
                # Number of overflows in nsync. If 0 or old version, it's an
                # old style single overflow
                if nsync == 0 or FormatVersion.startswith('1'):
                    oflcorrection += T3WRAPAROUND
                    # gotOverflow(1, recNum)
                else:
                    oflcorrection += T3WRAPAROUND * nsync
                    # gotOverflow(nsync, recNum)
            if channel >= 1 and channel <= 15:  # markers
                truensync = oflcorrection + nsync
                # gotMarker(truensync, channel, recNum)
        else:  # regular input channel
            truensync = oflcorrection + nsync
            # gotPhoton(truensync, channel, dtime, recNum)
            truetime = truensync * syncperiod
            RawData.append([channel + 1, dtime, truetime])

    RawData = np.array(RawData)

    RawData = np.array(RawData)

    if all_out:
        measT = np.floor((RawData[-1][2]-RawData[0][2])*1e-6)
        edges = np.arange(0,measT,1)
        coarseMacro = np.floor(RawData[:,2]*1e-6)
        RawInt = histc(coarseMacro, edges)

        return {'RawData':RawData, 'RawInt':RawInt, 'SyncRate':SyncRate, 'varout4':16}
    else:
        return RawData

if __name__ == '__main__':

    # script to test read HT3 files with non-standard (old) pico format without PQTTER beginning

    file_path = '/Users/philipp/Desktop/Work/SchlierfData/HT3_With_Header/default_000.ht3'

    input_file = open(file_path, 'rb')

    ####### ASCII file header ########

    Ident = input_file.read(16).decode("utf-8").strip('\0')

    FormatVersion = input_file.read(6).decode("utf-8").strip('\0')

    # not sure what this is
    CreatorName = input_file.read(18).decode("utf-8").strip('\0')

    # not sure what this is
    CreatorVersion = input_file.read(12).decode("utf-8").strip('\0')

    FileTime = input_file.read(18).decode("utf-8").strip('\0')

    # jump to next line
    #next(input_file)

    CRLF = input_file.read(2).decode("utf-8").strip('\0')

    Comment = input_file.read(256).decode("utf-8").strip('\0')


    ####### Binary file header ########

    NumberOfCurves, = struct.unpack('i', input_file.read(4))

    BitsPerRecord, = struct.unpack('i', input_file.read(4))

    ActiveCurve, = struct.unpack('i', input_file.read(4))

    MeasurementMode, = struct.unpack('i', input_file.read(4))

    SubMode, = struct.unpack('i', input_file.read(4))

    Binning, = struct.unpack('i', input_file.read(4))

    Resolution, = struct.unpack('d', input_file.read(8))

    Offset, = struct.unpack('i', input_file.read(4))

    Tacq, = struct.unpack('i', input_file.read(4))

    StopAt, = struct.unpack('I', input_file.read(4))

    StopOnOvfl, = struct.unpack('i', input_file.read(4))

    Restart, = struct.unpack('i', input_file.read(4))

    DispLinLog, = struct.unpack('i', input_file.read(4))

    DispTimeAxisFrom, = struct.unpack('I', input_file.read(4))

    DispTimeAxisTo, = struct.unpack('I', input_file.read(4))

    DispCountAxisFrom, = struct.unpack('I', input_file.read(4))

    DispCountAxisTo, = struct.unpack('I', input_file.read(4))

    DispCurveMapTo = np.zeros(8)
    DispCurveShow = np.zeros(8)
    ParamStart = np.zeros(3)
    ParamStep = np.zeros(3)
    ParamEnd = np.zeros(3)

    for i in np.arange(8):
        DispCurveMapTo[i] = (struct.unpack('i', input_file.read(4))[0])
        DispCurveShow[i] = (struct.unpack('i', input_file.read(4))[0])

    for i in np.arange(3):
        ParamStart[i] = (struct.unpack('f', input_file.read(4))[0])
        ParamStep[i] = (struct.unpack('f', input_file.read(4))[0])
        ParamEnd[i] = (struct.unpack('f', input_file.read(4))[0])

    RepeatMode, = (struct.unpack('i', input_file.read(4)))

    RepeatsPerCurve, = (struct.unpack('i', input_file.read(4)))

    RepeatTime, = (struct.unpack('i', input_file.read(4)))

    RepeatWaitTime, = (struct.unpack('i', input_file.read(4)))

    ScriptName = input_file.read(20).decode()


    ####### Hardware information header ########

    HardwareIdent = input_file.read(16).decode()

    HardwarePartNo = input_file.read(8).decode()

    HardwareSerial, = (struct.unpack('i', input_file.read(4)))

    nModulesPresent, = (struct.unpack('i', input_file.read(4)))

    ModelCode = np.zeros(10)
    VersionCode = np.zeros(10)
    for i in np.arange(10):
        ModelCode[i], = (struct.unpack('i', input_file.read(4)))
        VersionCode[i], = (struct.unpack('i', input_file.read(4)))


    BaseResolution, = (struct.unpack('d', input_file.read(8)))

    InputsEnabled, = (struct.unpack('Q', input_file.read(8)))

    InpChansPresent, = (struct.unpack('i', input_file.read(4)))

    RefClockSource, = (struct.unpack('i', input_file.read(4)))

    ExtDevices, = (struct.unpack('i', input_file.read(4)))

    MarkerSettings, = (struct.unpack('i', input_file.read(4)))

    SyncDivider, = (struct.unpack('i', input_file.read(4)))

    SyncCFDLevel, = (struct.unpack('i', input_file.read(4)))

    SyncCFDZeroCross, = (struct.unpack('i', input_file.read(4)))

    SyncOffset, = (struct.unpack('i', input_file.read(4)))

    ####### Channels information header ########

    InputModuleIndex = np.zeros(InpChansPresent)
    InputCFDLevel = np.zeros(InpChansPresent)
    InputCFDZeroCross = np.zeros(InpChansPresent)
    InputOffset = np.zeros(InpChansPresent)

    for i in np.arange(InpChansPresent):
        InputModuleIndex[i] = (struct.unpack('i', input_file.read(4)))[0]
        InputCFDLevel[i] = (struct.unpack('i', input_file.read(4)))[0]
        InputCFDZeroCross[i] = (struct.unpack('i', input_file.read(4)))[0]
        InputOffset[i] = (struct.unpack('i', input_file.read(4)))[0]


    ####### Time tagging mode specific header ########

    InputRate = np.zeros(InpChansPresent)

    for i in np.arange(InpChansPresent):
        InputRate[i] = (struct.unpack('i', input_file.read(4)))[0]

    SyncRate = (struct.unpack('i', input_file.read(4)))[0]
    StopAfter = (struct.unpack('i', input_file.read(4)))[0]
    StopReason = (struct.unpack('i', input_file.read(4)))[0]
    ImgHdrSize = (struct.unpack('i', input_file.read(4)))[0]
    nRecords = (struct.unpack('i', input_file.read(4)))[0]


    ####### Special imaging header ########

    #ImgHdr = (struct.unpack('i', input_file.read(ImgHdrSize)))[0]


    ####### Read data ########

    #print(f'Current pointer position after Header: {input_file.tell()}')

    oflcorrection = 0
    syncperiod = 1E9 / SyncRate
    globRes = 16

    T3WRAPAROUND = 1024

    data = np.fromfile(input_file, dtype='<u4')

    RawData = []

    for recNum, element in enumerate(data):

        recordData = "{0:0{1}b}".format(element, 32)

        special = int(recordData[0:1], base=2)
        channel = int(recordData[1:7], base=2)
        dtime = int(recordData[7:22], base=2)
        nsync = int(recordData[22:32], base=2)
        if special == 1:
            if channel == 0x3F:  # Overflow
                # Number of overflows in nsync. If 0 or old version, it's an
                # old style single overflow
                if nsync == 0 or FormatVersion.startswith('1'):
                    oflcorrection += T3WRAPAROUND
                    # gotOverflow(1, recNum)
                else:
                    oflcorrection += T3WRAPAROUND * nsync
                    # gotOverflow(nsync, recNum)
            if channel >= 1 and channel <= 15:  # markers
                truensync = oflcorrection + nsync
                # gotMarker(truensync, channel, recNum)
        else:  # regular input channel
            truensync = oflcorrection + nsync
            # gotPhoton(truensync, channel, dtime, recNum)
            truetime = truensync * syncperiod
            RawData.append([channel + 1, dtime, truetime])

    RawData = np.array(RawData)