"""
This script creates the following files in the $CLAW/geoclaw/scratch
directory:

  - etopo1_-140_-60_-60_10_4min.tt3    

    4-minute resolution resolution topography/bathymetry from the
    etopo1 data set. See http://www.ngdc.noaa.gov/mgg/global/global.html

    This is finer bathymetry than the 10-second bathymetry used in the 
    original GeoClaw example chile2010 and is now downloaded 
    directly from NCEI (if the file does not already exist locally)
    using the GeoClaw etopotools.py module.
                       
  - dtopo_usgs100227.tt3

    Seafloor deformation file created using the Okada model as implemented
    in the GeoClaw dtopotools.py module.

Call functions with makeplots==True to create plots of topo, slip, and dtopo.
"""

import os

import clawpack.clawutil.data

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")


# Scratch directory for storing topo and dtopo files:
scratch_dir = os.path.join(CLAW, 'geoclaw', 'scratch')


def get_topo(makeplots=False):
    """
    Retrieve the topo file from the GeoClaw repository.
    """
    from clawpack.geoclaw import topotools, etopotools

    topo_fname = 'etopo1_-140_-60_-60_10_10min.tt3'

    if os.path.exists(topo_fname):
        print "*** Not regenerating dtopo file (already exists): %s" \
                    % dtopo_fname
    else:
        xlimits = (-140,-60)
        ylimits = (-60,10)
        resolution = 10./60.   # degrees

        topo = etopotools.etopo1_download(xlimits,ylimits, dx=resolution, \
                output_dir=scratch_dir, file_name=topo_fname, return_topo=True)

    if makeplots:
        from matplotlib import pyplot as plt
        topo = topotools.Topography(os.path.join(scratch_dir,topo_fname), topo_type=2)
        topo.plot()
        fname = os.path.splitext(topo_fname)[0] + '.png'
        plt.savefig(fname)
        print "Created ",fname




def make_dtopo(makeplots=False):
    """
    Create dtopo data file for deformation of sea floor due to earthquake.
    Uses the Okada model with fault parameters and mesh specified below.
    """
    from clawpack.geoclaw import dtopotools
    import numpy

    dtopo_fname = os.path.join(scratch_dir, "dtopo_usgs100227.tt3")

    # Specify subfault parameters for this simple fault model consisting
    # of a single subfault:

    usgs_subfault = dtopotools.SubFault()
    usgs_subfault.strike = 16.
    usgs_subfault.length = 450.e3
    usgs_subfault.width = 100.e3
    usgs_subfault.depth = 35.e3
    usgs_subfault.slip = 15.
    usgs_subfault.rake = 104.
    usgs_subfault.dip = 14.
    usgs_subfault.longitude = -72.668
    usgs_subfault.latitude = -35.826
    usgs_subfault.coordinate_specification = "top center"

    fault = dtopotools.Fault()
    fault.subfaults = [usgs_subfault]

    print "Earthquake moment magnitude Mw = %5.2f" % fault.Mw()

    if os.path.exists(dtopo_fname):
        print "Not regenerating dtopo file (already exists): %s" \
                    % dtopo_fname
    else:
        print "Using Okada model to create dtopo file"

        x = numpy.linspace(-77, -67, 100)
        y = numpy.linspace(-40, -30, 100)
        times = [1.]

        fault.create_dtopography(x,y,times)
        dtopo = fault.dtopo
        dtopo.write(dtopo_fname, dtopo_type=3)


    if makeplots:
        from matplotlib import pyplot as plt
        if fault.dtopo is None:
            # read in the pre-existing file:
            print "Reading in dtopo file..."
            dtopo = dtopotools.DTopography()
            dtopo.read(dtopo_fname, dtopo_type=3)
            x = dtopo.x
            y = dtopo.y
        plt.figure(figsize=(12,7))
        ax1 = plt.subplot(121)
        ax2 = plt.subplot(122)
        fault.plot_subfaults(axes=ax1,slip_color=True)
        ax1.set_xlim(x.min(),x.max())
        ax1.set_ylim(y.min(),y.max())
        dtopo.plot_dz_colors(1.,axes=ax2)
        fname = os.path.splitext(dtopo_fname)[0] + '.png'
        plt.savefig(fname)
        print "Created ",fname


if __name__=='__main__':
    get_topo(False)
    make_dtopo(False)
