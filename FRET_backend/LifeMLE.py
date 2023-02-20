import numpy as np
from scipy.interpolate import CubicSpline, interp1d

def LifeMLE(IRF, meanIRF, Data, meanData, dtBin, boolFLA):

    if any(Data) and (np.sum(Data) != 0):

        numCh = len(Data)
        N = np.sum(Data)
        ies = np.arange(1,numCh+1,1)

        if (boolFLA == 0) and (np.sum(Data) >= 10):
            tau1 = np.arange(0,10.2,0.2)+0.01
            logMLE = np.zeros(len(tau1))

            for i in range(len(tau1)):
                func = np.exp(-ies * dtBin / tau1[i] / 1000)
                fold = convol(IRF, func)
                g = fold / np.sum(fold) * N
                ind = (g>0) & (Data > 0)
                logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
            del i

            # split fit
            t = np.arange(0.01, 10.02, 0.1)
            SplFunc = CubicSpline(x=tau1, y=logMLE) # piecewise cubic polynomial which is twice continuously differentiable
            Spl = SplFunc(t) # get y values from fit function
            v = np.min(Spl)

            # Todo: Well just confirm with others if this is the way
            # not to sure about the [0] but as it seems matlab [val, index] = min(someStuff) does only return
            # the index of a singl/first occuring minimum item. If one do this on a list of zeros the index
            # returned is just 1 (first element because of MATLAB counting system) but np.where gives a array
            # with all elements --> so by [0] only first index element is selected (does work if there is only
            # a single element
            # wow lots of comments for a simple expression lets ad another
            # höhö
            indMin = np.where(Spl == v)[0][0]

            minTau1 = t[indMin]


            tau2 = np.arange(minTau1-1, minTau1+1.1,0.1)
            del logMLE, func, g, ind # clear var before assigning new values
            logMLE = np.zeros(len(tau2))

            for i in range(len(tau2)):

                if tau2[i] > 0:
                    func = np.exp(-ies * dtBin / tau2[i] / 1000)
                    fold = convol(IRF, func)
                    g = fold / np.sum(fold) * N
                    ind = (g>0) & (Data > 0)
                    logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
                else:
                    logMLE[i] = np.inf
            del i

            # split fit
            t = np.arange(tau2[0], tau2[-1] + ((tau2[-1] - tau2[0]) / 100), (tau2[-1] - tau2[0]) / 100)
            # fill by extrapolation to have proper interpolation range
            # Todo: Danger this way Spl will contain nan values while in Matlab it inserts inf
            # Todo: If in Matlab some nan would occure this will be the smallest value (v)
            # Todo: In this case the result will differ from python since here i ignore all nan values with nanmin
            SplFunc = interp1d(x=tau2, y=logMLE, fill_value="extrapolate")
            Spl = SplFunc(t) # get y values from fit function
            v = np.nanmin(Spl)

            indMin = np.where(Spl == v)[0][0]
            minTau2 = t[indMin]

            tau3 = np.arange(minTau2-0.1, minTau2+0.11,0.01)
            del logMLE, func, g, ind # clear var before assigning new values
            logMLE = np.zeros(len(tau3))

            for i in range(len(tau3)):

                if tau3[i] > 0:
                    func = np.exp(-ies * dtBin / tau3[i] / 1000)
                    fold = convol(IRF, func)
                    g = fold / np.sum(fold) * N
                    ind = (g>0) & (Data > 0)
                    logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
                else:
                    logMLE[i] = np.inf
            del i

            # spline fit
            t = np.arange(tau3[0], tau3[-1] + ((tau3[-1] - tau3[0]) / 100), (tau3[-1] - tau3[0]) / 100)

            # Todo: I guess this wont resolve the problem since Matlab somehow can handle non finite values in
            # Todo: the spline --> Still wack
            try:
                SplFunc = CubicSpline(x=tau3, y=logMLE) # piecewise cubic polynomial which is twice continuously differentiable
                Spl = SplFunc(t) # get y values from fit function
                v = np.min(Spl)
                indMin = np.where(Spl == v)[0][0]
                trueTau = t[indMin]
            except ValueError:
                trueTau = t[0]


        else:
            trueTau = meanData * dtBin / 1000 - meanIRF
    else:
        trueTau = 0

    return trueTau


