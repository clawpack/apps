
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

from clawpack.pyclaw.solution import Solution
from clawpack.visclaw import geoplot, colormaps
from clawpack.clawutil.oldclawdata import Data



matplotlib.rcParams['figure.figsize'] = [16.0,6.0]

#--------------------------
def setplot(plotdata,xlower,xupper,rho,dry_tolerance):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """
    
    # Legacy fortran output in q
    # 0,1,2,3,4,5 = h(1),hu(1),h(2),hu(2),wind,kappa
    
    # Load bathymetry
    b = Solution(0,path=plotdata.outdir,read_aux=True).state.aux[0,:]

    def hurricane_afterframe(current_data):
        # Draw line for eye of hurricane
        pass
        
    def bathy(cd):
        return b
    
    def kappa(cd):
        return Solution(cd.frameno,path=plotdata.outdir,read_aux=True).state.aux[4,:]

    def wind(cd):
        return Solution(cd.frameno,path=plotdata.outdir,read_aux=True).state.aux[1,:]
    
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
        
        # Draw fill plot
        ax1 = fig.add_subplot(121)
        
        # Bottom layer
        ax1.fill_between(cd.x,bathy(cd),eta_1(cd),color='b')
        # Top Layer
        ax1.fill_between(cd.x,eta_1(cd),eta_2(cd),color=(0.2,0.8,1.0))
        # Plot bathy
        ax1.plot(cd.x,bathy(cd),'k')
        # Plot internal layer
        ax1.plot(cd.x,eta_2(cd),'k')
        # Plot surface
        ax1.plot(cd.x,eta_1(cd),'k')
        
        ax1.set_title('Multilayer Surfaces t = %s' % cd.t)
        ax1.set_xlim((0.0,1.0))
        ax1.set_ylim((-1.0,0.2))
        ax1.set_xlabel('x')
        ax1.set_ylabel('Depth')
        
        # Draw velocity and kappa plot
        ax1 = fig.add_subplot(122)     # the velocity scale
        ax2 = ax1.twinx()              # the kappa scale
        
        # Bottom layer velocity
        bottom_layer = ax1.plot(cd.x,u_2(cd),'k-',label="Bottom Layer Velocity")
        # Top Layer velocity
        top_layer = ax1.plot(cd.x,u_1(cd),'b-',label="Top Layer velocity")#,color=(0.2,0.8,1.0))
        
        # Kappa
        kappa_line = ax2.plot(cd.x,kappa(cd),color='r',label="Kappa")
        ax2.plot(cd.x,np.ones(cd.x.shape),'r--')
        
        # ax1.legend((bottom_layer,top_layer,kappa_line),('Bottom Layer','Top Layer',"Kappa"),loc=4)
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
    plotitem.plot_var = wind
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
    plotitem.plot_var = wind
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
    plotitem.plot_var = kappa
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

    
