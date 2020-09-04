"""
Plot fgmax output from GeoClaw run.

"""

import matplotlib.pyplot as plt
import numpy
from clawpack.geoclaw import fgmax_tools
from clawpack.visclaw import  geoplot
from numpy import ma  # masked arrays

dry_tolerance = 1e-2   # smaller h treated as dry

def plot_fgmax_grid(fgno):

    fg = fgmax_tools.FGmaxGrid()
    fg.read_fgmax_grids_data(fgno=fgno)
    fg.read_output()

    clines_zeta = [0.01] + list(numpy.linspace(.3, 2.1, 7))
    colors = geoplot.discrete_cmap_1(clines_zeta)
    plt.figure(fgno)
    plt.clf()

    # set zeta = max depth on shore, max surface elevation offshore:
    zeta = numpy.where(fg.B>0, fg.h, fg.h+fg.B)   

    plt.contourf(fg.X,fg.Y,zeta,clines_zeta,colors=colors,extend='max')
    plt.colorbar(extend='max')
    #plt.contour(fg.X,fg.Y,fg.B,[0.],colors='k')  # coastline

    # plot original coastline extending beyond fgmax region:
    theta = numpy.linspace(-numpy.pi/8., 3/8. *numpy.pi, 1000)
    plt.plot(90*numpy.cos(theta), 90*numpy.sin(theta), 'k')

    # fix axes:
    plt.ticklabel_format(useOffset=False)
    plt.xticks(rotation=20)
    plt.gca().set_aspect(1./numpy.cos(fg.Y.mean()*numpy.pi/180.))
    plt.title("Zeta = max depth or surface elevation")
    plt.axis('scaled')
    if fgno==1:
        plt.axis([85,95,-5,5])
    else:
        plt.axis([59,69,59,69])

def plot_fgmax_transects():

    # === Transect on x-axis:
    fg = fgmax_tools.FGmaxGrid()
    fg.read_fgmax_grids_data(fgno=3)
    fg.read_output()

    plt.figure(3)
    plt.clf()

    surface = ma.masked_where(fg.h < dry_tolerance, fg.B+fg.h)
    sea_level = 0.
    surface_original = ma.masked_where(fg.B > 0, sea_level*numpy.ones(fg.B.shape))

    # distance along transect:
    xi = numpy.sqrt((fg.X-fg.X[0])**2 + (fg.Y-fg.Y[0])**2)  

    plt.plot(xi, fg.B, 'g')    # topography
    plt.plot(xi,surface_original, 'k')
    plt.plot(xi,surface, 'b', label="along x-axis")

    # === Transect on diagonal:
    fg = fgmax_tools.FGmaxGrid()
    fg.read_fgmax_grids_data(fgno=4)
    fg.read_output()

    surface = ma.masked_where(fg.h < dry_tolerance, fg.B+fg.h)

    xi = numpy.sqrt((fg.X-fg.X[0])**2 + (fg.Y-fg.Y[0])**2)  
    plt.plot(xi,surface, 'r', label="along diagonal")
    plt.legend(loc="lower right")

    plt.title("Max elevation along transects vs distance")

    # === Along shoreline:
    fg = fgmax_tools.FGmaxGrid()
    fg.read_fgmax_grids_data(fgno=5)
    fg.read_output()
    plt.figure(5)
    theta = numpy.arctan(fg.Y / fg.X)
    plt.plot(theta,  fg.h, 'b')
    plt.title("Max elevation along shore (radius 90 m) vs angle")
    plt.xticks([0,numpy.pi/4.], ['0','pi/4'])
    plt.xlabel('theta')
    plt.ylabel('meters')


if __name__=="__main__":

    import os
    plotdir = '_plots'
    if not os.path.isdir(plotdir): 
        os.mkdir(plotdir)

    plot_fgmax_grid(1)
    plt.figure(1)
    fname = os.path.join(plotdir, "fgmax_grid1.png")
    plt.savefig(fname)
    print("Created ",fname)

    plot_fgmax_grid(2)
    plt.figure(2)
    fname = os.path.join(plotdir, "fgmax_grid2.png")
    plt.savefig(fname)
    print("Created ",fname)

    plot_fgmax_transects()
    plt.figure(3)
    fname = os.path.join(plotdir, "fgmax_transects.png")
    plt.savefig(fname)
    print("Created ",fname)

    plt.figure(5)
    fname = os.path.join(plotdir, "fgmax_along_shore.png")
    plt.savefig(fname)
    print("Created ",fname)


