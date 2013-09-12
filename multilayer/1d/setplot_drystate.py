#!/usr/bin/env python
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

import clawpack.pyclaw.solution

from multilayer.aux import bathy_index, kappa_index
import multilayer.plot as plot

# matplotlib.rcParams['figure.figsize'] = [6.0,10.0]

#--------------------------
def setplot(plotdata,rho,dry_tolerance):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """
    
    def jump_afteraxes(current_data):
        # Plot position of jump on plot
        mpl.hold(True)
        mpl.plot([0.5,0.5],[-10.0,10.0],'k--')
        mpl.plot([0.0,1.0],[0.0,0.0],'k--')
        mpl.hold(False)
        mpl.title('Layer Velocities')
        
    # Load bathymetery
    b = clawpack.pyclaw.solution.Solution(0, path=plotdata.outdir, 
                                         read_aux=True).state.aux[bathy_index,:]

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
    
    # Window Settings
    xlimits = [0.0,1.0]
    xlimits_zoomed = [0.45,0.55]
    ylimits_momentum = [-0.004,0.004]
    ylimits_depth = [-1.0,0.2]
    ylimits_depth_zoomed = ylimits_depth
    ylimits_velocities = [-0.75,0.75]
    ylimits_velocities_zoomed = ylimits_velocities
    
    # ========================================================================
    #  Depth and Momentum Plot
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Depth and Momentum')
    plotfigure.show = True
    
    def twin_axes(cd,xlimits):
        fig = mpl.gcf()
        fig.clf()
        
        # Get x coordinate values
        x = cd.patch.dimensions[0].centers
        
        # Create axes for each plot, sharing x axis
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212,sharex=ax1)     # the velocity scale
        
        # Bottom layer
        ax1.fill_between(x,bathy(cd),eta_1(cd),color=plot.bottom_color)
        # Top Layer
        ax1.fill_between(x,eta_1(cd),eta_2(cd),color=plot.top_color)
        # Plot bathy
        ax1.plot(x,bathy(cd),'k',linestyle=plot.bathy_linestyle)
        # Plot internal layer
        ax1.plot(x,eta_2(cd),'k',linestyle=plot.internal_linestyle)
        # Plot surface
        ax1.plot(x,eta_1(cd),'k',linestyle=plot.surface_linestyle)
        
        # Remove ticks from top plot
        locs,labels = mpl.xticks()
        labels = ['' for i in xrange(len(locs))]
        mpl.xticks(locs,labels)
        
        # ax1.set_title('')
        ax1.set_title('Solution at t = %3.2f' % cd.t)
        ax1.set_xlim(xlimits)
        ax1.set_ylim(ylimits_depth)
        # ax1.set_xlabel('x')
        ax1.set_ylabel('Depth (m)')
        
        # Bottom layer velocity
        bottom_layer = ax2.plot(x,u_2(cd),'k',linestyle=plot.internal_linestyle,label="Bottom Layer Velocity")
        # Top Layer velocity
        top_layer = ax2.plot(x,u_1(cd),'b',linestyle=plot.surface_linestyle,label="Top Layer velocity")

        # Add legend
        ax2.legend(loc=4)
        ax2.set_title('')
        # ax1.set_title('Layer Velocities')
        ax2.set_ylabel('Velocities (m/s)')
        ax2.set_xlabel('x (m)')
        ax2.set_xlim(xlimits)
        ax2.set_ylim(ylimits_velocities)
        
        # This does not work on all versions of matplotlib
        try:
            mpl.subplots_adjust(hspace=0.1)
        except:
            pass
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = lambda cd:twin_axes(cd,xlimits)
    
    # ========================================================================
    #  Fill plot zoom
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='full_zoom')
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = lambda cd:twin_axes(cd,xlimits_zoomed)
    
    # ========================================================================
    #  Momentum
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name="momentum")
    plotfigure.show = True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Momentum"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_momentum
    
    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = 1
    plotitem.plotstyle = 'b-'
    plotitem.show = True
    
    # Bottom layer 
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'k--'
    plotitem.show = True
    
    # ========================================================================
    #  h-values
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='depths')
    plotfigure.show = False
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,1)'
    plotaxes.title = 'Depths'
    plotaxes.xlimits = xlimits
    plotaxes.afteraxes = jump_afteraxes
    # plotaxes.ylimits = [-1.0,0.5]
    # plotaxes.xlimits = [0.45,0.55]
    # plotaxes.xlimits = [0.0,2000.0]
    # plotaxes.ylimits = [-2000.0,100.0]
     
    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = 0
    plotitem.plotstyle = '-'
    plotitem.color = (0.2,0.8,1.0)
    plotitem.show = True
    
    # Bottom layer
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = 2
    plotitem.color = 'b'
    plotitem.plotstyle = '-'
    plotitem.show = True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,2)'
    plotaxes.title = 'Depths Zoomed'
    plotaxes.afteraxes = jump_afteraxes
    # plotaxes.xlimits = [0.0,1.0]
    # plotaxes.ylimits = [-1.0,0.5]
    plotaxes.xlimits = [0.45,0.55]
    # plotaxes.xlimits = [0.0,2000.0]
    # plotaxes.ylimits = [-2000.0,100.0]
     
    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'x'
    plotitem.color = (0.2,0.8,1.0)
    plotitem.show = True
    
    # Bottom layer
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = 2
    plotitem.color = 'b'
    plotitem.plotstyle = '+'
    plotitem.show = True

    # ========================================================================
    #  Plot Layer Velocities
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='velocities')
    plotfigure.show = False
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(1,2,1)'
    plotaxes.title = "Layer Velocities"
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    
    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = u_1
    plotitem.color = 'b'
    plotitem.show = True
    
    # Bottom layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.color = (0.2,0.8,1.0)
    plotitem.plot_var = u_2
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

    
