from numpy import *
from astropy.io import fits

def createFITS(data, inwcs, outfile): #function to create the FITS header
    hdu1 = fits.PrimaryHDU()
    hdu  = fits.HDUList([hdu1])
    hdu[0].data = data
    
    data = hdu[0].data
    header = hdu[0].header
    
    header.set('RADESYS', 'FK5')
    header.set('EQUINOX', 2000.)
    header.set('NAXIS1', nx)
    header.set('NAXIS2', ny)
    
    header.set('CRPIX1', x0)
    header.set('CRPIX2', y0)
    header.set('CRVAL1', RA0)
    header.set('CRVAL2', Dec0)
    CD1 = -pixdeg
    CD2 =  pixdeg
    header.set('CD1_1',  float(CD1))
    header.set('CD2_2',  float(CD2))
    header.set('CDELT1', float(CD1))
    header.set('CDELT2', float(CD2))
    header.set('CD1_2', 0.)
    header.set('CD2_1', 0.)
    header.set('LTM1_1', 1.)  # image -> physical coordinates
    header.set('LTM1_2', 1.)  # image -> physical coordinates
    header.set('CTYPE1', 'RA---TAN')
    header.set('CTYPE2', 'DEC--TAN')
    
    data = data.astype(float32)
    header.set('BITPIX', -32)
    
    hdu[0].data = data
    hdu[0].header = header
    hdu.writeto(outfile)

# Define the input and output filepaths
infile  = 'input.dat' #structured data file as input
outfile = 'output.fits' #edit your output file name

# Restructure the data for the FITS
data = loadtxt(infile)
N, nvar = data.shape
ny = nx = int(round(sqrt(N))) #comment this line if input is a square array
data.shape = nx, ny, nvar
data = data.T  # nvar, ny, nx
data = data[:,:,::-1]  # flip RA: increases right to left
x, y, var = data  #Change if needed, x and y are in arcsec


# Define the pixel separation used
pixarcsec = y[1,0] - y[0,0]  # should be in arcsec
pixdeg = pixarcsec / 3600. # convert into degrees

# Define the reference pixel and corresponding RA and dec
x0 = nx / 2.
y0 = ny / 2.
RA0 = 40.00                # Change if needed, "should be in degrees"
Dec0 = -1.500               # Change if needed

inwcs = x0, y0, RA0, Dec0, pixdeg

# Use the createFITS function to generate the fits file
createFITS(var, inwcs, outfile)



