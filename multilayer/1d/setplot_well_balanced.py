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

from clawpack.pyclaw.solution import Solution
from clawpack.visclaw import geoplot, colormaps
from clawpack.clawutil.oldclawdata import Data

from multilayer.aux import bathy_index,kappa_index,wind_index
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
    
    
    # Load bathymetry
    b = Solution(0,path=plotdata.outdir,read_aux=True).state.aux[bathy_index,:]

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
    
    
    def jump_afteraxes(current_data):
        # Plot position of jump on plot
        mpl.hold(True)
        mpl.plot([0.5,0.5],[-10.0,10.0],'k--')
        mpl.plot([0.0,1.0],[0.0,0.0],'k--')
        mpl.hold(False)
        mpl.title('')

    plotdata.clearfigures()  # clear any old figures,axes,items data
    
    # Window Settings
    xlimits = [0.0,10.0]
    ylimits_depth = [-10.5,0.5]
    
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
        # km_labels(cd)
        mpl.xlabel('Depth (m)')
        mpl.ylabel('x (m)')
        mpl.title("Depths at t=%2.1f" % cd.t)
        # mpl.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
        # mpl.xlabel('km')
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Full Depths'
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_depth
    plotaxes.afteraxes = bathy_axes
    
    fill_items(plotaxes)

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    # plotdata.print_framenos = [0,25,50]      # list of frames to print
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
