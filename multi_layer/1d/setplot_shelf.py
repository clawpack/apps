
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

from multilayer.aux import bathy_index,kappa_index,wind_index
import multilayer.plot as plot

# matplotlib.rcParams['figure.figsize'] = [6.0,10.0]

def setplot(plotdata,eta=[0.0,-300.0],rho=[1025.0,1045.0],g=9.81,dry_tolerance=1e-3,bathy_ref_lines=[-30e3]):
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """
    
    # Fetch bathymetry once
    b = Solution(0,path=plotdata.outdir,read_aux=True).state.aux[bathy_index,:]
    
    # ========================================================================
    #  Plot variable functions
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
            
    # ========================================================================
    #  Labels    
    def add_bathy_dashes(current_data):
        mpl.hold(True)
        for ref_line in bathy_ref_lines:
            mpl.plot([ref_line,ref_line],[-10,10],'k--')
        mpl.hold(False)
        
    def add_horizontal_dashes(current_data):
        mpl.hold(True)
        mpl.plot([-400e3,0.0],[0.0,0.0],'k--')
        mpl.hold(False)

    def km_labels(current_data):
        r"""Flips xaxis and labels with km"""
        mpl.xlabel('km')
        locs,labels = mpl.xticks()
        labels = np.flipud(locs)/1.e3
        mpl.xticks(locs,labels)
        
    def time_labels(current_data):
        r"""Convert time to hours"""
        pass
        
    
    # ========================================================================
    # Limit Settings
    xlimits = [-400e3,0.0]
    ylimits_depth = [-4000.0,100.0]
    xlimits_zoomed = [-30e3-1e3,-30e3+1e3]
    ylimits_surface_zoomed = [eta[0] - 0.5,eta[0] + 0.5]
    ylimits_internal_zoomed = [eta[1] - 2.5,eta[1] + 2.5] 
    # ylimits_velocities = [-1.0,1.0]
    ylimits_velocities = [-0.04,0.04]
    ylimits_kappa = [0.0,1.2]
        
    # Create data object
    plotdata.clearfigures()  # clear any old figures,axes,items data
    
    # ========================================================================
    #  Function for doing depth drawing
    # ========================================================================
    def fill_items(plotaxes):
        # Top layer
        plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
        plotitem.plot_var = eta_1
        plotitem.plot_var2 = eta_2
        plotitem.color = plot.top_color
        plotitem.plotstyle = plot.surface_linestyle
        plotitem.show = True
    
        # Bottom Layer
        plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
        plotitem.plot_var = eta_2
        plotitem.plot_var2 = bathy
        plotitem.color = plot.bottom_color
        plotitem.plotstyle = plot.internal_linestyle
        plotitem.show = True
    
        # Plot bathy
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = bathy
        plotitem.plotstyle = plot.bathy_linestyle
        plotitem.show = True
            
        # Plot line in between layers
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = eta_2
        plotitem.color = 'k'
        plotitem.plotstyle = plot.internal_linestyle
        plotitem.show = True
    
        # Plot line on top layer
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = eta_1
        plotitem.color = 'k'
        plotitem.plotstyle = plot.surface_linestyle
        plotitem.show = True
    
    # ========================================================================
    #  Full Depths
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Full Depths',figno=102)
    plotfigure.show = True
    
    def bathy_axes(cd):
        km_labels(cd)
        mpl.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
        mpl.xlabel('km')
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Full Depths'
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = [-4100,100]
    plotaxes.afteraxes = bathy_axes
    
    fill_items(plotaxes)
    
    # ========================================================================
    #  Velocities with Kappa
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Velocity and Kappa',figno=14)
    plotfigure.show = True
    # plotfigure.kwargs = {'figsize':(7,6)}
    
    def twin_axes(cd):
        fig = mpl.gcf()
        fig.clf()

        # Get x coordinate values
        x = cd.patch.dimensions[0].centers
        
        # Draw velocity and kappa plot
        vel_axes = fig.add_subplot(111)     # the velocity scale
        # kappa_axes = vel_axes.twinx()              # the kappa scale
        
        # Bottom layer velocity
        bottom_layer = vel_axes.plot(x,u_2(cd),'k-',label="Bottom Layer Velocity")
        # Top Layer velocity
        top_layer = vel_axes.plot(x,u_1(cd),'b--',label="Top Layer velocity")
        
        # Kappa
        # kappa_line = kappa_axes.plot(x,kappa(cd),'r-.',label="Kappa")
        # kappa_axes.plot(x,np.ones(x.shape),'r:')

        vel_axes.set_xlabel('km')
        mpl.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
        
        for ref_line in bathy_ref_lines:
            vel_axes.plot([ref_line,ref_line],ylimits_velocities,'k:')
        # plot.add_legend(vel_axes,'Kappa',location=3,color='r',linestyle='-.')
        vel_axes.set_title("Layer Velocities and Kappa at t = %4.1f s" % cd.t)
        vel_axes.set_ylabel('Velocities (m/s)')
        # kappa_axes.set_ylabel('Kappa')
        vel_axes.set_xlim(xlimits)
        vel_axes.set_ylim(ylimits_velocities)
        # kappa_axes.set_ylim(ylimits_kappa)
        
        try:
            mpl.subplots_adjust(hspace=0.1)
        except:
            pass
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = twin_axes
    
    # ========================================================================
    #  Combined Top and Internal Surface
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Zoomed Depths',figno=13)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize':(6,6)}
    
    # Top surface
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,1)'
    plotaxes.title = 'Surfaces'
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_surface_zoomed
    def top_afteraxes(cd):
        mpl.xlabel('')
        locs,labels = mpl.xticks()
        # labels = np.flipud(locs)/1.e3
        labels = ['' for i in xrange(len(locs))]
        mpl.xticks(locs,labels)
        add_bathy_dashes(cd)
        mpl.ylabel('m')
        mpl.title("Surfaces t = %4.1f s" % cd.t)
    plotaxes.afteraxes = top_afteraxes
    plotaxes = fill_items(plotaxes)
    
    # Internal surface
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,2)'
    plotaxes.title = ''
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_internal_zoomed
    def internal_surf_afteraxes(cd):
        km_labels(cd)
        mpl.title('')
        mpl.ylabel('m')
        mpl.subplots_adjust(hspace=0.05)
        mpl.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
        mpl.xlabel('km')
    plotaxes.afteraxes = internal_surf_afteraxes
    plotaxes = fill_items(plotaxes)
    
    
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    # plotdata.print_framenos = [0,30,100,200,300]
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
