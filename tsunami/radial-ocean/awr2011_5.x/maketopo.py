
"""
Module to create topo and qinit data files for this example.
"""

from clawpack.geoclaw import topotools
from clawpack.geoclaw.data import Rearth  # radius of earth
from interp import pwcubic
from clawpack.clawutil.data import ClawData
from numpy import *

from mapper import latlong, gcdist

probdata = ClawData()
probdata.read('setprob.data', force=True)
theta_island = probdata.theta_island
print "theta_island = ",theta_island

(xisland,yisland) = latlong(1600.e3, theta_island, 40., Rearth)

def maketopo():
    """
    Output topography file for the entire domain
    and near-shore in one location.
    """
    nxpoints=400
    nypoints=400
    xlower=-20.e0
    xupper= 20.e0
    ylower= 20.e0
    yupper= 60.e0
    outfile= "ocean.topotype2"
    topotools.topo2writer(outfile,topo,xlower,xupper,ylower,yupper,nxpoints,nypoints)

    nxpoints=200
    nypoints=200
    xlower= xisland - 1.
    xupper= xisland + 1.
    ylower= yisland - 1.
    yupper= yisland + 1.
    outfile= "island.topotype2"
    topotools.topo2writer(outfile,topo,xlower,xupper,ylower,yupper,nxpoints,nypoints)

def makeqinit():
    """
    Create qinit data file
    """
    nxpoints=100
    nypoints=100
    xlower=-20.e0
    xupper= 20.e0
    ylower= 20.e0
    yupper= 60.e0
    outfile= "hump.xyz"
    topotools.topo1writer(outfile,qinit,xlower,xupper,ylower,yupper,nxpoints,nypoints)

def shelf1(r):
    """
    Ocean followed by continental slope, continental shelf, and beach.
    The ocean is flat, the slope is cubic, and the shelf and beach are linear.
    """

    rad1 = 1500e3         # beginning of continental slope
    rad2 = rad1 + 60e3   # end of slope, start of shelf
    rad3 = rad2 + 80e3   # end of shelf, start of beach
    rad4 = rad3 + 5e3    # radius of shoreline where z=0
    z1 = -4000.          # depth from r=0  to rad1 (ocean)
    z2 = -100.           # depth at r=rad2 (start of shelf)
    z3 = -100.           # depth at r=rad3 (start of beach)
    z4 = 0.              # depth at shoreline
    xi = array([0., rad1, rad2, rad3, rad4])
    zl = array([z1, z1, z2, z3, z4])
    zr = zl  # continuous!
    slope_of_shelf = (z3 - z2) / (rad3 - rad2)
    slope_of_beach = (z4 - z3) / (rad4 - rad3)
    print "Slope of shelf = ",slope_of_shelf
    print "Slope of beach = ",slope_of_beach
    slopel = array([0., 0., slope_of_shelf, slope_of_shelf, slope_of_beach])
    sloper = array([0., 0., slope_of_shelf, slope_of_beach, slope_of_beach])
    z = pwcubic(xi, zl, zr, slopel, sloper, r)
    return z

def island1(r):
    """
    Island created using piecewise cubic with radius rad with zero slope at peak and
    base. Raises topo by ztop at the peak.
    """
    rad = 30e3
    ztop = 120.  # 20m above sealevel on the 100m deep shelf.
    xi = array([0., rad])
    zl = array([ztop, 0.])
    zr = zl
    slopel = array([0., 0.])
    sloper = slopel
    z = pwcubic(xi, zl, zr, slopel, sloper, r)
    return z

def topo(x,y):
    """
    x = longitude, y = latitude in degrees
    """
    import numpy as np
    x0 = 0.0
    y0 = 40.0
    d = gcdist(x0,y0,x,y,Rearth)
    z = shelf1(d)
    d = gcdist(xisland,yisland,x,y,Rearth)
    z = z + island1(d)
    z = where(z>200, 200, z)   # cut off topo at 200 m above sea level
    return z


def qinit(x,y):
    """
    Gaussian hump:
    """
    from numpy import where
    x0 = 0.0
    y0 = 40.0
    d = gcdist(x0,y0,x,y,Rearth)
    ze = -d**2/2.e9
    z = where(ze>-100., 20.e0*exp(ze), 0.)
    return z

if __name__=='__main__':
    maketopo()
    makeqinit()
