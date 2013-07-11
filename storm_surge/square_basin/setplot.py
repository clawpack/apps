
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""

import os

import datetime
import numpy as np
import matplotlib.pyplot as plt

import clawpack.geoclaw.surge as surge
import clawpack.visclaw.colormaps as colormaps
import clawpack.visclaw.geoplot as geoplot
import clawpack.clawutil.clawdata as clawdata

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

def setplot(plotdata):
    r"""Setplot function for surge plotting"""
    

    plotdata.clearfigures()  # clear any old figures,axes,items data

    # Load data from output
    amrdata = clawdata.AmrclawInputData(2)
    amrdata.read(os.path.join(plotdata.outdir,'amrclaw.data'))
    physics = clawdata.GeoclawInputData(2)
    physics.read(os.path.join(plotdata.outdir,'geoclaw.data'))
    surge_data = surge.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir,'surge.data'))
    friction_data = surge.data.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir,'friction.data'))

    # Load storm track
    track = surge.plot.track_data(os.path.join(plotdata.outdir,'fort.track'))

    # Calculate landfall time, off by a day, maybe leap year issue?
    landfall_dt = datetime.datetime(2008, 8, 1, 12) - datetime.datetime(2008,1,1,0)
    landfall = landfall_dt.days * 24.0 * 60**2 + landfall_dt.seconds

    # Set afteraxes function
    surge_afteraxes = lambda cd: surge.plot.surge_afteraxes(cd, 
                                        track, landfall, plot_direction=False)

    # Limits for plots
    full_xlimits = [amrdata.lower[0],amrdata.upper[0]]
    full_ylimits = [amrdata.lower[1],amrdata.upper[1]]

    # Color limits
    surface_range = 1.0
    speed_range = 2.0

    xlimits = full_xlimits
    ylimits = full_ylimits
    eta = physics.sea_level
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    speed_limits = [0.0,speed_range]
    
    wind_limits = [0,55]
    pressure_limits = [966,1013]

    ref_lines = []


    # ==========================================================================
    #  Generic helper functions
    # ==========================================================================
    def pcolor_afteraxes(current_data):
        surge_afteraxes(current_data)
        surge.plot.gauge_locations(current_data)
        
    def contour_afteraxes(current_data):
        surge_afteraxes(current_data)
        
    def bathy_ref_lines(current_data):
        plt.hold(True)
        y = [amrdata.ylower,amrdata.yupper]
        for ref_line in ref_lines:
            plt.plot([ref_line,ref_line],y,'y--')
        plt.hold(False)

    
    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================

    # ========================================================================
    #  Surface Elevations - Entire Ocean
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=0)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes
    
    surge.plot.add_surface_elevation(plotaxes,bounds=surface_limits)
    surge.plot.add_land(plotaxes)


    # ========================================================================
    #  Water Speed - Entire Gulf
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='speed', figno=1)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes

    # Speed
    surge.plot.add_speed(plotaxes,bounds=speed_limits)

    # Land
    surge.plot.add_land(plotaxes)


    # ========================================================================
    # Hurricane forcing - Entire gulf
    # ========================================================================
    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure', figno=2)
    plotfigure.show = surge_data.pressure_forcing
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.plot.add_pressure(plotaxes,bounds=pressure_limits)
    # add_pressure(plotaxes)
    surge.plot.add_land(plotaxes)
    
    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed',figno=4)
    plotfigure.show = surge_data.wind_forcing
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.plot.add_wind(plotaxes,bounds=wind_limits,plot_type='imshow')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='contour')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='quiver')
    surge.plot.add_land(plotaxes)
    
    # Wind field components
    plotfigure = plotdata.new_plotfigure(name='Wind Components',figno=5)
    plotfigure.show = surge_data.wind_forcing
    plotfigure.kwargs = {'figsize':(16,6)}
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(121)"
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "X-Component of Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surge.plot.wind_x
    plotitem.imshow_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.imshow_cmin = -wind_limits[1]
    plotitem.imshow_cmax = wind_limits[1]
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(122)"
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Y-Component of Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surge.plot.wind_y
    plotitem.imshow_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.imshow_cmin = -wind_limits[1]
    plotitem.imshow_cmax = wind_limits[1]
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    # plotaxes.xlimits = [0.0,amrdata.tfinal]
    # plotaxes.ylimits = [0,150.0]
    plotaxes.ylimits = surface_limits
    plotaxes.title = 'Surface'
    plotaxes.afteraxes = surge.plot.gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'r-'
    
    # =================
    #  Plot bathymetry
    # =================
    plotfigure = plotdata.new_plotfigure(name='Bathymetry', figno=301)
    plotfigure.show = True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Bathymetry"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    plotitem = plotaxes.new_plotitem(plot_type="2d_pcolor")
    plotitem.plot_var = geoplot.topo
    # plotitem.pcolor_cmap = geoplot.seafloor_colormap
    plotitem.pcolor_cmin = physics.basin_depth
    plotitem.pcolor_cmax = 300.0
    plotitem.add_colorbar = True

    surge.plot.add_land(plotaxes)


    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    # plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
    #                 type='each_gauge')
    # plotfigure.clf_each_gauge = True
    # 
    # # Set up for axes in this figure:
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.xlimits = 'auto'
    # plotaxes.ylimits = 'auto'
    # plotaxes.title = 'Surface'
    # 
    # # Plot surface as blue curve:
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 3
    # plotitem.plotstyle = 'b-'
    # 
    # # Plot topo as green curve:
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.show = False
    # 
    # def gaugetopo(current_data):
    #     q = current_data.q
    #     h = q[0,:]
    #     eta = q[3,:]
    #     topo = eta - h
    #     return topo
    #     
    # plotitem.plot_var = gaugetopo
    # plotitem.plotstyle = 'g-'
    # 
    # def add_zeroline(current_data):
    #     from pylab import plot, legend, xticks, floor
    #     t = current_data.t
    #     #legend(('surface','topography'),loc='lower left')
    #     plot(t, 0*t, 'k')
    #     n = int(floor(t.max()/3600.) + 2)
    #     xticks([3600*i for i in range(n)])
    # 
    # plotaxes.afteraxes = add_zeroline


    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    # plotdata.print_framenos = [45,46,47,48]
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

