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
from OnTheFlyBurst_Scripts.Select_file_Window import File_DD_Dialog


class OTF_Burst():

    def __init__(self):

        self.start_file_dialogue()
        self.import_settings()
        # init first file flag since some info is extracted from just first file
        self.first_file = True

        # start program
        self.track_ht3_folder(self.target_folder)

    ### Section for folder tracking and init if file is created ###

    def start_file_dialogue(self):

        gapp = QApplication(sys.argv)
        dlg = File_DD_Dialog()
        dlg.exec_()

        try:
            self.target_folder = dlg.file_dir_dict['Tracker']
            self.setting_file = dlg.file_dir_dict['Settings']
            self.first_hhd = dlg.file_dir_dict['HHD1']
            self.second_hhd = dlg.file_dir_dict['HHD2']

        except:
            print('Please select files')
            quit = input('Do you want to exit the program Y/N?: ')
            if quit.upper() == 'Y' or quit.upper() == 'YES':
                exit()
            else:
                self.start_file_dialogue()

    def on_create_ht3_file(self, event):

        file_root = os.path.dirname(event.src_path)
        file_name = os.path.basename(event.src_path)
        file_path = event.src_path

        if self.first_file:

            print(f'Working on file: {file_name}')

            try:
                Data = read_ht3_raw(file_path)
                repRate = Data['SyncRate']
                self.dtBin = Data['varout4']

                # clear cash
                del Data

            except (IndexError, FileNotFoundError):
                print('Error no ht3 data given')
                return

            self.hhd_handling(Brd_GGR=self.roiMLE_G, Brd_RR=self.roiMLE_R, repRate=repRate, dtBin=self.dtBin)

            # create running files
            self.check_running_files(folder_path=file_root)

            lastBN = np.load(self.str_path_lastBN)

            # trigger get burst all
            Bursts = getBurstAll(filename=file_name, pathname=file_root, suffix='', lastBN=lastBN,
                                 roiRG=self.roiMLE_G, roiR0=self.roiMLE_R, threIT=self.threIT, threIT2=self.threITN,
                                 minPhs=self.minPhs, threAveT=10, newIRF_G_II=self.newIRF_G_II,
                                 newIRF_G_T=self.newIRF_G_T,  meanIRFG_II=self.meanIRFG_II, meanIRFG_T=self.meanIRFG_T,
                                 newIRF_R_II=self.newIRF_R_II, newIRF_R_T=self.newIRF_R_T, meanIRFR_II=self.meanIRFR_II,
                                 meanIRFR_T=self.meanIRFR_T, roiMLE_G=self.roiMLE_G, roiMLE_R=self.roiMLE_R,
                                 dtBin=self.dtBin, setLeeFilter=self.setLeeFilter, boolFLA=self.boolFLA, gGG=self.gGG,
                                 gRR=self.gRR, boolTotal=self.boolTotal, minGR=self.minGR, minR0=self.minR0,
                                 boolPostA=self.boolPostA, checkInner=False)

            # save lastBN in running file folder wise
            lastBN += len(Bursts)
            np.save(self.str_path_lastBN, lastBN)

            self.first_file = False


        elif self.first_file == False:

            print(f'Working on file: {file_name}')

            self.check_running_files(folder_path=file_root)
            lastBN = np.load(self.str_path_lastBN)

            Bursts = getBurstAll(filename=file_name, pathname=file_root, suffix='', lastBN=lastBN,
                                 roiRG=self.roiMLE_G, roiR0=self.roiMLE_R, threIT=self.threIT, threIT2=self.threITN,
                                 minPhs=self.minPhs, threAveT=10, newIRF_G_II=self.newIRF_G_II,
                                 newIRF_G_T=self.newIRF_G_T,  meanIRFG_II=self.meanIRFG_II, meanIRFG_T=self.meanIRFG_T,
                                 newIRF_R_II=self.newIRF_R_II, newIRF_R_T=self.newIRF_R_T, meanIRFR_II=self.meanIRFR_II,
                                 meanIRFR_T=self.meanIRFR_T, roiMLE_G=self.roiMLE_G, roiMLE_R=self.roiMLE_R,
                                 dtBin=self.dtBin, setLeeFilter=self.setLeeFilter, boolFLA=self.boolFLA, gGG=self.gGG,
                                 gRR=self.gRR, boolTotal=self.boolTotal, minGR=self.minGR, minR0=self.minR0,
                                 boolPostA=self.boolPostA, checkInner=False)

            # save lastBN in running file folder wise
            lastBN += len(Bursts)
            np.save(self.str_path_lastBN, lastBN)

    def track_ht3_folder(self, dir):

        # function tracking dir in which folders will be created
        print(f'Tracking: {dir}')
        # dir = '/Users/philipp/Desktop/Work/WHK Schlierf Group/smFRET_Software/speed_tests/eval_folder'
        # track only ht3 files in the folder
        patterns = ['*.ht3']
        ignore_patterns = None
        ignore_dirs = True
        case_sensitive = True
        event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_dirs, case_sensitive)

        event_handler.on_created = self.on_create_ht3_file

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
            data = None
            return

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
            self.roiMLE_G = [int(data.roiMLE_G_lower), int(data.roiMLE_G_upper)]
            self.roiMLE_R = [int(data.roiMLE_R_lower), int(data.roiMLE_R_upper)]

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

        # split parallel (II) and perpendicular (T) parts

        IRF_G_II = IRF_AllG[1]
        IRF_G_T = IRF_AllG[3]

        IRF_G_II = IRF_G_II - np.mean(IRF_G_II[int(numCh) - 601:int(numCh) - 100])
        IRF_G_T = IRF_G_T - np.mean(IRF_G_T[int(numCh) - 601:int(numCh) - 100])

        self.newIRF_G_II = IRF_G_II[Brd_GGR[0] - 1:Brd_GGR[1]]
        self.newIRF_G_T = IRF_G_T[Brd_GGR[0] - 1:Brd_GGR[1]]

        self.meanIRFG_II = (np.sum(np.arange(1, len(self.newIRF_G_II) + 1, 1) * self.newIRF_G_II) / np.sum(
            self.newIRF_G_II) +
                       Brd_GGR[0]) * dtBin / 1000
        self.meanIRFG_T = (np.sum(np.arange(1, len(self.newIRF_G_T) + 1, 1) * self.newIRF_G_T) / np.sum(self.newIRF_G_T) +
                      Brd_GGR[0]) * dtBin / 1000


        RHHD_R = read_hhd(self.second_hhd)

        IRF_AllR = RHHD_R[0]
        IRF_R = IRF_AllR[0] + IRF_AllR[2]
        IRF_R = IRF_R - np.mean(IRF_R[int(midCh) - 501:int(midCh) - 100])

        IRF_R_II = IRF_AllR[0]
        IRF_R_T = IRF_AllR[2]

        IRF_R_II = IRF_R_II - np.mean(IRF_R_II[int(midCh) - 501:int(midCh) - 100])
        IRF_R_T = IRF_R_T - np.mean(IRF_R_T[int(midCh) - 501:int(midCh) - 100])

        self.newIRF_R_II = IRF_R_II[Brd_GGR[0] - 1:Brd_GGR[1]]
        self.newIRF_R_T = IRF_R_T[Brd_GGR[0] - 1:Brd_GGR[1]]

        self.meanIRFR_II = (np.sum(np.arange(1, len(self.newIRF_R_II) + 1, 1) * self.newIRF_R_II) / np.sum(
            self.newIRF_R_II) +
                       Brd_RR[0]) * dtBin / 1000
        self.meanIRFR_T = (np.sum(np.arange(1, len(self.newIRF_R_T) + 1, 1) * self.newIRF_R_T) / np.sum(self.newIRF_R_T) +
                      Brd_RR[0]) * dtBin / 1000


        self.newIRF_G = IRF_G[Brd_GGR[0] - 1:Brd_GGR[1]]

        self.meanIRFG = (np.sum(np.arange(1, len(self.newIRF_G) + 1, 1) * self.newIRF_G) / np.sum(self.newIRF_G) +
                         Brd_GGR[0]) * dtBin / 1000


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
    OTF_Burst()
