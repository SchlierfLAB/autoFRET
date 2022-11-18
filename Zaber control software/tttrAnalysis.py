#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Analysis code for HydraHarp 400 - T3 mode
'''

import struct
import matplotlib.pyplot as plt
import numpy as np


MeasDesc_GlobalResolution = 0.016
global f
cnt_ph = 0
cnt_ma = 0
cnt_ov = 0
RecNum = 0
isT2 = False

fpout = open("tttrOutTest.out", 'w')


def gotPhoton(TimeTag, Channel, DTime):
    global isT2
    global fpout
    global RecNum
    global MeasDesc_GlobalResolution
    global cnt_ph

    cnt_ph = cnt_ph + 1
    if (isT2):
        print('%i CHN %1x %i %e\n' % (RecNum, Channel, TimeTag,
                                        (TimeTag * MeasDesc_GlobalResolution * 1e12)), file=fpout)
    else:
        print("%i CHN %1x %i %e %i\n" % (RecNum, Channel, TimeTag,
                                        (TimeTag * MeasDesc_GlobalResolution * 1e12), DTime), file=fpout)

def gotMarker(TimeTag, Markers):
    global f
    global RecNum
    global cnt_ma
    cnt_ma = cnt_ma + 1
    print("%i MAR %x %i\n" % (RecNum, Markers, TimeTag), file=fpout)

def gotOverflow(Count):
    global f
    global RecNum
    global cnt_ov
    cnt_ov = cnt_ov + Count
    print("%i OFL * %x\n", RecNum, Count, file=fpout)


# plt.figure()
T3WRAPAROUND = 1024
ofltime = 0

with open('Hydraharp_test\\tttrmode4.out', 'rb') as f:
    # for line in f:
    #     # t3rec = f.read(4)
    #     # t3rec = int.from_bytes(t3rec, byteorder='big')
    #     # nsync = t3rec & (65535)
    #     # chan = (t3rec >> (28)) & (15)
    #     t3rec = line
    #     t3rec = int.from_bytes(t3rec, byteorder='big')
    #     nsync = t3rec & (65535)
    #     chan = (t3rec >> (28)) & (15)
    #     print(chan)

    """
    Old data analysis method
    """
    t3rec_temp = [line for line in f]
    t3rec = [int.from_bytes(value, byteorder='big') for value in t3rec_temp]
    # nsync = np.bitwise_and(t3rec, 65535)
    # chan = np.bitwise_and(np.right_shift(t3rec, 28), 15)

    # truensync = ofltime + nsync

    # for chanNum in range(np.size(chan)):
    #     if (chan[chanNum] >= 0 and chan[chanNum] <= 4):
    #         dtime = np.bitwise_and(np.right_shift(t3rec, 16), 4095)
    #         gotPhoton(truensync[chanNum], chan[chanNum], dtime[chanNum])
    #     else:
    #         if chan[chanNum] == 15:
    #             # markers = np.bitwise_and(np.right_shift(t3rec[chanNum], 16), 15)
    #             markers = np.right_shift(t3rec[chanNum], 16) & 15
    #             if markers == 0:
    #                 ofltime = ofltime + T3WRAPAROUND
    #                 gotOverflow(1)
    #             else:
    #                 gotMarker(truensync[chanNum], markers)
    #         else:
    #             print("Err ", file=fpout)

    #     RecNum += 1

    """
    New (faster) data analysis method
    """

    nsync2 = np.bitwise_and(t3rec, 1023)
    dtime2 = np.bitwise_and(np.right_shift(t3rec,10),32767)
    chan2 = np.bitwise_and(np.right_shift(t3rec, 25), 63)
    special = np.bitwise_and(np.right_shift(t3rec,31),1)

    

    # t1 = np.bitwise_and(special[np.nonzero(special)], chan2[np.where(chan2 == 63)[0]])
    # t1 = special[np.nonzero(special)] & chan2[np.where(chan2 == 63)[0]]
    # t1 = special[special != 0]

    # oldOFL = np.bitwise_and(np.bitwise_and(special[np.nonzero(special)], np.where(chan2 == 63)[0]), np.where(nsync2==0)[0])

    # plt.plot(t1)
    # plt.show()
