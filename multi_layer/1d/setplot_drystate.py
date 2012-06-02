#!/usr/bin/env python
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import os

import numpy as np

import matplotlib
import matplotlib.pyplot as mpl

from clawpack.pyclaw.solution import Solution
from clawpack.visclaw import geoplot, colormaps
from clawpack.clawutil.oldclawdata import Data

# matplotlib.rcParams['figure.figsize'] = [6.0,10.0]

#--------------------------
def setplot(plotdata,rho,dry_tolerance):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """

    # problem_data = Data(os.path.join(plotdata.outdir,'problem.data'))

    bathy_ref_lines = []
    # if problem_data.bathy_type == 1:
    #     bathy_ref_lines.append(problem_data.bathy_location)
    # elif problem_data.bathy_type == 2:
    #     bathy_ref_lines.append(problem_data.x0)
    #     bathy_ref_lines.append(problem_data.x1)
    
    def jump_afteraxes(current_data):
        # Plot position of jump on plot
        mpl.hold(True)
        mpl.plot([0.5,0.5],[-10.0,10.0],'k--')
        mpl.plot([0.0,1.0],[0.0,0.0],'k--')
        mpl.hold(False)
        mpl.title('Layer Velocities')
        
    # Load bathymetery
    b = Solution(0,path=plotdata.outdir,read_aux=True).state.aux[0,:]

    def bathy(current_data):
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
    
    # Window Settings
    xlimits = [0.0,1.0]
    xlimits_zoomed = [0.45,0.55]
    ylimits_momentum = [-0.004,0.004]
    ylimits_depth = [-1.0,0.2]
    ylimits_depth_zoomed = ylimits_depth
    ylimits_velocities = [-0.75,0.75]
    ylimits_velocities_zoomed = ylimits_velocities
    
    # ========================================================================
    #  Fill plot
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
    plotaxes.afteraxes = jump_afteraxes
    
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
    plotfigure.show = True
    
    def twin_axes(cd):
        fig = mpl.gcf()
        fig.clf()
        
        x = cd.patch.dimensions[0].centers
        
        # Draw fill plot
        ax1 = fig.add_subplot(211)
        
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
        
        # Remove ticks from top plot
        locs,labels = mpl.xticks()
        labels = ['' for i in xrange(len(locs))]
        mpl.xticks(locs,labels)
        
        ax1.set_title('Multilayer Surfaces t = %3.2f' % cd.t)
        ax1.set_xlim((0.0,1.0))
        ax1.set_ylim(ylimits_depth)
        # ax1.set_xlabel('x')
        ax1.set_ylabel('Depth')
        
        # Draw velocity and kappa plot
        ax1 = fig.add_subplot(212)     # the velocity scale
        # ax2 = ax1.twinx()              # the kappa scale
        
        # Bottom layer velocity
        bottom_layer = ax1.plot(x,u_2(cd),'k-',label="Bottom Layer Velocity")
        # Top Layer velocity
        top_layer = ax1.plot(x,u_1(cd),'b-',label="Top Layer velocity")#,color=(0.2,0.8,1.0))
        
        # Kappa
        # kappa_line = ax2.plot(x,cd.q[:,5],color='r',label="Kappa")
        # ax2.plot(x,np.ones(x.shape),'r--')
        
        for ref_line in bathy_ref_lines:
            ax1.plot([ref_line,ref_line],ylimits_velocities,'k--')

        # ax1.legend((bottom_layer,top_layer),('Bottom Layer','Top Layer'),loc=4)
        ax1.legend(('Bottom Layer','Top Layer'),loc=4)
        ax1.set_title('Layer Velocities')
        ax1.set_ylabel('Velocities (m/s)')
        # ax1.legend((bottom_layer,top_layer,kappa_line),('Bottom Layer','Top Layer',"Kappa"),loc=4)
        # ax1.set_title('Layer Velocities and Kappa')
        # ax2.set_ylabel('Kappa (1/Ri)')
        ax1.set_xlim((cd.xlower,cd.xupper))
        ax1.set_ylim(ylimits_velocities)
        # ax2.set_ylim((0.0,1.2))
        
        # mpl.subplots_adjust(hspace=0.1)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = twin_axes
    
    # ========================================================================
    #  Fill plot zoom
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='full_zoom',figno=1)
    
    def fill_zoom_afteraxes(cd):
        mpl.title('Multilayer Surfaces at t = %3.2f' % cd.t)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,1)'
    plotaxes.title = 'Multilayer Surfaces'
    plotaxes.xlimits = xlimits_zoomed
    plotaxes.ylimits = ylimits_depth_zoomed
    plotaxes.afteraxes = fill_zoom_afteraxes
     
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
    plotitem.plotstyle = '+'
    plotitem.show = True
    
    # Plot line on top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = eta_1
    plotitem.color = 'k'
    plotitem.plotstyle = 'x'
    plotitem.show = True
    
    # Layer Velocities
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,2)'
    plotaxes.title = "Layer Velocities"
    plotaxes.xlimits = xlimits_zoomed
    plotaxes.ylimits = ylimits_velocities_zoomed
    plotaxes.afteraxes = jump_afteraxes
    
    # Bottom layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = u_2
    plotitem.color = 'b'
    plotitem.plotstyle = '+-'
    plotitem.show = True

    # Top layer
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.color = (0.2,0.8,1.0)
    plotitem.plot_var = u_1
    plotitem.plotstyle = 'x-'
    plotitem.show = True
    
    # # Wind plot
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.axescmd = 'subplot(1,2,2)'
    # plotaxes.title = "Wind Velocity"
    # plotaxes.xlimits = 'auto'
    # plotaxes.ylimits = [-5.0,5.0]
    # 
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 4
    # plotitem.color = 'r'
    # plotitem.show = True
    
    # ========================================================================
    #  Momentum
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name="momentum",figno=134)
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
    plotitem.plotstyle = 'k-'
    plotitem.show = True
    
    # ========================================================================
    #  h-values
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='depths',figno=2)
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
    # plotfigure = plotdata.new_plotfigure(name='velocities',figno=1)
    # plotfigure.show = True
    # 
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.axescmd = 'subplot(1,2,1)'
    # plotaxes.title = "Layer Velocities"
    # plotaxes.xlimits = 'auto'
    # plotaxes.ylimits = 'auto'
    # 
    # # Top layer
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = u_1
    # plotitem.color = 'b'
    # plotitem.show = True
    # 
    # # Bottom layer
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.color = (0.2,0.8,1.0)
    # plotitem.plot_var = u_2
    # plotitem.show = True
    
    # Wind plot
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.axescmd = 'subplot(1,2,2)'
    # plotaxes.title = "Wind Velocity"
    # plotaxes.xlimits = 'auto'
    # plotaxes.ylimits = 'auto'
    # 
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 4
    # plotitem.color = 'r'
    # plotitem.show = True
    
    # ========================================================================
    #  Plot Wind Velocity
    # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='wind',figno=2)
    # plotfigure.show = True
    # 
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.title = "Wind Velocity"
    # plotaxes.xlimits = 'auto'
    # plotaxes.ylimits = [-5.0,5.0]
    # 
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 4
    # plotitem.color = 'r'
    # plotitem.show = True
    
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

    
