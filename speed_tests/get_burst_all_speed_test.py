# Aimed to construct a burst speed test
from FRET_backend.getBurstAll import getBurstAll
from FRET_backend.numba_getBurstAll import NgetBurstAll
from FRET_backend.get_burst_all_loop_optimized import LOgetBurstAll
import scipy.io as sio
import numpy as np
import os
import time

def get_params():
    # get function inputs from matlab file
    inputs_path = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/Sample_Data/example_function_input.mat'
    inputs = sio.loadmat(inputs_path)
    inputs.pop('__header__')
    inputs.pop('__version__')
    inputs.pop('__globals__')

    roiRG = [21, 1217]
    roiR0 = [1240, 2452]

    roiMLE_G = [21,1217]
    roiMLE_R = [1240, 2452]

    lastBN = 0

    threIT = inputs['threIT'][0]
    threIT2 = inputs['threIT2'][0]
    minPhs = inputs['minPhs'][0]
    threAveT = inputs['threAveT'][0]
    IRF_G = inputs['IRF_G'][0]
    meanIRFG = inputs['meanIRFG'][0]
    IRF_R = inputs['IRF_R'][0]
    meanIRFR = inputs['meanIRFR'][0]
    dtBin = inputs['dtBin'][0]
    setLeeFilter = inputs['setLeeFilter'][0]
    boolFLA = inputs['boolFLA'][0]
    gGG = inputs['gGG'][0]
    gRR = inputs['gRR'][0]
    boolTotal = inputs['boolTotal'][0]
    minGR = inputs['minGR'][0]
    minR0 = inputs['minR0'][0]
    boolPostA = inputs['boolPostA'][0]
    checkInner = inputs['checkInner'][0]

    return roiRG, roiR0, roiMLE_G, roiMLE_R, lastBN, threIT, threIT2, minPhs, threAveT, IRF_G, meanIRFG, IRF_R, \
           meanIRFR, dtBin, dtBin, dtBin, setLeeFilter, boolFLA, gGG, gRR, boolTotal, minGR, minR0, boolPostA, \
           checkInner


if __name__ == '__main__':
    print('main')

    Optimized = True

    # Call get burst all on a test dataset

    # def getBurstAll(filename, pathname, suffix, lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, IRF_G,
    #                 meanIRFG, IRF_R, meanIRFR, roiMLE_G, roiMLE_R, dtBin, setLeeFilter, boolFLA, gGG, gRR, boolTotal, minGR, minR0,
    #                 boolPostA, checkInner)

    # Hardcode path because why not

    root_for_mes = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/' \
                   'smFRET_Software/speed_tests/Sample_data/typical_96well_data'

    first_irf = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/smFRET_Software/' \
               'speed_tests/Sample_data/typical_96well_data/IRF_L530_EryB_KI_X.hhd'

    second_irf = '/Users/mbpro/Desktop/Work/WHK Schlierf Group/smFRET_Software/' \
                 'speed_tests/Sample_data/typical_96well_data/IRF_L640_ATTO655_KI.hhd'


    roiRG, roiR0, roiMLE_G, roiMLE_R, lastBN, threIT, threIT2, minPhs, threAveT, IRF_G, meanIRFG, IRF_R, \
    meanIRFR, dtBin, dtBin, dtBin, setLeeFilter, boolFLA, gGG, gRR, boolTotal, minGR, minR0, boolPostA, \
    checkInner = get_params()

    print('Start get burst all')

    start = time.time()

    for folder in os.walk(root_for_mes):

        if folder[0] != root_for_mes:
            pathname = folder[0]
            lastBN = 0
            print(f'Working on folder: {pathname.split("/")[-1]}')

            # save empty file for usage in getBurstAll
            dataAll = dict()
            dataAll['photonHIST'] = np.zeros([4096,2])
            str_path_dA = pathname + '/allHIST.npy'
            np.save(str_path_dA, dataAll)

            dataN = dict()
            dataN['backHIST'] = np.zeros([4096,2])
            dataN['time'] = [0]
            str_pathdN = pathname + '/backHIST.npy'
            np.save(str_pathdN, dataN)

            for file in folder[2]:

                print(f'Working on file {file}')

                # exclude all but ht3 files
                if file.endswith('.ht3'):

                    if not Optimized:
                        print('Non numba version')
                        BurstData = getBurstAll(file, pathname, 'Python_test', lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, IRF_G,
                                                meanIRFG, IRF_R, meanIRFR, roiMLE_G, roiMLE_R, dtBin, setLeeFilter[0], boolFLA, gGG, gRR, boolTotal, minGR, minR0,
                                                boolPostA, checkInner)
                    elif Optimized:
                        print('Optimized version')
                        BurstData = LOgetBurstAll(file, pathname, 'Python_test', lastBN, roiRG, roiR0, threIT, threIT2, minPhs, threAveT, IRF_G,
                                                meanIRFG, IRF_R, meanIRFR, roiMLE_G, roiMLE_R, dtBin, setLeeFilter[0], boolFLA, gGG, gRR, boolTotal, minGR, minR0,
                                                boolPostA, checkInner)
                    lastBN += len(BurstData)


    finished = time.time() - start

    print(f'Finished in {finished} seconds')

# default run Finished in 478.69442200660706 seconds