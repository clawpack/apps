"""
Plot fgmax output from GeoClaw runs, assuming points are on transect.

"""


from pylab import *
from numpy import ma
import os

def make_plots(outdir='_output', plotdir='_plots'):

    # Some things that might need to change...

    plot_zeta = True
    plot_arrival_times = True

    fgmax_input_file = 'fgmax_transect.txt'



    if not os.path.isdir(outdir):
        raise Exception("Missing directory: %s" % outdir)

    if not os.path.isdir(plotdir):
        os.mkdir(plotdir)

    print outdir
    print fgmax_input_file

    # read mx and my from the input file:
    try:
        fid = open(fgmax_input_file)
    except:
        raise Exception("cannot open %s" % fgmax_input_file)

    # skip some lines:
    for i in range(6):
        line = fid.readline()

    line = fid.readline().split()
    fid.close()
    npts = int(line[0])

    fname = outdir + '/fort.FG2.valuemax' 
    print "Reading %s ..." % fname
    try:
        d = loadtxt(fname)
    except:
        raise Exception("*** Cannot read file: %s" % fname)

    x = d[:,0]
    y = d[:,1]
    y0 = 0.5*(y.min() + y.max())   # mid-latitude for scaling plots
    eta_tilde = d[:,3]

    # AMR level used for each zeta value:
    level = array(d[:,2], int)
    
    # Determine topo B at each point from the same level of AMR:
    fname = outdir + '/fort.FG2.aux1' 
    print "Reading %s ..." % fname
    daux = loadtxt(fname)
    topo = []
    nlevels = daux.shape[1]
    for i in range(2,nlevels):
        topoi = daux[:,i]
        topoi = ma.masked_where(topoi < -1e50, topoi)
        topo.append(topoi)

    B = ma.masked_where(level==0, topo[0])  # level==0 ==> never updated
    levelmax = level.max()
    for i in range(levelmax):
        B = where(level==i+1, topo[i], B)

    h = where(eta_tilde > B, eta_tilde - B, 0.)


    # zeta = max h on land or max eta offshore:
    zeta = where(B>0, h, eta_tilde)

    tzeta = d[:,4]  # Time maximum h recorded
    tzeta = ma.masked_where(tzeta < -1e50, tzeta)      
    tzeta = ma.masked_where(zeta == 0., tzeta) / 3600.  # hours 

    inundated = logical_and((B>0), (h>0))

    atimes = d[:,5]
    atimes = ma.masked_where(atimes < -1e50, atimes)  
    atimes = ma.masked_where(zeta == 0., atimes) / 3600.  # hours 

    if plot_zeta:

        # Plot h or eta along with topo:
        figure(101)
        clf()
        zeta = ma.masked_where(zeta==0.,zeta)
        subplot(211)
        plot(x,zeta)
        title("Zeta Maximum at Latitude %g" % y[0])
        xlabel("Longitude")

        subplot(212)
        plot(x,zeta)
        plot(x,B,'g')  # topo
        title("Topography at Latitude %g" % y[0])
        xlabel("Longitude")
        
        fname = plotdir + '/zeta_transect.png' 
        savefig(fname)
        print "Created ",fname


    if plot_arrival_times:

        # Plot time max h recorded:
        figure(103)
        clf()

        plot(x,atimes)
        title("Arrival time at Latitude %g" % y[0])
        xlabel("Longitude")
        ylabel("Hours")
        fname = plotdir + '/arrival_times_transect.png' 
        savefig(fname)
        print "Created ",fname


if __name__ == "__main__":
    make_plots()
