import numpy as np
from datetime import datetime, timedelta
import struct

def read_hhd(location):
    
    inputfile = location
    # inputfile = "/Users/bcudevs/Python Scripts/20190409_BertaIRF/IRF_L530_Reflection_Berta.hhd"    
    RHHD = []    
        
        
    data = open(inputfile,'rb')    
    # print(data.read(16).decode())    
    # print(data.read(6).decode()) # Ident    
    # print(data.read(6).decode()) # FormatVersion    
        
    print('\n=========================================================================== \n')    
    print('  Content of {} : \n'.format(inputfile))    
    print('=========================================================================== \n')    
    print('\n')    
        ##################################################################################
        #
        
    # ASCII file header    #
        ##################################################################################
        
        
    Ident = data.read(16).decode()    
    print('               Ident: {}\n'.format(Ident))    
        
    FormatVersion = data.read(6).decode().strip()    
    print('      Format version: {}\n'.format(FormatVersion))    
        
    # if not(strcmp(FormatVersion,'2.0'))    
    #     fprintf(1,'\n\n      Warning: This program is for version 2.0 only. Aborted.');    
    #     STOP;    
    # end;    
        
    CreatorName = data.read(18).decode()    
    print('        Creator name: {}\n'.format(CreatorName))    
        
    CreatorVersion = data.read(12).decode()    
    print('     Creator version: {}\n'.format(CreatorVersion))    
        
    FileTime = data.read(18).decode()    
    print('    Time of creation: {}\n'.format(FileTime))    
        
    CRLF = data.read(2).decode()    
        
    Comment = data.read(256).decode()    
    print('             Comment: {}\n'.format(Comment))    
        ##################################################################################
        #
        
    # Binary file header    #
        ##################################################################################
        
        
    NumberOfCurves,  = struct.unpack('i', data.read(4))    
    print('    Number of Curves: {}\n'.format(NumberOfCurves))    
        
    BitsPerRecord, = struct.unpack('i', data.read(4))    
    print('       Bits / Record: {}\n'.format(BitsPerRecord))    
        
    ActiveCurve, = struct.unpack('i', data.read(4))    
    print('        Active Curve: {}\n'.format(ActiveCurve))    
        
    MeasurementMode, = struct.unpack('i', data.read(4))    
    print('    Measurement Mode: {}\n'.format(MeasurementMode))    
        
    SubMode, = struct.unpack('i', data.read(4))    
    print('            Sub-Mode: {}\n'.format(SubMode))    
        
    Binning, = struct.unpack('i', data.read(4))    
    print('             Binning: {}\n'.format(Binning))    
        
    Resolution, = struct.unpack('d', data.read(8))    
    print('          Resolution: {}\n'.format(Resolution))    
        
    Offset, = struct.unpack('i', data.read(4))    
    print('              Offset: {}\n'.format(Offset))    
        
    Tacq, = struct.unpack('i', data.read(4))    
    print('    Acquisition Time: {} ms \n'.format(Tacq))    
        
    StopAt, = struct.unpack('I', data.read(4))    
    print('             Stop At: {} counts \n'.format(StopAt))    
        
    StopOnOvfl, = struct.unpack('i', data.read(4))    
    print('    Stop on Overflow: {}\n'.format(StopOnOvfl))    
        
    Restart, = struct.unpack('i', data.read(4))    
    print('             Restart: {}\n'.format(Restart))    
        
    DispLinLog, = struct.unpack('i', data.read(4))    
    print('     Display Lin/Log: {}\n'.format(DispLinLog))    
        
    DispTimeAxisFrom, = struct.unpack('I', data.read(4))    
    print('      Time Axis From: {} ns \n'.format(DispTimeAxisFrom))    
        
    DispTimeAxisTo, = struct.unpack('I', data.read(4))    
    print('        Time Axis To: {} ns \n'.format(DispTimeAxisTo))    
        
    DispCountAxisFrom, = struct.unpack('I', data.read(4))    
    print('     Count Axis From: {}\n'.format(DispCountAxisFrom))    
        
    DispCountAxisTo, = struct.unpack('I', data.read(4))    
    print('       Count Axis To: {}\n'.format(DispCountAxisTo))    
        
        
    DispCurveMapTo = np.zeros(8)    
    DispCurveShow = np.zeros(8)    
    ParamStart = np.zeros(3)    
    ParamStep = np.zeros(3)    
    ParamEnd = np.zeros(3)    
        
    for i in np.arange(8):    
        DispCurveMapTo[i] = (struct.unpack('i', data.read(4))[0])
        DispCurveShow[i] = (struct.unpack('i', data.read(4))[0])
        print('-------------------------------------\n')    
        print('    Curve No.{}\n'.format(i))
        print('               MapTo: {}\n'.format(DispCurveMapTo[i]))
        if (DispCurveShow[i] != 0):
            print('                Show: true\n')
        else:    
            print('                Show: false\n')    
        
        
    for i in np.arange(3):    
        ParamStart[i] = (struct.unpack('f', data.read(4))[0])
        ParamStep[i] = (struct.unpack('f', data.read(4))[0])
        ParamEnd[i] = (struct.unpack('f', data.read(4))[0])
        print('-------------------------------------\n')    
        print('Parameter No.{}\n'.format(i))
        print('               Start: {}\n'.format(ParamStart[i]))
        print('                Step: {}\n'.format(ParamStep[i]))
        print('                 End: {}\n'.format(ParamEnd[i]))    
    print('-------------------------------------\n')    
        
    RepeatMode, = (struct.unpack('i', data.read(4)))    
    print('         Repeat Mode: {}\n'.format(RepeatMode))    
        
    RepeatsPerCurve, = (struct.unpack('i', data.read(4)))    
    print('      Repeat / Curve: {}\n'.format(RepeatsPerCurve))    
        
    RepeatTime, = (struct.unpack('i', data.read(4)))    
    print('         Repeat Time: {}\n'.format(RepeatTime))    
        
    RepeatWaitTime, = (struct.unpack('i', data.read(4)))    
    print('    Repeat Wait Time: {}\n'.format(RepeatWaitTime))    
        
    ScriptName = data.read(20).decode()    
    print('         Script Name: {}\n'.format(ScriptName))    
        
    # %    
    # %          Hardware information header     
    # %    
        
    print('-------------------------------------\n')    
        
    HardwareIdent = data.read(16).decode()    
    print(' Hardware Identifier: {}\n'.format(HardwareIdent))    
        
    HardwarePartNo = data.read(8).decode()    
    print('Hardware Part Number: {}\n'.format(HardwarePartNo))    
        
    HardwareSerial, = (struct.unpack('i', data.read(4)))    
    print('    HW Serial Number: {}\n'.format(HardwareSerial))    
        
    nModulesPresent, = (struct.unpack('i', data.read(4)))    
    print('     Modules present: {}\n'.format(nModulesPresent))    
        
    ModelCode = np.zeros(10)    
    VersionCode = np.zeros(10)    
    for i in np.arange(10):
            ModelCode[i], = (struct.unpack('i', data.read(4)))   
            VersionCode[i], = (struct.unpack('i', data.read(4)))    
        
        
    for i in np.arange(nModulesPresent):    
        print(f'      ModuleInfo[{i:02d}]: {ModelCode[i]} {VersionCode[i]}\n')    
        
    BaseResolution, = (struct.unpack('d', data.read(8)))      
    print('      BaseResolution: {}\n'.format(BaseResolution))    
        
    InputsEnabled, = (struct.unpack('Q', data.read(8)))      
    print('      Inputs Enabled: {}\n'.format(InputsEnabled))    
        
    InpChansPresent,  = (struct.unpack('i', data.read(4)))    
    print(' Input Chan. Present: {}\n'.format(InpChansPresent))    
        
    RefClockSource,  = (struct.unpack('i', data.read(4)))    
    print('      RefClockSource: {}\n'.format(RefClockSource))    
        
    ExtDevices,  = (struct.unpack('i', data.read(4)))    
    print('    External Devices: {}\n'.format(ExtDevices))    
        
    MarkerSettings,  = (struct.unpack('i', data.read(4)))    
    print('     Marker Settings: {}\n'.format(MarkerSettings))    
        
        
    SyncDivider, = (struct.unpack('i', data.read(4)))    
    print('        Sync divider: {} \n'.format(SyncDivider))    
        
    SyncCFDLevel, = (struct.unpack('i', data.read(4)))    
    print('      Sync CFD Level: {} mV\n'.format(SyncCFDLevel))    
        
    SyncCFDZeroCross, = (struct.unpack('i', data.read(4)))    
    print('  Sync CFD ZeroCross: {} mV\n'.format(SyncCFDZeroCross))    
        
    SyncOffset, = (struct.unpack('i', data.read(4)))    
    print('         Sync Offset: {}\n'.format(SyncOffset))    
        
    # %    
    # %          Channels' information header     
    # %    
        
    InputModuleIndex = np.zeros(InpChansPresent)    
    InputCFDLevel = np.zeros(InpChansPresent)    
    InputCFDZeroCross = np.zeros(InpChansPresent)    
    InputOffset = np.zeros(InpChansPresent)    
        
    for i in np.arange(InpChansPresent):    
        InputModuleIndex[i] = (struct.unpack('i', data.read(4)))[0]    
        InputCFDLevel[i] = (struct.unpack('i', data.read(4)))[0]
        InputCFDZeroCross[i] = (struct.unpack('i', data.read(4)))[0]
        InputOffset[i] = (struct.unpack('i', data.read(4)))[0]    
        
        print('-------------------------------------\n')    
        print('Input Channel No. {}\n'.format(i))
        print('  Input Module Index: {}\n'.format(InputModuleIndex[i]))    
        print('     Input CFD Level: {} mV\n'.format(InputCFDLevel[i]))
        print(' Input CFD ZeroCross: {} mV\n'.format(InputCFDZeroCross[i]))
        print('        Input Offset: {}\n'.format(InputOffset[i]))    
        
    # %    
    # %                Headers for each histogram (curve)    
    # %    
        
    CurveIndex = np.zeros(NumberOfCurves)    
    TimeOfRecording = np.zeros(NumberOfCurves)    
    HardwareIdent = []    
    HardwarePartNo = []    
    HardwareSerial = np.zeros(NumberOfCurves)    
    nModulesPresent = np.zeros(NumberOfCurves)    
    ModelCode = np.zeros([NumberOfCurves, 10])    
    VersionCode = np.zeros([NumberOfCurves, 10])    
    BaseResolution = np.zeros(NumberOfCurves)    
    InputsEnabled = np.zeros(NumberOfCurves)    
    InpChansPresent = np.zeros(NumberOfCurves)    
    RefClockSource = np.zeros(NumberOfCurves)    
    ExtDevices = np.zeros(NumberOfCurves)    
    MarkerSettings = np.zeros(NumberOfCurves)    
    SyncDivider = np.zeros(NumberOfCurves)    
    SyncCFDLevel = np.zeros(NumberOfCurves)    
    SyncCFDZeroCross = np.zeros(NumberOfCurves)    
    SyncOffset = np.zeros(NumberOfCurves)    
    InputModuleIndex = np.zeros(NumberOfCurves)    
    InputCFDLevel = np.zeros(NumberOfCurves)    
    InputCFDZeroCross = np.zeros(NumberOfCurves)    
    InputOffset = np.zeros(NumberOfCurves)    
    InpChannel = np.zeros(NumberOfCurves)    
    MeasurementMode = np.zeros(NumberOfCurves)    
    SubMode = np.zeros(NumberOfCurves)    
    Binning = np.zeros(NumberOfCurves)    
    Resolution = np.zeros(NumberOfCurves)    
    Offset = np.zeros(NumberOfCurves)    
    Tacq = np.zeros(NumberOfCurves)    
    StopAfter = np.zeros(NumberOfCurves)    
    StopReason = np.zeros(NumberOfCurves)    
    P1 = np.zeros(NumberOfCurves)    
    P2 = np.zeros(NumberOfCurves)    
    P3 = np.zeros(NumberOfCurves)    
    SyncRate = np.zeros(NumberOfCurves)    
    InputRate = np.zeros(NumberOfCurves)    
    HistCountRate = np.zeros(NumberOfCurves)    
    IntegralCount = np.zeros(NumberOfCurves)    
    HistogramBins = np.zeros(NumberOfCurves)    
    DataOffset = np.zeros(NumberOfCurves)    
        
    for i in np.arange(NumberOfCurves):    
        
        print('-------------------------------------\n')       
        
        CurveIndex[i] = (struct.unpack('i', data.read(4)))[0]
        print('         Curve Index: {}\n'.format(CurveIndex[i]))    
        
        TimeOfRecording[i] = (struct.unpack('I', data.read(4)))[0]    
        
    #  The HydraHarp software saves the time of recording    
    #  as time_t. This equals the number of seconds elapsed    
    #  since 00:00:00 UTC, January 1, 1970.    
    #  MATLAB datenums are in days since January 1, 0000.    
    #  The offset is: datenum(1970,1,1) =  719529    
    #  1 day = 86400 seconds    
        
        
        TimeOfRecording[i] =  TimeOfRecording[i]/86400 + 719529    
        # print((datetime.fromordinal(int(TimeOfRecording[i]))+ timedelta(days=TimeOfRecording[i]%1) - timedelta(days = 366)).strftime('%d-%m-%Y %H:%M:%S'))
        print('   Time of Recording: {} \n'.format((datetime.fromordinal(int(TimeOfRecording[i])) + timedelta(days=TimeOfRecording[i]%1) - timedelta(days = 366)).strftime('%d-%m-%Y %H:%M:%S')))    
        
        HardwareIdent.append(data.read(16).decode())    
        print(' Hardware Identifier: {}\n'.format(HardwareIdent[i]))    
        
        HardwarePartNo.append(data.read(8).decode())    
        print('Hardware Part Number: {}\n'.format(HardwarePartNo[i]))        
        
        HardwareSerial[i] = (struct.unpack('i', data.read(4)))[0]
        print('    HW Serial Number: {}\n'.format(HardwareSerial[i]))    
        
        nModulesPresent[i] = (struct.unpack('i', data.read(4)))[0]
        print('     Modules present: {}\n'.format(nModulesPresent[i]))    
        
        for j in np.arange(10):  # up to 10 modules can exist; we do not print this info    
            ModelCode[i,j] = (struct.unpack('i', data.read(4)))[0]
            VersionCode[i,j] = (struct.unpack('i', data.read(4)))[0]    
        
        BaseResolution[i] = (struct.unpack('d', data.read(8)))[0]
        print('      BaseResolution: {}\n'.format(BaseResolution[i]))    
        
        InputsEnabled[i] = (struct.unpack('Q', data.read(8)))[0]
        print('      Inputs Enabled: {}\n'.format(InputsEnabled[i])) #actually a bitfield    
        
        InpChansPresent[i]  = (struct.unpack('i', data.read(4)))[0]
        print(' Input Chan. Present: {}\n'.format(InpChansPresent[i])) #this determines the number of ChannelHeaders below!    
        
        RefClockSource[i]  = (struct.unpack('i', data.read(4)))[0]
        print('      RefClockSource: {}\n'.format(RefClockSource[i]))    
        
        ExtDevices[i]  = (struct.unpack('i', data.read(4)))[0]
        print('    External Devices: {}\n'.format(ExtDevices[i])) #actually a bitfield    
        
        MarkerSettings[i]  = (struct.unpack('i', data.read(4)))[0]
        print('     Marker Settings: {}\n'.format(MarkerSettings[i])) #actually a bitfield    
        
        SyncDivider[i] = (struct.unpack('i', data.read(4)))[0]
        print('        Sync divider: {} \n'.format(SyncDivider[i]))    
        
        SyncCFDLevel[i] = (struct.unpack('i', data.read(4)))[0]
        print('      Sync CFD Level: {} mV\n'.format(SyncCFDLevel[i]))    
        
        SyncCFDZeroCross[i] = (struct.unpack('i', data.read(4)))[0]
        print('  Sync CFD ZeroCross: {} mV\n'.format(SyncCFDZeroCross[i]))    
        
        SyncOffset[i] = (struct.unpack('i', data.read(4)))[0]
        print('         Sync Offset: {}\n'.format(SyncOffset[i]))    
        
        InputModuleIndex[i] = (struct.unpack('i', data.read(4)))[0] # in which module was this channel, only for troubleshooting   
        print('  Input Module Index: {}\n'.format(InputModuleIndex[i]))    
        
        InputCFDLevel[i] = (struct.unpack('i', data.read(4)))[0]
        print('     Input CFD Level: {} mV\n'.format(InputCFDLevel[i]))    
        
        InputCFDZeroCross[i] = (struct.unpack('i', data.read(4)))[0]
        print(' Input CFD ZeroCross: {} mV\n'.format(InputCFDZeroCross[i]))    
        
        InputOffset[i] = (struct.unpack('i', data.read(4)))[0]
        print('        Input Offset: {}\n'.format(InputOffset[i]))    
        
        InpChannel[i]  = (struct.unpack('i', data.read(4)))[0]
        print('       Input Channel: {}\n'.format(InpChannel[i]))    
        
        MeasurementMode[i] = (struct.unpack('i', data.read(4)))[0]
        print('    Measurement Mode: {}\n'.format(MeasurementMode[i]))    
        
        SubMode[i] = (struct.unpack('i', data.read(4)))[0]
        print('            Sub-Mode: {}\n'.format(SubMode[i]))    
        
        Binning[i] = (struct.unpack('i', data.read(4)))[0]
        print('             Binning: {}\n'.format(Binning[i]))    
        
        Resolution[i] = (struct.unpack('d', data.read(8)))[0]
        print('          Resolution: {}\n'.format(Resolution[i]))    
        
        Offset[i] = (struct.unpack('i', data.read(4)))[0]
        print('              Offset: {}\n'.format(Offset[i]))    
        
        Tacq[i] = (struct.unpack('i', data.read(4)))[0]
        print('    Acquisition Time: {} ms \n'.format(Tacq[i]))    
        
        StopAfter[i] = (struct.unpack('i', data.read(4)))[0]
        print('          Stop After: {} ms \n'.format(StopAfter[i]))    
        
        StopReason[i] = (struct.unpack('i', data.read(4)))[0]
        print('         Stop Reason: {}\n'.format(StopReason[i]))    
        
        P1[i] = (struct.unpack('f', data.read(4)))[0]  # Wavelength in case of TRES
        print('              Par. 1: {}\n'.format(P1[i]))
        P2[i] = (struct.unpack('f', data.read(4)))[0]
        print('              Par. 2: {}\n'.format(P2[i]))
        P3[i] = (struct.unpack('f', data.read(4)))[0]
        print('              Par. 3: {}\n'.format(P3[i]))    
        
        SyncRate[i] = (struct.unpack('i', data.read(4)))[0]
        print('           Sync Rate: {} Hz\n'.format(SyncRate[i]))    
        
        InputRate[i] = (struct.unpack('i', data.read(4)))[0]
        print('        Input Rate 1: {} Hz\n'.format(InputRate[i]))    
        
        HistCountRate[i] = (struct.unpack('i', data.read(4)))[0]
        print('    Hist. Count Rate: {} cps\n'.format(HistCountRate[i]))    
        
        IntegralCount[i] = (struct.unpack('q', data.read(8)))[0]
        print('      Integral Count: {}\n'.format(IntegralCount[i]))    
        
        HistogramBins[i] = (struct.unpack('i', data.read(4)))[0]
        print('      Histogram Bins: {}\n'.format(HistogramBins[i]))    
        
        DataOffset[i] = (struct.unpack('i', data.read(4)))[0]
        print('         Data Offset: {}\n'.format(DataOffset[i]))    
        
        ##################################################################################
        #
        
    #          Reads all histograms into one matrix    #
        ##################################################################################
        
        
    Counts = []    
    Peak = np.zeros(NumberOfCurves)    
    BinRes = np.zeros(NumberOfCurves)    
        
    for i in np.arange(NumberOfCurves):
            data.seek(int(DataOffset[i]))    
        # fseek(fid,DataOffset(i),'bof');
            Counts.append(np.fromfile(data, dtype='uint32', count=int(HistogramBins[i])))    
        # Counts[i] = int.from_bytes(data.read(int(HistogramBins[i])), 'big', signed=False)
            Peak[i]=max(Counts[i])    
        ##################################################################################
        #
        
    #          Summary    #
        ##################################################################################
        
        
    print('\n')    
    print('\n')    
    print('=====================================================\n')    
    print('                     SUMMARY                         \n')    
    print('=====================================================\n')    
    print(' Curve      ps      Histogram      Peak     Integral \n')    
    print(' index     res        bins         count     count   \n')    
    print('=====================================================\n')    
        
    for i in np.arange(NumberOfCurves):    
        print('  {}      {}      {}      {}    {}\n'.format(CurveIndex[i],Resolution[i], HistogramBins[i], Peak[i], IntegralCount[i]))    
        ##################################################################################
        #
        
    #          This is a simple display of the histogram(s)    #
        ##################################################################################
        
        
    data.close()    
        
    BinRes=Resolution[i]    
        
    RHHD.append(Counts)    
    RHHD.append(BinRes)

    return RHHD