def convol(irf, x):

    irf = np.array(irf)
    mm = np.mean(irf[-11:])

    '''part from matlab that does not seem required for python
    if size(x,1) == 1 | size(x,2) == 1
        irf = irf(:) 
        x = x(:)'''

    '''if len(x.shape) == 1:
        p = 1
    else:
        p = x.shape[1]'''
    n = len(irf)
    p = len(x)

    # required because matlab gives an error if one would to know dimension of 1D vectore by using
    # x.shape[1] while matlab will return 1 for size(x,2)
    try:
        xSize = x.shape[1]
    except IndexError:
        xSize = 1


    if p>n:
        irf = [irf, mm*np.ones(np.abs(p-n))]
    else:
        irf = irf[0:p]

    y = (np.fft.ifft((np.fft.fft(irf) * np.ones([xSize,xSize])) * np.fft.fft(x))).real[0]

    t = (((np.arange(n) % p) + p) % p)

    y = y[t]

    return y



if __name__ == '__main__':
    print('Welcome to Main wonderworld where the debugging magic can happen outside the function body')

    # variables from bat: IRF_G, meanIRFG, roihMicroG, mean_roiMicroG, dtBin, boolFLA, roiRG[0]
    # Todo: For debugging only
    IRF = [-0.70658683, 1.29341317, 1.29341317, -2.70658683, 1.29341317, 0.29341317, -5.70658683, -3.70658683, 2.29341317, -1.70658683, 5.29341317, 1.29341317, -1.70658683, -2.70658683, -3.70658683, -5.70658683, 6.29341317, 7.29341317, 4.29341317, -0.70658683, -2.70658683, -0.70658683, -1.70658683, -3.70658683, 4.29341317, 0.29341317, -3.70658683, 6.29341317, 0.29341317, 3.29341317, 0.29341317, 2.29341317, -4.70658683, -0.70658683, -3.70658683, 4.29341317, 4.29341317, 1.29341317, 9.29341317, -2.70658683, -0.70658683, 9.29341317, -4.70658683, 1.29341317, 4.29341317, -4.70658683, 0.29341317, -6.70658683, -2.70658683, 5.29341317, -2.70658683, 2.29341317, 5.29341317, -3.70658683, -0.70658683, 3.29341317, -0.70658683, 4.29341317, 0.29341317, 8.29341317, -0.70658683, -1.70658683, 0.29341317, 1.29341317, 0.29341317, -1.70658683, -2.70658683, -2.70658683, -0.70658683, -2.70658683, -0.70658683, -0.70658683, -3.70658683, 2.29341317, -4.70658683, 3.29341317, -0.70658683, -2.70658683, -3.70658683, 7.29341317, -3.70658683, 6.29341317, 0.29341317, 0.29341317, 1.29341317, 2.29341317, 9.29341317, 2.29341317, 1.29341317, 0.29341317, 1.29341317, 9.29341317, -1.70658683, -3.70658683, -5.70658683, 4.29341317, 3.29341317, 3.29341317, 0.29341317, 5.29341317, -3.70658683, 0.29341317, 0.29341317, 1.29341317, 1.29341317, 1.29341317, -1.70658683, 0.29341317, 3.29341317, 1.29341317, -3.70658683, 0.29341317, 13.29341317, 0.29341317, 2.29341317, 9.29341317, 1.29341317, 3.29341317, -4.70658683, 1.29341317, -4.70658683, 3.29341317, -2.70658683, -2.70658683, -1.70658683, 1.29341317, 1.29341317, 0.29341317, -0.70658683, 1.29341317, 1.29341317, -0.70658683, -1.70658683, -2.70658683, -5.70658683, 2.29341317, 0.29341317, 4.29341317, -3.70658683, 4.29341317, -5.70658683, -1.70658683, -1.70658683, 2.29341317]
    meanIRF = np.array(21.1581301)
    Data = np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 0., 0.])
    meanData = np.array(1292.)
    dtBin = np.array(16)
    boolFLA = 1
    roiLeft = 1244

    if any(Data) and (np.sum(Data) != 0):

        numCh = len(Data)
        N = np.sum(Data)
        ies = np.arange(1,numCh+1,1)

        if (boolFLA == 0) and (np.sum(Data) >= 10):
            tau1 = np.arange(0,10.2,0.2)+0.01
            logMLE = np.zeros(len(tau1))

            for i in range(len(tau1)):
                func = np.exp(-ies * dtBin / tau1[i] / 1000)
                fold = convol(IRF, func)
                g = fold / np.sum(fold) * N
                ind = (g>0) & (Data > 0)
                logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
            del i

            # split fit
            t = np.arange(0.01, 10.02, 0.1)
            SplFunc = CubicSpline(x=tau1, y=logMLE) # piecewise cubic polynomial which is twice continuously differentiable
            Spl = SplFunc(t) # get y values from fit function
            v = np.min(Spl)

            # Todo: Well just confirm with others if this is the way
            # not to sure about the [0] but as it seems matlab [val, index] = min(someStuff) does only return
            # the index of a singl/first occuring minimum item. If one do this on a list of zeros the index
            # returned is just 1 (first element because of MATLAB counting system) but np.where gives a array
            # with all elements --> so by [0] only first index element is selected (does work if there is only
            # a single element
            # wow lots of comments for a simple expression lets ad another
            # höhö
            indMin = np.where(Spl == v)[0][0]

            minTau1 = t[indMin]


            tau2 = np.arange(minTau1-1, minTau1+1.1,0.1)
            del logMLE, func, g, ind # clear var before assigning new values
            logMLE = np.zeros(len(tau2))

            for i in range(len(tau2)):

                if tau2[i] > 0:
                    func = np.exp(-ies * dtBin / tau2[i] / 1000)
                    fold = convol(IRF, func)
                    g = fold / np.sum(fold) * N
                    ind = (g>0) & (Data > 0)
                    logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
                else:
                    logMLE[i] = np.inf
            del i

            # split fit
            t = np.arange(tau2[0], tau2[-1] + ((tau2[-1] - tau2[0]) / 100), (tau2[-1] - tau2[0]) / 100)
            # fill by extrapolation to have proper interpolation range
            # Todo: Danger this way Spl will contain nan values while in Matlab it inserts inf
            # Todo: If in Matlab some nan would occure this will be the smallest value (v)
            # Todo: In this case the result will differ from python since here i ignore all nan values with nanmin
            SplFunc = interp1d(x=tau2, y=logMLE, fill_value="extrapolate")
            Spl = SplFunc(t) # get y values from fit function
            v = np.nanmin(Spl)

            indMin = np.where(Spl == v)[0][0]
            minTau2 = t[indMin]

            tau3 = np.arange(minTau2-0.1, minTau2+0.11,0.01)
            del logMLE, func, g, ind # clear var before assigning new values
            logMLE = np.zeros(len(tau3))

            for i in range(len(tau3)):

                if tau3[i] > 0:
                    func = np.exp(-ies * dtBin / tau3[i] / 1000)
                    fold = convol(IRF, func)
                    g = fold / np.sum(fold) * N
                    ind = (g>0) & (Data > 0)
                    logMLE[i] = 2 / (numCh-1) * np.sum(Data[ind] * np.log(Data[ind] / g[ind]))
                else:
                    logMLE[i] = np.inf
            del i

            # spline fit
            t = np.arange(tau3[0], tau3[-1] + ((tau3[-1] - tau3[0]) / 100), (tau3[-1] - tau3[0]) / 100)

            # Todo: I guess this wont resolve the problem since Matlab somehow can handle non finite values in
            # Todo: the spline --> Still wack
            try:
                SplFunc = CubicSpline(x=tau3, y=logMLE) # piecewise cubic polynomial which is twice continuously differentiable
                Spl = SplFunc(t) # get y values from fit function
                v = np.min(Spl)
                indMin = np.where(Spl == v)[0][0]
                trueTau = t[indMin]
            except ValueError:
                trueTau = t[0]


        else:
            trueTau = meanData * dtBin / 1000 - meanIRF
    else:
        trueTau = 0

    #return trueTau
