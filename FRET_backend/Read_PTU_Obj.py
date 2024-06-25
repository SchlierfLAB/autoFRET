import time
import sys
import struct
import io
import numpy as np


class Read_PTU:
    def __init__(self, inputfilePath):

        self.PTU = False
        self.ht3 = False

        # get file type
        if inputfilePath.endswith('.ptu'):
            self.PTU = True
        elif inputfilePath.endswith('.ht3'):
            self.ht3 = True

        # def output var
        self.RawData = list()

        # open inputfile
        self.inputfile = open(inputfilePath, 'rb')

        # check if ptu
        self.magic = self.inputfile.read(8).decode("utf-8").strip('\0')
        if self.magic != "PQTTTR" and self.PTU:
            print("ERROR: Magic invalid, this is not a PTU or HT3 (with header) file.")
            self.inputfile.close()
            exit(0)



        if self.PTU:
            # get version info
            self.version = self.inputfile.read(8).decode("utf-8").strip('\0')


            # Def some consts
            self.oflcorrection = 0
            self.dlen = 0

            #Todo: Check for errors or if we can get that from header stuff as well
            # Pico seems to handle that differently depending on file formats and header info
            self.SyncRate = 25000000
            self.syncperiod = 1E9 / self.SyncRate


            # Tag Types
            self.tyEmpty8 = struct.unpack(">i", bytes.fromhex("FFFF0008"))[0]
            self.tyBool8 = struct.unpack(">i", bytes.fromhex("00000008"))[0]
            self.tyInt8 = struct.unpack(">i", bytes.fromhex("10000008"))[0]
            self.tyBitSet64 = struct.unpack(">i", bytes.fromhex("11000008"))[0]
            self.tyColor8 = struct.unpack(">i", bytes.fromhex("12000008"))[0]
            self.tyFloat8 = struct.unpack(">i", bytes.fromhex("20000008"))[0]
            self.tyTDateTime = struct.unpack(">i", bytes.fromhex("21000008"))[0]
            self.tyFloat8Array = struct.unpack(">i", bytes.fromhex("2001FFFF"))[0]
            self.tyAnsiString = struct.unpack(">i", bytes.fromhex("4001FFFF"))[0]
            self.tyWideString = struct.unpack(">i", bytes.fromhex("4002FFFF"))[0]
            self. tyBinaryBlob = struct.unpack(">i", bytes.fromhex("FFFFFFFF"))[0]

            # Record types
            self.rtPicoHarp300T3 = struct.unpack(">i", bytes.fromhex('00010303'))[0]
            self.rtPicoHarp300T2 = struct.unpack(">i", bytes.fromhex('00010203'))[0]
            self.rtHydraHarpT3 = struct.unpack(">i", bytes.fromhex('00010304'))[0]
            self.rtHydraHarpT2 = struct.unpack(">i", bytes.fromhex('00010204'))[0]
            self.rtHydraHarp2T3 = struct.unpack(">i", bytes.fromhex('01010304'))[0]
            self.rtHydraHarp2T2 = struct.unpack(">i", bytes.fromhex('01010204'))[0]
            self.rtTimeHarp260NT3 = struct.unpack(">i", bytes.fromhex('00010305'))[0]
            self.rtTimeHarp260NT2 = struct.unpack(">i", bytes.fromhex('00010205'))[0]
            self.rtTimeHarp260PT3 = struct.unpack(">i", bytes.fromhex('00010306'))[0]
            self.rtTimeHarp260PT2 = struct.unpack(">i", bytes.fromhex('00010206'))[0]
            self.rtGenericT3 = struct.unpack(">i", bytes.fromhex('00010307'))[0]  # MultiHarpXXX and PicoHarp330
            self.rtGenericT2 = struct.unpack(">i", bytes.fromhex('00010207'))[0]  # MultiHarpXXX and PicoHarp330

            # get header information

            self.read_PTU_Header()

            # get important variables from headers
            self.numRecords = self.tagValues[self.tagNames.index("TTResult_NumberOfRecords")]
            self.globRes = self.tagValues[self.tagNames.index("MeasDesc_GlobalResolution")]

            self.detect_extract()

        elif self.ht3:

            # decide if file has a header or not
            try:
                input_file = open(inputfilePath, 'rb')
                input_file.read(16).decode("utf-8").strip('\0')
                header = True
                input_file.close()
            except UnicodeError:
                header = False

            if header:
                from FRET_backend.ReadHT3HeaderFiles import read_ht3_header
                self.all_out = read_ht3_header(inputfilePath, True)
                self.RawData = self.all_out['RawData']
            else:
                from FRET_backend.read_ht3_vect import read_ht3_raw
                self.all_out = read_ht3_raw(inputfilePath, True)
                self.RawData = self.all_out['RawData']



    def read_PTU_Header(self):
        # read header
        tagDataList = []
        while True:
            tagIdent = self.inputfile.read(32).decode("utf-8").strip('\0')
            tagIdx = struct.unpack("<i", self.inputfile.read(4))[0]
            tagTyp = struct.unpack("<i", self.inputfile.read(4))[0]
            if tagIdx > -1:
                evalName = tagIdent + '(' + str(tagIdx) + ')'
            else:
                evalName = tagIdent
            if tagTyp == self.tyEmpty8:
                self.inputfile.read(8)
                tagDataList.append((evalName, "<empty Tag>"))
            elif tagTyp == self.tyBool8:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                if tagInt == 0:
                    tagDataList.append((evalName, "False"))
                else:
                    tagDataList.append((evalName, "True"))
            elif tagTyp == self.tyInt8:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyBitSet64:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyColor8:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyFloat8:
                tagFloat = struct.unpack("<d", self.inputfile.read(8))[0]
                tagDataList.append((evalName, tagFloat))
            elif tagTyp == self.tyFloat8Array:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                tagDataList.append((evalName, tagInt))
            elif tagTyp == self.tyTDateTime:
                tagFloat = struct.unpack("<d", self.inputfile.read(8))[0]
                tagTime = int((tagFloat - 25569) * 86400)
                tagTime = time.gmtime(tagTime)
                tagDataList.append((evalName, tagTime))
            elif tagTyp == self.tyAnsiString:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                tagString = self.inputfile.read(tagInt).decode("utf-8").strip("\0")
                tagDataList.append((evalName, tagString))
            elif tagTyp == self.tyWideString:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                tagString = self.inputfile.read(tagInt).decode("utf-16le", errors="ignore").strip("\0")
                tagDataList.append((evalName, tagString))
            elif tagTyp == self.tyBinaryBlob:
                tagInt = struct.unpack("<q", self.inputfile.read(8))[0]
                tagDataList.append((evalName, tagInt))
            else:
                print("ERROR: Unknown tag type")
                # exit(0)
            if tagIdent == "Header_End":
                break

        # Reformat the saved data for easier access
        self.tagNames = [tagDataList[i][0] for i in range(0, len(tagDataList))]
        self.tagValues = [tagDataList[i][1] for i in range(0, len(tagDataList))]



    def readHT3(self, v):
        T3WRAPAROUND = 1024
        for recNum in range(0, self.numRecords):
            try:
                recordData = "{0:0{1}b}".format(struct.unpack("<I", self.inputfile.read(4))[0], 32)
            except:
                print("The file ended earlier than expected, at record %d/%d." \
                      % (recNum, self.numRecords))
                exit(0)

            special = int(recordData[0:1], base=2)
            channel = int(recordData[1:7], base=2)
            dtime = int(recordData[7:22], base=2)
            nsync = int(recordData[22:32], base=2)
            if special == 1:
                if channel == 0x3F:  # Overflow
                    # Number of overflows in nsync. If 0 or old version, it's an
                    # old style single overflow
                    if nsync == 0 or v == 1:
                        self.oflcorrection += T3WRAPAROUND
                        #gotOverflow(1)
                    else:
                        self.oflcorrection += T3WRAPAROUND * nsync
                        #gotOverflow(nsync)
                if channel >= 1 and channel <= 15:  # markers
                    truensync = self.oflcorrection + nsync
                    #gotMarker(truensync, channel)
            else:  # regular input channel
                truensync = self.oflcorrection + nsync
                #gotPhoton(truensync, channel, dtime)
                truetime = truensync * self.syncperiod
                self.RawData.append([channel+1, dtime, truetime])
            if recNum % 100000 == 0:
                sys.stdout.write("\rProgress: %.1f%%" % (float(recNum) * 100 / float(self.numRecords)))
                sys.stdout.flush()

        self.RawData = np.array(self.RawData)

    def readPT2(self):

        T2WRAPAROUND = 210698240
        for recNum in range(0, self.numRecords):
            try:
                recordData = "{0:0{1}b}".format(struct.unpack("<I", self.inputfile.read(4))[0], 32)
            except:
                print("The file ended earlier than expected, at record %d/%d." \
                      % (recNum, self.numRecords))
                exit(0)

            channel = int(recordData[0:4], base=2)
            time = int(recordData[4:32], base=2)
            #Todo: Ok no clue if this is correct or in that case the time is the dtime
            # dtime = int(recordData[7:22], base=2)
            if channel == 0xF:  # Special record
                # lower 4 bits of time are marker bits
                markers = int(recordData[28:32], base=2)
                if markers == 0:  # Not a marker, so overflow
                    #gotOverflow(1)
                    self.oflcorrection += T2WRAPAROUND
                else:
                    # Actually, the lower 4 bits for the time aren't valid because
                    # they belong to the marker. But the error caused by them is
                    # so small that we can just ignore it.
                    truetime = self.oflcorrection + time
                    #gotMarker(truetime, markers)
            else:
                if channel > 4:  # Should not occur
                    print("Illegal Channel: #%1d %1u" % (recNum, channel))
                    #outputfile.write("\nIllegal channel ")
                truetime = self.oflcorrection + time
                #gotPhoton(truetime, channel, time)
                self.RawData.append([channel + 1, time, truetime])
            if recNum % 100000 == 0:
                sys.stdout.write("\rProgress: %.1f%%" % (float(recNum) * 100 / float(self.numRecords)))
                sys.stdout.flush()

        self.RawData = np.array(self.RawData)

    def readPT3(self):

        T3WRAPAROUND = 65536
        for recNum in range(0, self.numRecords):
            # The data is stored in 32 bits that need to be divided into smaller
            # groups of bits, with each group of bits representing a different
            # variable. In this case, channel, dtime and nsync. This can easily be
            # achieved by converting the 32 bits to a string, dividing the groups
            # with simple array slicing, and then converting back into the integers.
            try:
                recordData = "{0:0{1}b}".format(struct.unpack("<I", self.inputfile.read(4))[0], 32)
            except:
                print("The file ended earlier than expected, at record %d/%d." \
                      % (recNum, self.numRecords))
                exit(0)

            channel = int(recordData[0:4], base=2)
            dtime = int(recordData[4:16], base=2)
            nsync = int(recordData[16:32], base=2)
            if channel == 0xF:  # Special record
                if dtime == 0:  # Not a marker, so overflow
                    #gotOverflow(1)
                    self.oflcorrection += T3WRAPAROUND
                else:
                    truensync = self.oflcorrection + nsync
                    #gotMarker(truensync, dtime)
            else:
                if channel == 0 or channel > 4:  # Should not occur
                    print("Illegal Channel: #%1d %1u" % (self.dlen, channel))
                    #outputfile.write("\nIllegal channel ")
                truensync = self.oflcorrection + nsync

                truetime = truensync * self.syncperiod
                #gotPhoton(truensync, channel, dtime)
                self.RawData.append([channel + 1, dtime, truetime])

                self.dlen += 1
            if recNum % 100000 == 0:
                sys.stdout.write("\rProgress: %.1f%%" % (float(recNum) * 100 / float(self.numRecords)))
                sys.stdout.flush()

        self.RawData = np.array(self.RawData)


    def histc(self, Inp, bin):
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
            count[i - 1] += 1
        return [count, bin_map]

    def detect_extract(self):
        # Will detect record type and call correct function (HT3, PT2, PT3)
        recordType = self.tagValues[self.tagNames.index("TTResultFormat_TTTRRecType")]

        if recordType == self.rtPicoHarp300T2:
            self.isT2 = True
            print("PicoHarp 300 T2 data")
            self.readPT2()
        elif recordType == self.rtPicoHarp300T3:
            self.isT2 = False
            print("PicoHarp 300 T3 data")
            self.readPT3()
        elif recordType == self.rtHydraHarpT2:
            self.isT2 = True
            print("HydraHarp V1 T2 data")
            self.readHT2(v=1)
        elif recordType == self.rtHydraHarpT3:
            self.isT2 = False
            print("HydraHarp V1 T3 data")
            self.readHT3(v=1)
        elif recordType == self.rtHydraHarp2T2:
            self.isT2 = True
            print("HydraHarp V2 T2 data")
            self.readHT2(v=2)
        elif recordType == self.rtHydraHarp2T3:
            self.isT2 = False
            print("HydraHarp V2 T3 data")
            self.readHT3(v=2)
        elif recordType == self.rtTimeHarp260NT3:
            self.isT2 = False
            print("TimeHarp260N T3 data")
            self.readHT3(v=2)
        elif recordType == self.rtTimeHarp260NT2:
            self.isT2 = True
            print("TimeHarp260N T2 data")
            self.readHT2(v=2)
        elif recordType == self.rtTimeHarp260PT3:
            self.isT2 = False
            print("TimeHarp260P T3 data")
            self.readHT3(v=2)
        elif recordType == self.rtTimeHarp260PT2:
            self.isT2 = True
            print("TimeHarp260P T2 data")
            self.readHT2(v=2)
        elif recordType == self.rtGenericT3:
            self.isT2 = False
            print("PQ Generic T3 data")
            self.readHT3(v=2)
        elif recordType == self.rtGenericT2:
            self.isT2 = True
            print("PQ Generic T2 data")
            self.readHT2(v=2)
        else:
            print("ERROR: Unknown record type")

    def further_process(self):

        if not self.ht3:
            measT = np.floor((self.RawData[-1][2] - self.RawData[0][2]) * 1e-6)
            edges = np.arange(0, measT, 1)
            coarseMacro = np.floor(self.RawData[:, 2] * 1e-6)
            RawInt = self.histc(coarseMacro, edges)

            self.all_out = {'RawData':self.RawData, 'RawInt':RawInt, 'SyncRate':self.SyncRate, 'varout4':16}



if __name__ == '__main__':
    print('IN Main')
    inputfile_path = '/Users/philipp/Desktop/Work/SchlierfData/HT3_With_Header/default_000.ht3'

    test_read = Read_PTU(inputfile_path)

    RawData = test_read.RawData

    print('\n'*3, RawData)