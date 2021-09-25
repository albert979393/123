from astropy.io import fits
import numpy as np
def qiepian(path):
    with fits.open(path) as hdul:
        t1= np.array(hdul[0].data)
        var = t1[392:493,253:354]
        return var
def Qie():
    path='/home/deng/traindata300-300_zw44_list/uv7_1-1.fits'
    result=qiepian(path)
    return result