if __name__ == '__main__':
    # debug imports
    import scipy.io as sio
    from read_ht3_vect import read_ht3_raw, histc

    # recreate steps till get burst all

    # statics

    ht3file = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/Sample_Data/typical_96well_data/A11/A11_0.ht3'

    Data = read_ht3_raw(ht3file)
    RawData = Data['RawData']
    RawInt = Data['RawInt']
    repRate = Data['SyncRate']
    dtBin = Data['varout4']
    BinSize = 1

    edges2 = np.arange(0,4096,1)
    hRII=histc(RawData[np.equal(RawData[:,0], 1)][:,1],edges2)[0]
    hRT=histc(RawData[np.equal(RawData[:,0], 3)][:,1],edges2)[0]

    tt=np.arange(1,len(RawInt),1)
    measTime=tt[-1]/1000*BinSize

    numCh=(1e12/repRate/dtBin)
    midCh=(round(numCh/2))


    rhhd_file = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/Sample_Data/IRF_L640_ATTO655_KI.hhd'
    RHHD_R = read_hhd(rhhd_file)

    IRF_AllR = RHHD_R[0]
    IRF_R = IRF_AllR[0] + IRF_AllR[2]
    IRF_R = IRF_R - np.mean(IRF_R[int(midCh) - 501:int(midCh) - 100])

    maxhR = np.max(np.max([hRII, hRT]))
    normIRF_R = IRF_R / max(IRF_R) * maxhR

    Brd_RR = [1240,2452]
    newIRF_R = IRF_R[Brd_RR[0]-1:Brd_RR[1]]


    meanIRFR = (np.sum(np.arange(1,len(newIRF_R)+1,1) * newIRF_R) / np.sum(newIRF_R) +
                Brd_RR[0]) * dtBin/1000

    # get matlab stuff for comparison

    # get function inputs from matlab file
    inputs_path = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/Sample_Data/Bat_Test/matlab_ws_latest.mat'
    inputs = sio.loadmat(inputs_path)
    inputs.pop('__header__')
    inputs.pop('__version__')
    inputs.pop('__globals__')

    # dont want to assign to workspace
    # inputs is a dict and i can use var names as inputs (lol) for it
    '''for key, val in inputs.items():
        if len(inputs[key]) == 1:
            exec(key + '=val[0]')
        else:
            exec(key + '=val')'''


