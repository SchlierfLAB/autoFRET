from scipy.ndimage.measurements import variance
from scipy import ndimage
import numpy as np
import cv2
import copy

def lee_filter_uniform(img ,filter_ , size=4):
    img_mean = ndimage.mean(img)
    img_sqr_mean = getattr(ndimage,filter_)(img**2,size)
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = variance(img)

    img_weights = img_variance / (img_variance + overall_variance)
    img_output = img_mean + img_weights * (img - img_mean)

    return img_output

def fspecial_average(window_size):
    '''
    Clone of matlabs f special function to create a kernel of type average
    Args:
        window_size:
    Returns: Smoothing filter kernel
    '''

    h = np.ones([window_size,window_size],np.float64)/np.prod([window_size,window_size])

    return h

def im_filterish_function(I,window_size):
    '''
    Args:
        I: inter photon time (some array :D)
        window_size: int

    Returns: filtered array

    --> Basically it is imfilter with replicate border condition
    '''

    # Todo: The border condition is not 100% same first element differs (actually the second is where it would start in
    # Todo: matlab and the last is missing (second last in matlab)
    means = cv2.filter2D(np.float64(I), -1, fspecial_average(window_size), borderType=cv2.BORDER_REPLICATE)

    return np.append(means[1:],means[0]).T

def leeFilter(I_, window_size):

    # Todo: Direct comparison of matlab and python output
    '''
    Matlab clone of Grzegorz Mianowski
    https://de.mathworks.com/matlabcentral/fileexchange/28046-lee-filter

    Args:
        I:
        window_size:

    Returns:

    '''

    I_ = np.float64(I_)
    OIm = copy.deepcopy(I_)
    means_ = im_filterish_function(I_, window_size)
    sigmas = np.sqrt((I_ - means_)**2 / window_size**2)
    sigmas = im_filterish_function(sigmas, window_size)

    ENLs = (means_/sigmas)**2
    sx2s = ((ENLs * sigmas **2) - means_**2) / (ENLs +1)
    # at this point the last three elements are "wrong" compare to matlab due to mismatching boundaries
    # in fbar only last element is wrong
    fbar = means_ + (sx2s * (I_-means_) / (sx2s + (means_**2 / ENLs)))

    OIm[means_ != 0] = fbar[fbar != 0]

    return OIm


if __name__ == '__main__':
    test_img = np.fromfile('/Users/mbpro/Desktop/Work/WHK Schlierf Group/pyFRET_ph/Sample_Data/test_interPHT')

    OIm = leeFilter(test_img, 4)
