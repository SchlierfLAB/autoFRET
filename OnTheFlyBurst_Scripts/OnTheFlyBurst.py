# 'Main on the fly (OTF) burst'

### Section Imports ###

import pandas as pd
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os, sys, time
import numpy as np
from PyQt5.QtWidgets import QApplication

from FRET_backend.read_hhd import read_hhd
from FRET_backend.getBurstAll import getBurstAll
from FRET_backend.read_ht3_vect import read_ht3_raw
from Select_file_Window import File_DD_Dialog

class OTF_Burst:

    def __init__(self, target_folder, setting_file, first_hhd, second_hhd):

        self.target_folder = target_folder
        self.setting_file = setting_file
        self.first_hhd = first_hhd
        self.second_hhd = second_hhd

        # Todo: dummy vars for range that should be given by the User somehow
        self.roiMLE_G = [12, 1387]
        self.roiMLE_R = [1687, 1913]

        # get settings - no other prerequirements here
        self.import_settings()


        # init first file flag since some info is extracted from just first file
        self.first_file = True

    ### Section for folder tracking and init if file is created ###


    def on_create_ht3_file(self):

        file_dir = os.path.dirname(self.src_path)
        file_name = os.path.basename(self.src_path)

        if self.first_file:

            try:
                Data = read_ht3_raw(file_dir)
                repRate = Data['SyncRate']
                self.dtBin = Data['varout4']

                # clear cash
                del Data

            except (IndexError, FileNotFoundError):
                print('Error no ht3 data given')
                return


            self.hhd_handling(Brd_GGR=self.roiMLE_G, Brd_RR=self.roiMLE_R, repRate=repRate, dtBin=self.dtBin)

            # create running files
            self.check_running_files(folder_path=os.path.dirname(file_dir))

            lastBN = np.load(self.str_path_lastBN)

            # trigger get burst all
            Bursts = getBurstAll(filename=file_name, pathname=os.path.dirname(file_dir), suffix='', lastBN=lastBN, \
                                 roiRG=self.roiMLE_G, roiR0=self.roiMLE_R, threIT=self.threIT  ,threIT2=self.threITN,\
                                 minPhs=self.minPhs, threAveT=10, IRF_G=self.newIRF_G, meanIRFG=self.meanIRFG, \
                                 IRF_R=self.newIRF_R, meanIRFR=self.meanIRFR, roiMLE_G=self.roiMLE_G,\
                                 roiMLE_R=self.roiMLE_R, dtBin=self.dtBin, setLeeFilter=self.setLeeFilter, \
                                 boolFLA=self.boolFLA, gGG=self.gGG, gRR=self.gRR, boolTotal=self.boolTotal, \
                                 minGR=self.minGR, minR0=self.minR0, boolPostA=self.boolPostA, checkInner=False)

            # save lastBN in running file folder wise
            lastBN += len(Bursts)
            np.save(self.str_path_lastBN, lastBN)


            self.first_file = False


        elif self.first_file == False:
            self.check_running_files(file_dir=os.path.dirname(file_dir))
            lastBN = np.load(self.str_path_lastBN)

            Bursts = getBurstAll(filename=file_name, pathname=os.path.dirname(file_dir), suffix='', lastBN=lastBN, \
                                 roiRG=self.roiMLE_G, roiR0=self.roiMLE_R, threIT=self.threIT  ,threIT2=self.threITN,\
                                 minPhs=self.minPhs, threAveT=10, IRF_G=self.newIRF_G, meanIRFG=self.meanIRFG, \
                                 IRF_R=self.newIRF_R, meanIRFR=self.meanIRFR, roiMLE_G=self.roiMLE_G,\
                                 roiMLE_R=self.roiMLE_R, dtBin=self.dtBin, setLeeFilter=self.setLeeFilter, \
                                 boolFLA=self.boolFLA, gGG=self.gGG, gRR=self.gRR, boolTotal=self.boolTotal, \
                                 minGR=self.minGR, minR0=self.minR0, boolPostA=self.boolPostA, checkInner=False)

            # save lastBN in running file folder wise
            lastBN += len(Bursts)
            np.save(self.str_path_lastBN, lastBN)



    def track_ht3_folder(self, dir):

        # function tracking dir in which folders will be created

        # track only ht3 files in the folder
        patterns = ['*.ht3']
        ignore_patterns = None
        ignore_dirs = False
        case_sensitive = True
        event_handler = PatternMatchingEventHandler(None, ignore_patterns, ignore_dirs, case_sensitive, \
                                                    patterns=patterns)

        event_handler.on_created = self.on_create_ht3_file()

        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(event_handler, dir, recursive=go_recursively)

        my_observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()

    ### Section for getting Settings ###

    def import_settings(self):

        if self.setting_file.endswith('.xls'):
            data = pd.read_excel(self.setting_file)
        elif self.setting_file.endswith('.csv'):
            data = pd.read_csv(self.setting_file)
        else:
            print('Settings file has wrong format\nPlease input only .xls or .csv files')

        try:
            self.setLeeFilter = int(data.leeFilterBox)
            self.gGG = float(data.gGGBox)
            self.gRR = float(data.gRRBox)
            self.threIT = float(data.maxInterTime)
            self.threITN = float(data.minInterTimeNoise)
            self.minPhs = int(data.minTotal)
            self.minGR = int(data.grBox)
            self.minR0 = int(data.r0Box)
            self.filesBin = int(data.filesPerBinBox)

            # gives a bool for tickboxes
            self.boolFLA = data.flaCheckbox.bool()
            self.boolLee = data.leeFilterCheck.bool()
            self.boolPostA = data.postAnaCheckbox.bool()
            self.boolTotal = data.minTotalTick.bool()
            self.thirty_thirty = data.thirtythirtyCheck.bool()


        except AttributeError:
            raise AttributeError
            print('\nSeems like the settings file is wrongly formatted or does miss some values')
            return

    ### Section initital data processing before applying burst function on data ###

    def hhd_handling(self, Brd_GGR, Brd_RR, repRate, dtBin):
        # takes two file paths which are the ones for green and red channel (correction)
        '''

        Args:
            hhdfileG: path to green hhd file
            hhdfileR: path to red hhd file
            Brd_GGR: range top
            Brd_RR: range bottom
            repRate: will get from first ht3 readout
            dtBin: will get from first ht3 readout

        Returns: newIRF_G, meanIRFG, newIRF_R, meanIRFR --> als self. in object version

        '''
        numCh = (1e12 / repRate / dtBin)
        midCh = (round(numCh / 2))

        RHHD_G = read_hhd(self.first_hhd)

        IRF_AllG = RHHD_G[0]
        IRF_G = IRF_AllG[1] + IRF_AllG[3]
        IRF_G = IRF_G - np.mean(IRF_G[int(numCh) - 601:int(numCh) - 100])

        self.newIRF_G = IRF_G[Brd_GGR[0] - 1:Brd_GGR[1]]

        self.meanIRFG = (np.sum(np.arange(1, len(self.newIRF_G) + 1, 1) * self.newIRF_G) / np.sum(self.newIRF_G) +
                    Brd_GGR[0]) * dtBin / 1000

        RHHD_R = read_hhd(self.second_hhd)

        IRF_AllR = RHHD_R[0]
        IRF_R = IRF_AllR[0] + IRF_AllR[2]
        IRF_R = IRF_R - np.mean(IRF_R[int(midCh) - 501:int(midCh) - 100])

        self.newIRF_R = IRF_R[Brd_RR[0] - 1:Brd_RR[1]]

        self.meanIRFR = (np.sum(np.arange(1, len(self.newIRF_R) + 1, 1) * self.newIRF_R) / np.sum(self.newIRF_R) +
                    Brd_RR[0]) * dtBin / 1000

    def check_running_files(self, folder_path):
        '''
        Args:
            folder_path: path of current Bat working folder

        Returns: Void --> Will check if the running files are already created in the folder. If not they get created
                          where getBurstAll will expect them

        '''

        # create expected file dirs

        self.str_path_dA = folder_path + '/allHIST.npy'
        self.str_pathdN = folder_path + '/backHIST.npy'
        self.str_path_lastBN = folder_path + '/lastBN.npy'

        # save empty file for usage in getBurstAll

        if not os.path.isfile(self.str_path_dA):
            dataAll = dict()
            dataAll['photonHIST'] = np.zeros([4096, 2])
            np.save(self.str_path_dA, dataAll)
            del dataAll


        if not os.path.isfile(self.str_pathdN):
            dataN = dict()
            dataN['backHIST'] = np.zeros([4096, 2])
            dataN['time'] = [0]
            np.save(self.str_pathdN, dataN)

        # create running lastBN file
        if not os.path.isfile(self.str_path_lastBN):
            np.save(self.str_path_lastBN, 0)











if __name__ == '__main__':
    print('Run on the fly burst')

    app = QApplication(sys.argv)
    app.setApplicationDisplayName("OTF_pyBat")
    # app.setWindowIcon(QtGui.QIcon('requirements/batIcon.png'))
    w = File_DD_Dialog()
    w.setWindowTitle('OTF-Bat')
    w.show()
    sys.exit(app.exec_())