
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import os

import numpy as np

# Plot customization
import matplotlib

# Markers and line widths
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['lines.markersize'] = 8

# Font Sizes
matplotlib.rcParams['font.size'] = 16
matplotlib.rcParams['axes.labelsize'] = 15
matplotlib.rcParams['legend.fontsize'] = 12
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12

# DPI of output images
matplotlib.rcParams['savefig.dpi'] = 100

# Need to do this after the above
import matplotlib.pyplot as mpl

from clawpack.pyclaw.solution import Solution
from clawpack.visclaw import geoplot, colormaps
from clawpack.clawutil.oldclawdata import Data

from multilayer.aux import bathy_index,kappa_index,wind_index
import multilayer.plot as plot

#--------------------------
def setplot(plotdata,xlower,xupper,rho,dry_tolerance):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """
    
    # Load bathymetry
    b = Solution(0,path=plotdata.outdir,read_aux=True).state.aux[bathy_index,:]

    def hurricane_afterframe(current_data):
        # Draw line for eye of hurricane
        pass
        
    def bathy(cd):
        return b
    
    def kappa(cd):
        return Solution(cd.frameno,path=plotdata.outdir,read_aux=True).state.aux[kappa_index,:]

    def wind(cd):
        return Solution(cd.frameno,path=plotdata.outdir,read_aux=True).state.aux[wind_index,:]
    
    def h_1(cd):
        return cd.q[0,:] / rho[0]
    
    def h_2(cd):
        return cd.q[2,:] / rho[1]
        
    def eta_2(cd):
        return h_2(cd) + bathy(cd)
        
    def eta_1(cd):
        return h_1(cd) + eta_2(cd)
        
    def u_1(cd):
        index = np.nonzero(h_1(cd) > dry_tolerance)
        u_1 = np.zeros(h_1(cd).shape)
        u_1[index] = cd.q[1,index] / cd.q[0,index]
        return u_1
        
    def u_2(cd):
        index = np.nonzero(h_2(cd) > dry_tolerance)
        u_2 = np.zeros(h_2(cd).shape)
        u_2[index] = cd.q[3,index] / cd.q[2,index]
        return u_2


    plotdata.clearfigures()  # clear any old figures,axes,items data
    
    xlimits = [xlower,xupper]
    ylimits_velocities = (-0.15,0.15)
    ylimits_depth = [-1.0,0.1]
    ylimits_wind = [-5,5]
    ylimits_kappa = [0.0,1.2]
    
    # ========================================================================
    #  Depth, Momenta, and Kappa
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Depth, Momenta, and Kappa',figno=14)
    
    def twin_axes(cd):
        fig = mpl.gcf()
        fig.clf()
        
        # Get x coordinate values
        x = cd.patch.dimensions[0].centers
        
        # Draw fill plot
        depth_axes = fig.add_subplot(211)
        vel_axes = fig.add_subplot(212,sharex=depth_axes)     # the velocity scale
        kappa_axes = vel_axes.twinx()
        
        # Bottom layer
        depth_axes.fill_between(x,bathy(cd),eta_1(cd),color=plot.bottom_color)
        # Top Layer
        depth_axes.fill_between(x,eta_1(cd),eta_2(cd),color=plot.top_color)
        # Plot bathy
        depth_axes.plot(x,bathy(cd),'k',linestyle=plot.bathy_linestyle)
        # Plot internal layer
        depth_axes.plot(x,eta_2(cd),'k',linestyle=plot.internal_linestyle)
        # Plot surface
        depth_axes.plot(x,eta_1(cd),'k',linestyle=plot.surface_linestyle)
        
        # Remove ticks from top plot
        locs,labels = mpl.xticks()
        labels = ['' for i in xrange(len(locs))]
        mpl.xticks(locs,labels)
        
        depth_axes.set_title('Oscillatory Wind at t = %3.2f' % cd.t)
        depth_axes.set_xlim(xlimits)
        depth_axes.set_ylim(ylimits_depth)
        depth_axes.set_ylabel('Depth (m)')
        
        # Draw velocity and kappa plot
        
        # Bottom layer velocity
        bottom_layer = vel_axes.plot(cd.x,u_2(cd),'k-',label="Bottom Layer Velocity")
        # Top Layer velocity
        top_layer = vel_axes.plot(cd.x,u_1(cd),'b--',label="Top Layer velocity")
        
        # Kappa
        kappa_line = kappa_axes.plot(cd.x,kappa(cd),'r-.')
        kappa_axes.plot(cd.x,np.ones(cd.x.shape),'r:')
        
        plot.add_legend(vel_axes,'Kappa',color='r',linestyle='-.',location=4)
        vel_axes.set_xlim(xlimits)
        vel_axes.set_ylim(ylimits_velocities)
        kappa_axes.set_ylim(ylimits_kappa)
        vel_axes.set_title('')
        # vel_axes.set_title('Layer Velocities and Kappa')
        vel_axes.set_ylabel('Velocities (m/s)')
        kappa_axes.set_ylabel('Kappa')
        
        # This does not work on all versions of matplotlib
        try:
            mpl.subplots_adjust(hspace=0.1)
        except:
            pass
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = twin_axes
    
    # ========================================================================
    #  Plot Wind Velocity
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Wind Field',figno=2)
    plotfigure.show = True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Wind Velocity"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_wind
    plotaxes.xlabel = "x (m)"
    plotaxes.ylabel = "Velocity (m/s)"
    
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = wind
    plotitem.color = 'r'
    plotitem.show = True
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
