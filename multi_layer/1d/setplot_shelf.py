
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

from pyclaw.solution import Solution
from visclaw import geoplot, colormaps

# matplotlib.rcParams['figure.figsize'] = [6.0,10.0]

def setplot(plotdata,eta=[0.0,-300.0],rho=[1025.0,1045.0],g=9.81,dry_tolerance=1e-3,bathy_ref_lines=[-30e3]):
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """
    
    # Fetch bathymetry once
    b = Solution(0,path=plotdata.outdir,read_aux=True).state.aux[0,:]
    
        
    # ========================================================================
    #  Plot variable functions
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


    def kinetic_energy(current_data):
        q = current_data.q
        h = eta_1(current_data) - bathy(current_data)
        u = 0.5 * (u_1(current_data) + u_2(current_data))
        return 0.5*h*u**2
        
    def potential_energy(current_data):
        return 0.5*eta_1(current_data)**2

    def total_energy(current_data):
        return kinetic_energy(current_data) + potential_energy(current_data)

    def print_energy(current_data):
        PE = np.sum(potential_energy(current_data))
        KE = np.sum(kinetic_energy(current_data))
        total = PE + KE
        print 'PE = %g, KE = %g, total = %23.16e' % (PE,KE,total)
        
            
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
    plotdata.afterframe = print_energy
    
    # ========================================================================
    #  Figure for eta
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='eta', figno=0)
    plotfigure.kwargs = {'figsize':(8,3)}
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([0.1,0.15,0.80,0.75])'
    def fixfig(current_data):
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        add_bathy_dashes(current_data)
        xticks([-300000,-200000,-100000, -30000],['300','200','100','30','0'],\
          fontsize=15)
        ylim(-0.4,0.6)
        yticks([-0.4,-0.2,0,0.2,0.4],fontsize=15)
        #xlabel('kilometres offshore', fontsize=15)
        ylabel('Metres', fontsize=15)
        title('Surface at t = %i seconds' % int(t),fontsize=20)
        # savefig('shelf%s.eps' % str(current_data.frameno).zfill(2))

    plotaxes.afteraxes = fixfig
    #plotaxes.xlimits = [-150.e3, 50e3]
    #plotaxes.ylimits = [-0.4, 0.4]
    plotaxes.title = 'Surface'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = eta_1
    plotitem.plotstyle = '-'
    plotitem.color = 'b'
    plotitem.kwargs = {'linewidth':2}
    plotitem.show = True       # show on plot?
    
    # ========================================================================
    #  Figure for energy
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='energy', figno=1)
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Energy'
    def energy_axes(current_data):
        add_horizontal_dashes(current_data)
        add_bathy_dashes(current_data)
        km_labels(current_data)
    plotaxes.afteraxes = energy_axes

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = total_energy
    plotitem.plotstyle = '-o'
    plotitem.color = 'b'
    plotitem.show = True 
    
    # ========================================================================
    #  Full plot
    # ========================================================================
    def fill_items(plotaxes):
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
        plotitem.show = True
            
        # Plot line in between layers
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = eta_2
        plotitem.color = 'k'
        plotitem.plotstyle = '-'
        plotitem.show = True
    
        # Plot line on top layer
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = eta_1
        plotitem.color = 'k'
        plotitem.plotstyle = '-'
        plotitem.show = True
    
    # ========================================================================
    #  Full Plot
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='bathy',figno=102)
    plotfigure.show = True
    
    def bathy_axes(cd):
        km_labels(cd)
        mpl.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
        mpl.xlabel('km')
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Bathymetry'
    plotaxes.xlimits = xlimits
    plotaxes.ylimtis = [-4100,100]
    plotaxes.afteraxes = bathy_axes
    # if prob_data.bathy_type == 1:
    #     plotaxes.ylimits = [prob_data.bathy_right,10.0 ]
    #     plotaxes.xlimits = xlimits
    # elif prob_data.bathy_type == 2:
    #     # m = (prob_data.basin_depth - prob_data.shelf_depth) / (prob_data.x0 - prob_data.x1)
    #     # z = m * (x - prob_data.x0) + prob_data.basin_depth
    #     plotaxes.ylimits = [prob_data.eta_2-2,prob_data.eta_2+2]
    #     plotaxes.xlimits = [-32750,-32550]
    
    fill_items(plotaxes)
    
    # ========================================================================
    # Zoomed Depths  
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='depth',figno=103)
    plotfigure.show = True
    
    def zoom_depth_afteraxes(cd):
        mpl.hold(True)
        mpl.plot([-33000,-32500],[0,0],'k--')
        mpl.hold(False)

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Bottom Depth at Inundation point"
    plotaxes.afteraxes = zoom_depth_afteraxes
    # if prob_data.bathy_type == 2:
    #     plotaxes.ylimits = [-10,10]
    #     plotaxes.xlimits = [-33000,-32500]
    
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 2
    plotitem.color = 'b'
    plotitem.plotstyle = 'o'
    
    # ========================================================================
    #  Velocities
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name="Velocities",figno=200)
    plotfigure.show = False
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Layer Velocities"
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits_velocities
    def velocity_afteraxes(cd):
        add_bathy_dashes(cd)
        add_horizontal_dashes(cd)
        # km_labels(cd)
        mpl.title("Layer Velocities t = %4.1f s" % cd.t)
        mpl.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
        mpl.xlabel('km')
    plotaxes.afteraxes = velocity_afteraxes
    
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
    
    # ========================================================================
    #  Velocities with Kappa
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='vel_kappa',figno=14)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize':(7,6)}
    
    def twin_axes(cd):
        fig = mpl.gcf()
        fig.clf()
        
        x = cd.patch.dimensions[0].centers
        
        # Draw velocity and kappa plot
        ax1 = fig.add_subplot(111)     # the velocity scale
        ax2 = ax1.twinx()              # the kappa scale
        
        # Bottom layer velocity
        bottom_layer = ax1.plot(x,u_2(cd),'k-',label="Bottom Layer Velocity")
        # Top Layer velocity
        top_layer = ax1.plot(x,u_1(cd),'b-',label="Top Layer velocity")#,color=(0.2,0.8,1.0))
        
        # Kappa
        kappa_line = ax2.plot(x,kappa(cd),color='r',label="Kappa")
        ax2.plot(x,np.ones(x.shape),'r--')

        ax1.set_xlabel('km')
        mpl.xticks([-300e3,-200e3,-100e3,-30e3],[300,200,100,30],fontsize=15)
        
        for ref_line in bathy_ref_lines:
            ax1.plot([ref_line,ref_line],ylimits_velocities,'k--')
        # ax1.legend((bottom_layer,top_layer,kappa_line),('Bottom Layer','Top Layer',"Kappa"),loc=3)
        ax1.set_title("Layer Velocities and Kappa t = %4.1f s" % cd.t)
        ax1.set_ylabel('Velocities (m/s)')
        ax2.set_ylabel('Kappa (1/Ri)')
        ax1.set_xlim(xlimits)
        ax1.set_ylim(ylimits_velocities)
        ax2.set_ylim(ylimits_kappa)
        
        # mpl.subplots_adjust(hspace=0.1)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = twin_axes
    
    # ========================================================================
    #  Combined Top and Internal Surface
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='combined_surface',figno=13)
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
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
