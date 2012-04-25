
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import os

import numpy as np
import re

import matplotlib
import matplotlib.pyplot as mpl

from visclaw import geoplot, colormaps
from oldclawdata import Data

matplotlib.rcParams['figure.figsize'] = [16.0,6.0]

#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """
    
    claw_data = Data(os.path.join(plotdata.outdir,'claw.data'))
    prob_data = Data(os.path.join(plotdata.outdir,'problem.data'))

    def hurricane_afterframe(current_data):
        # Draw line for eye of hurricane
        pass

    def bathy(current_data):
        return np.loadtxt(os.path.join(plotdata.outdir,'fort.aux'),converters={0:(lambda x:float(re.compile("[Dd]").sub("e",x)))})
    
    def eta_2(current_data):
        h_2 = current_data.q[:,2]
        return h_2 + bathy(current_data)
        
    def eta_1(current_data):
        h_1 = current_data.q[:,0]
        return h_1 + eta_2(current_data)
        
    def u_1(current_data):
        h_1 = current_data.q[:,0]
        return (np.abs(h_1) > 1e-3) * current_data.q[:,1]/h_1[:]
        
    def u_2(current_data):
        h_2 = current_data.q[:,2]
        return (np.abs(h_2) > 1e-3) * current_data.q[:,3]/h_2[:]

    plotdata.clearfigures()  # clear any old figures,axes,items data
    
    xlimits = [claw_data.xlower,claw_data.xupper]
    ylimits_velocities = (-0.15,0.15)
    ylimits_depth = [-1.0,0.1]
    ylimits_wind = [-5,5]
    ylimits_kappa = [0.0,1.2]
    
    # ========================================================================
    #  Original Fill plot
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='full',figno=0)
    plotfigure.show = False
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,1)'
    plotaxes.title = 'Multilayer Surfaces'
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_depth
     
    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.plot_var = eta_1
    plotitem.plot_var2 = eta_2
    plotitem.color = (0.2,0.8,1.0)
    plotitem.show = True
    
    # Bottom Layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.plot_var = eta_2
    plotitem.plot_var2 = bathy
    plotitem.color = 'b'
    plotitem.show = True
    
    # Plot bathy
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = bathy
    plotitem.color = 'k'
    # plotitem.plotstyle = '-'
    plotitem.show = True
    
    # Plot line in between layers
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = eta_2
    plotitem.color = 'k'
    # plotitem.plotstyle = 'o'
    plotitem.show = True
    
    # Plot line on top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = eta_1
    plotitem.color = 'k'
    # plotitem.plotstyle = 'x'
    plotitem.show = True
    
    # Layer Velocities
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,2)'
    plotaxes.title = "Layer Velocities"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_velocities
    # plotaxes.afteraxes = jump_afteraxes
    
    # Bottom layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = u_2
    plotitem.color = 'b'
    plotitem.show = True

    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.color = (0.2,0.8,1.0)
    plotitem.plot_var = u_1
    plotitem.show = True
    
    # ========================================================================
    #  Fill plot with Kappa
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='full_kappa',figno=14)
    
    def twin_axes(cd):
        fig = mpl.gcf()
        fig.clf()
        
        x = cd.grid.dimensions[0].center
        
        # Draw fill plot
        ax1 = fig.add_subplot(121)
        
        # Bottom layer
        ax1.fill_between(x,bathy(cd),eta_1(cd),color='b')
        # Top Layer
        ax1.fill_between(x,eta_1(cd),eta_2(cd),color=(0.2,0.8,1.0))
        # Plot bathy
        ax1.plot(x,bathy(cd),'k')
        # Plot internal layer
        ax1.plot(x,eta_2(cd),'k')
        # Plot surface
        ax1.plot(x,eta_1(cd),'k')
        
        ax1.set_title('Multilayer Surfaces t = %s' % cd.t)
        ax1.set_xlim((0.0,1.0))
        ax1.set_ylim((-1.0,0.2))
        ax1.set_xlabel('x')
        ax1.set_ylabel('Depth')
        
        # Draw velocity and kappa plot
        ax1 = fig.add_subplot(122)     # the velocity scale
        ax2 = ax1.twinx()              # the kappa scale
        
        # Bottom layer velocity
        bottom_layer = ax1.plot(x,u_2(cd),'k-',label="Bottom Layer Velocity")
        # Top Layer velocity
        top_layer = ax1.plot(x,u_1(cd),'b-',label="Top Layer velocity")#,color=(0.2,0.8,1.0))
        
        # Kappa
        kappa_line = ax2.plot(x,cd.q[:,5],color='r',label="Kappa")
        ax2.plot(x,np.ones(x.shape),'r--')
        
        ax1.legend((bottom_layer,top_layer,kappa_line),('Bottom Layer','Top Layer',"Kappa"),loc=4)
        ax1.set_xlim(xlimits)
        ax1.set_ylim(ylimits_velocities)
        ax2.set_ylim(ylimits_kappa)
        ax1.set_title('Layer Velocities and Kappa')
        ax1.set_ylabel('Velocities (m/s)')
        ax2.set_ylabel('Kappa (1/Ri)')
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = twin_axes
    

    # ========================================================================
    #  Plot Layer Velocities
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='velocities',figno=1)
    plotfigure.show = True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(1,2,1)'
    plotaxes.title = "Layer Velocities"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_velocities
    
    # Bottom layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = u_2
    plotitem.color = 'b'
    plotitem.show = True

    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.color = (0.2,0.8,1.0)
    plotitem.plot_var = u_1
    plotitem.show = True
    
    # Wind plot
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(1,2,2)'
    plotaxes.title = "Wind Velocity"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_wind
    
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 4
    plotitem.color = 'r'
    plotitem.show = True
    
    # ========================================================================
    #  Plot Wind Velocity
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='wind',figno=2)
    plotfigure.show = True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Wind Velocity"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_wind
    
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 4
    plotitem.color = 'r'
    plotitem.show = True
    
    # ========================================================================
    #  Plot Kappa
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name="kappa",figno=13)
    plotfigure.show = True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Discrete Richardson Number"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_kappa
    
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 5
    plotitem.color = 'b'
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

    
