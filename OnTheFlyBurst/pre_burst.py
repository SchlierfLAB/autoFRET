# 'TODO: Create a function which can do all preprocessing before actual burst function kicks in
#  TODO: with only a bin file as input'

import pandas as pd
import numpy as np
from FRET_backend.read_hhd import read_hhd
import os

def import_settings(file_path):

    '''
    Args:
        file_path: path to a predefined settings file

    Returns: Values for the burst analyzing settings for the on the fly bat implementation without any
    UI
    '''

    # import csv from selected into pandas df
    out = pd.read_csv(file_path)

    return out.leeFilterBox.values,out.gGGBox.values,out.gRRBox.values,out.maxInterTime.values,\
           out.minInterTimeNoise.values,out.minTotal.values,out.grBox.values,out.r0Box.values,\
           out.filesPerBinBox.values,out.flaCheckbox.values,out.leeFilterCheck.values,\
           out.postAnaCheckbox.values,out.minTotalTick.values,out.thirtythirtyCheck.values

def hhd_handling(hhdfileG, hhdfileR, Brd_GGR, Brd_RR, repRate, dtBin):
    # takes two file paths which are the ones for green and red channel (correction)
    '''

    Args:
        hhdfileG: path to green hhd file
        hhdfileR: path to red hhd file
        Brd_GGR: range top
        Brd_RR: range bottom
        repRate: will get from first ht3 readout
        dtBin: will get from first ht3 readout

    Returns: newIRF_G, meanIRFG, newIRF_R, meanIRFR

    '''
    numCh = (1e12 / repRate / dtBin)
    midCh = (round(numCh / 2))

    RHHD_G = read_hhd(hhdfileG)

    IRF_AllG = RHHD_G[0]
    IRF_G = IRF_AllG[1] + IRF_AllG[3]
    IRF_G = IRF_G - np.mean(IRF_G[int(numCh) - 601:int(numCh) - 100])

    newIRF_G = IRF_G[Brd_GGR[0] - 1:Brd_GGR[1]]

    meanIRFG = (np.sum(np.arange(1, len(newIRF_G) + 1, 1) * newIRF_G) / np.sum(newIRF_G) +
                Brd_GGR[0]) * dtBin / 1000

    RHHD_R = read_hhd(hhdfileR)

    IRF_AllR = RHHD_R[0]
    IRF_R = IRF_AllR[0] + IRF_AllR[2]
    IRF_R = IRF_R - np.mean(IRF_R[int(midCh) - 501:int(midCh) - 100])

    newIRF_R = IRF_R[Brd_RR[0] - 1:Brd_RR[1]]

    meanIRFR = (np.sum(np.arange(1, len(newIRF_R) + 1, 1) * newIRF_R) / np.sum(newIRF_R) +
                Brd_RR[0]) * dtBin / 1000

    return newIRF_G, meanIRFG, newIRF_R, meanIRFR

def check_running_files(folder_path):
    '''
    Args:
        folder_path: path of current Bat working folder

    Returns: Void --> Will check if the running files are already created in the folder. If not they get created
                      where getBurstAll will expect them

    '''


    # save empty file for usage in getBurstAll
    dataAll = dict()
    dataAll['photonHIST'] = np.zeros([4096, 2])
    str_path_dA = folder_path + '/allHIST.npy'

    if not os.path.isfile(str_path_dA):
        np.save(str_path_dA, dataAll)

    dataN = dict()
    dataN['backHIST'] = np.zeros([4096, 2])
    dataN['time'] = [0]
    str_pathdN = folder_path + '/backHIST.npy'

    if not os.path.isfile(str_pathdN):
        np.save(str_pathdN, dataN)

    # create running lastBN file
    str_path_lastBN = folder_path + '/lastBN.npy'
    if not os.path.isfile(str_path_lastBN):
        np.save(str_path_lastBN, 0)




if __name__ == '__main__':

    #### Section 1: Stuff that only needs to be done once per analysis ####

    # Todo: load current settings + hhdFiles for red and green

    setting_input = import_settings(file_path)

    # Todo: obtain average IRF shift

    newIRF_G, meanIRFG, newIRF_R, meanIRFR = hhd_handling(hhdfileG, hhdfileR, Brd_GGR, Brd_RR, repRate, dtBin)
    #### Section 2: Needs to be done per folder ####

    # Todo: Should check inner by user given or just turned off for later version?
    existCB = 0
    checkInner = 0
    folder_counter = 0



#' Target function
# BurstData = getBurstAll(fileName, folderName, suffix, lastBN, Brd_GGR, Brd_RR,threIT \
#                                         , threITN, minPhs, 10, newIRF_G, meanIRFG, newIRF_R, \
#                                         meanIRFR, Brd_GGR, Brd_RR, dtBin, setLeeFilter, \
#                                         boolFLA, gGG, gRR, boolTotal, minGR, minR0, \
#                                         boolPostA, checkInner)
#
#                                         ==> For which the input shall be provided mostly by this and a postprocessing
#                                         script that mainly hands over the lastBN value which is the cum sum of
#                                         all prior len(BurstData)'
