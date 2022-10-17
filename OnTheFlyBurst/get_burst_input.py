import scipy.io as sio

def get_input(matlab_workspace_file =
              '/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/Sample_Data/example_function_input.mat'):

    inputs = sio.loadmat(matlab_workspace_file)

    # transform dict to vars
    threIT = inputs['threIT']
    threIT2 = inputs['threIT2']
    minPhs = inputs['minPhs']
    threAveT = inputs['threAveT']
    IRF_G = inputs['IRF_G']
    meanIRFG = inputs['meanIRFG']
    IRF_R = inputs['IRF_R']
    meanIRFR = inputs['meanIRFR']
    dtBin = inputs['dtBin']
    setLeeFilter = inputs['setLeeFilter']
    boolFLA = inputs['boolFLA']
    gGG = inputs['gGG']
    gRR = inputs['gRR']
    boolTotal = inputs['boolTotal']
    minGR = inputs['minGR']
    minR0 = inputs['minR0']
    boolPostA = inputs['boolPostA']
    checkInner = inputs['checkInner']

    del inputs

    return threIT, threIT2, minPhs, threAveT, IRF_G, meanIRFG, IRF_R, meanIRFR, dtBin, setLeeFilter, boolFLA, \
           gGG, gRR, boolTotal, minGR, minR0, boolPostA, checkInner



