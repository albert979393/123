import numpy as np
from astropy.table import Table
from photutils.datasets import (make_random_gaussians_table,
                               make_noise_image,
                                make_gaussian_sources_image)
from qiepian import Qie
sigma_psf = 2.0
sources = Table()
sources['flux'] = [3000]
sources['x_mean'] = [115]
sources['y_mean']=[594]
sources['x_stddev'] = sigma_psf*np.ones(1)
sources['y_stddev'] = sources['x_stddev']
sources['theta'] = [0]
sources['id'] = [1]
tshape = (700,700)
image = (make_gaussian_sources_image(tshape, sources) +
         make_noise_image(tshape, distribution='poisson', mean=6.,
                           seed=123) +
         make_noise_image(tshape, distribution='gaussian', mean=0.,
                          stddev=2., seed=123))
from matplotlib import rcParams
rcParams['font.size'] = 13
import matplotlib.pyplot as plt
plt.imshow(image, cmap='viridis', aspect=1, interpolation='nearest',
           origin='lower')
plt.title('Simulated data')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
from photutils.detection import IRAFStarFinder
from photutils.psf import IntegratedGaussianPRF, DAOGroup
from photutils.background import MMMBackground, MADStdBackgroundRMS
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.stats import gaussian_sigma_to_fwhm
bkgrms = MADStdBackgroundRMS()
std = bkgrms(image)
iraffind = IRAFStarFinder(threshold=3.5*std,
                        fwhm=sigma_psf*gaussian_sigma_to_fwhm,
                         minsep_fwhm=0.01, roundhi=5.0, roundlo=-5.0,
                         sharplo=0.0, sharphi=2.0)
daogroup = DAOGroup(2.0*sigma_psf*gaussian_sigma_to_fwhm)
mmm_bkg = MMMBackground()
fitter = LevMarLSQFitter()
psf_model = IntegratedGaussianPRF(sigma=sigma_psf)
psf_model.x_0.fixed = True
psf_model.y_0.fixed = True
pos = Table(names=['x_0', 'y_0'], data=[sources['x_mean'],
                                        sources['y_mean']])
from photutils.psf import BasicPSFPhotometry
photometry = BasicPSFPhotometry(group_maker=daogroup,
                                bkg_estimator=mmm_bkg,
                                psf_model=psf_model,
                                fitter=LevMarLSQFitter(),
                                fitshape=(11,11))

image = Qie()
result_tab = photometry(image=image,init_guesses=pos)
residual_image = photometry.get_residual_image()
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='viridis', aspect=1,
           interpolation='nearest', origin='lower')
plt.title('Real data')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
plt.subplot(1 ,2, 2)
plt.imshow(residual_image, cmap='viridis', aspect=1,
           interpolation='nearest', origin='lower')
plt.title('Residual Image')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
plt.show()


