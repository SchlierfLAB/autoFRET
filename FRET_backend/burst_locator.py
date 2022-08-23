import numpy as np

def burstLoc(Arr, minDistace):
    '''
    Clone of the matlab burstLoc function from ?Andreas?

    Args:
        Arr: Array of positions
        minDistace: minimume distance (int)
    Returns:
    '''

    Arr = np.append(Arr, Arr[-1])
    bIndex = np.argwhere((Arr[1:] - Arr[0:-1]) >1)+1
    bIndex = np.insert(bIndex, 0, 0, axis=0)
    bLength = np.zeros(len(bIndex))
    bStart = Arr[bIndex]

    for iterator in range(len(bIndex)):
        length = 1
        index = bIndex[iterator]

        while Arr[index+1] == (Arr[index]+1):
            length += 1
            index += 1

        bLength[iterator] = length

    bStartAcc = bStart[0]
    bLengthAcc = bLength[0]

    del iterator

    for iterator in range(1,len(bStart)):

        if (bStart[iterator] - (bStart[iterator-1] + bLength[iterator-1] - 1)) > minDistace:
            bStartAcc = np.append(bStartAcc, bStart[iterator])
            bLengthAcc = np.append(bLengthAcc, bLength[iterator])


    return bStartAcc, bLengthAcc





