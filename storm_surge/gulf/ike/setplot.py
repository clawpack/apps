
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""

import os

import numpy

# Plot customization
import matplotlib

# Markers and line widths
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['lines.markersize'] = 8

# Font Sizes
matplotlib.rcParams['font.size'] = 16
matplotlib.rcParams['axes.labelsize'] = 16
matplotlib.rcParams['legend.fontsize'] = 12
matplotlib.rcParams['xtick.labelsize'] = 16
matplotlib.rcParams['ytick.labelsize'] = 16

# DPI of output images
matplotlib.rcParams['savefig.dpi'] = 300

import matplotlib.pyplot as plt
import datetime

from clawpack.visclaw import colormaps
import clawpack.clawutil.data as clawutil
import clawpack.amrclaw.data as amrclaw
import clawpack.geoclaw.data as geodata

import clawpack.geoclaw.surge as surge

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

def setplot(plotdata):
    r"""Setplot function for surge plotting"""
    

    plotdata.clearfigures()  # clear any old figures,axes,items data

    fig_num_counter = surge.plot.figure_counter()

    # Load data from output
    clawdata = clawutil.ClawInputData(2)
    clawdata.read(os.path.join(plotdata.outdir,'claw.data'))
    amrdata = amrclaw.AmrclawInputData(clawdata)
    amrdata.read(os.path.join(plotdata.outdir,'amrclaw.data'))
    physics = geodata.GeoClawData()
    physics.read(os.path.join(plotdata.outdir,'geoclaw.data'))
    surge_data = surge.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir,'surge.data'))
    friction_data = surge.data.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir,'friction.data'))

    # Load storm track
    track = surge.plot.track_data(os.path.join(plotdata.outdir,'fort.track'))

    # Calculate landfall time, off by a day, maybe leap year issue?
    landfall_dt = datetime.datetime(2008,9,13,7) - datetime.datetime(2008,1,1,0)
    landfall = (landfall_dt.days - 1.0) * 24.0 * 60**2 + landfall_dt.seconds

    # Set afteraxes function
    surge_afteraxes = lambda cd: surge.plot.surge_afteraxes(cd, 
                                        track, landfall, plot_direction=False)

    # Color limits
    surface_range = 5.0
    speed_range = 3.0
    eta = physics.sea_level
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    # surface_contours = numpy.linspace(-surface_range, surface_range,11)
    surface_contours = [-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]
    surface_ticks = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
    surface_labels = [str(value) for value in surface_ticks]
    speed_limits = [0.0,speed_range]
    speed_contours = numpy.linspace(0.0,speed_range,13)
    speed_ticks = [0,1,2,3]
    speed_labels = [str(value) for value in speed_ticks]
    
    wind_limits = [0,64]
    # wind_limits = [-0.002,0.002]
    pressure_limits = [935,1013]
    friction_bounds = [0.01,0.04]
    # vorticity_limits = [-1.e-2,1.e-2]

    # def pcolor_afteraxes(current_data):
    #     surge_afteraxes(current_data)
    #     surge.plot.gauge_locations(current_data,gaugenos=[6])
    
    def contour_afteraxes(current_data):
        surge_afteraxes(current_data)

    def add_custom_colorbar_ticks_to_axes(axes, item_name, ticks, tick_labels=None):
        axes.plotitem_dict[item_name].colorbar_ticks = ticks
        axes.plotitem_dict[item_name].colorbar_tick_labels = tick_labels

    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================

    # ========================================================================
    #  Entire Gulf
    # ========================================================================
    gulf_xlimits = [clawdata.lower[0],clawdata.upper[0]]
    gulf_ylimits = [clawdata.lower[1],clawdata.upper[1]]
    gulf_shrink = 1.0
    def gulf_after_axes(cd):
        plt.subplots_adjust(left=0.08, bottom=0.04, right=0.97, top=0.96)
        surge_afteraxes(cd)
    #
    #  Surface
    #
    plotfigure = plotdata.new_plotfigure(name='Surface - Entire Domain', 
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.afteraxes = gulf_after_axes

    surge.plot.add_surface_elevation(plotaxes, plot_type='contourf', 
                                               contours=surface_contours,
                                               shrink=gulf_shrink)
    surge.plot.add_land(plotaxes,topo_min=-10.0,topo_max=5.0)
    surge.plot.add_bathy_contours(plotaxes)
    add_custom_colorbar_ticks_to_axes(plotaxes, 'surface', surface_ticks, surface_labels)

    #
    #  Water Speed
    #
    plotfigure = plotdata.new_plotfigure(name='Currents - Entire Domain',  
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.afteraxes = gulf_after_axes

    # Speed
    surge.plot.add_speed(plotaxes, plot_type='contourf', 
                                   contours=speed_contours, 
                                   shrink=gulf_shrink)
    add_custom_colorbar_ticks_to_axes(plotaxes, 'speed', speed_ticks, speed_labels)

    # Land
    surge.plot.add_land(plotaxes)
    surge.plot.add_bathy_contours(plotaxes)    

    #
    # Friction field
    #
    plotfigure = plotdata.new_plotfigure(name='Friction',
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = friction_data.variable_friction and True

    def friction_after_axes(cd):
        plt.subplots_adjust(left=0.08, bottom=0.04, right=0.97, top=0.96)
        plt.title(r"Manning's $n$ Coefficient")
        # surge_afteraxes(cd)

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    # plotaxes.title = "Manning's N Coefficient"
    plotaxes.afteraxes = friction_after_axes
    plotaxes.scaled = True

    surge.plot.add_friction(plotaxes,bounds=friction_bounds,shrink=0.9)
    plotaxes.plotitem_dict['friction'].amr_patchedges_show = [0,0,0,0,0,0,0]
    plotaxes.plotitem_dict['friction'].colorbar_label = ""


    # ========================================================================
    #  LaTex Shelf
    # ========================================================================
    latex_xlimits = [-97.5,-88.5]
    latex_ylimits = [27.5,30.5]
    latex_shrink = 1.0
    def latex_after_axes(cd):
        plt.subplots_adjust(right=1.0)
        surge_afteraxes(cd)
    #
    # Surface
    #
    plotfigure = plotdata.new_plotfigure(name='Surface - LaTex Shelf', 
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = True
    plotfigure.kwargs = {'figsize':(9,2.7), 'facecolor':'none'}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = latex_xlimits
    plotaxes.ylimits = latex_ylimits
    plotaxes.afteraxes = latex_after_axes
    
    surge.plot.add_surface_elevation(plotaxes, plot_type='contourf', 
                                               contours=surface_contours,
                                               shrink=latex_shrink)
    add_custom_colorbar_ticks_to_axes(plotaxes, 'surface', surface_ticks, surface_labels)
    # plotaxes.plotitem_dict['surface'].contour_cmap = plt.get_cmap('OrRd')
    # surge.plot.add_surface_elevation(plotaxes,plot_type='contour')
    surge.plot.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [1,1,1,0,0,0,0]
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [1,1,1,0,0,0,0]

    # Plot using jet and 0.0 to 5.0 to match figgen generated ADCIRC results
    # plotaxes.plotitem_dict['surface'].pcolor_cmin = 0.0
    # plotaxes.plotitem_dict['surface'].pcolor_cmax = 5.0
    # plotaxes.plotitem_dict['surface'].pcolor_cmap = plt.get_cmap('jet')

    #
    # Water Speed
    #
    plotfigure = plotdata.new_plotfigure(name='Currents - LaTex Shelf',  
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = True
    plotfigure.kwargs = {'figsize':(9,2.7), 'facecolor':'none'}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = latex_xlimits
    plotaxes.ylimits = latex_ylimits
    plotaxes.afteraxes = latex_after_axes
    
    surge.plot.add_speed(plotaxes, plot_type='contourf', 
                                   contours=speed_contours, 
                                   shrink=latex_shrink)
    add_custom_colorbar_ticks_to_axes(plotaxes, 'speed', speed_ticks, speed_labels)
    # surge.plot.add_surface_elevation(plotaxes,plot_type='contour')
    surge.plot.add_land(plotaxes)
    plotaxes.plotitem_dict['speed'].amr_patchedges_show = [1,1,0,0,0,0,0]
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [1,1,1,0,0,0,0]


    # ========================================================================
    #  Houston/Galveston
    # ========================================================================
    houston_xlimits = [-(95.0 + 26.0 / 60.0), -(94.0 + 25.0 / 60.0)]
    houston_ylimits = [29.1, 29.0 + 55.0 / 60.0]
    houston_shrink = 0.9
    def houston_after_axes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        # surge.plot.gauge_locations(cd)
    
    #
    # Surface Elevations
    #
    plotfigure = plotdata.new_plotfigure(name='Surface - Houston/Galveston',  
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = houston_xlimits
    plotaxes.ylimits = houston_ylimits
    plotaxes.afteraxes = houston_after_axes
    
    surge.plot.add_surface_elevation(plotaxes, plot_type='contourf', 
                                               contours=surface_contours,
                                               shrink=houston_shrink)
    add_custom_colorbar_ticks_to_axes(plotaxes, 'surface', surface_ticks, surface_labels)
    surge.plot.add_land(plotaxes)
    # surge.plot.add_bathy_contours(plotaxes)

    # Plot using jet and 0.0 to 5.0 to match figgen generated ADCIRC results
    # plotaxes.plotitem_dict['surface'].pcolor_cmin = 0.0
    # plotaxes.plotitem_dict['surface'].pcolor_cmax = 5.0
    # plotaxes.plotitem_dict['surface'].pcolor_cmap = plt.get_cmap('jet')

    #
    # Water Speed
    #
    plotfigure = plotdata.new_plotfigure(name='Currents - Houston/Galveston',  
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = houston_xlimits
    plotaxes.ylimits = houston_ylimits
    plotaxes.afteraxes = houston_after_axes
    
    surge.plot.add_speed(plotaxes, plot_type='contourf', 
                                   contours=speed_contours,
                                   shrink=houston_shrink)
    add_custom_colorbar_ticks_to_axes(plotaxes, 'speed', speed_ticks, speed_labels)
    surge.plot.add_land(plotaxes)
    # surge.plot.add_bathy_contours(plotaxes)
    # plotaxes.plotitem_dict['speed'].amr_patchedges_show = [1,1,1,1,1,1,1,1]
    # plotaxes.plotitem_dict['land'].amr_patchedges_show = [1,1,1,1,1,1,1,1]


    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    # try:
        # plotaxes.xlimits = [clawdata.t0,clawdata.tfinal]
    # except:
        # pass
    # plotaxes.ylimits = [0,150.0]
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Surface'
    plotaxes.afteraxes = surge.plot.gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    # =====================
    #  Gauge Location Plot
    # =====================
    gauge_xlimits = [-95.5, -94.0]
    gauge_ylimits = [29.0, 30.0]
    houston_shrink = 0.9
    def gauge_after_axes(cd):
        # plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        surge.plot.gauge_locations(cd)
        plt.title("Gauge Locations")

    plotfigure = plotdata.new_plotfigure(name='Gauge Locations',  
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = gauge_xlimits
    plotaxes.ylimits = gauge_ylimits
    plotaxes.afteraxes = gauge_after_axes
    
    surge.plot.add_surface_elevation(plotaxes, plot_type='contourf', 
                                               contours=surface_contours,
                                               shrink=houston_shrink)
    # surge.plot.add_surface_elevation(plotaxes, plot_type="contourf")
    add_custom_colorbar_ticks_to_axes(plotaxes, 'surface', surface_ticks, surface_labels)
    surge.plot.add_land(plotaxes)
    # plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0,0,0,0,0,0,0]
    # plotaxes.plotitem_dict['surface'].add_colorbar = False
    # plotaxes.plotitem_dict['surface'].pcolor_cmap = plt.get_cmap('jet')
    # plotaxes.plotitem_dict['surface'].pcolor_cmap = plt.get_cmap('gist_yarg')
    # plotaxes.plotitem_dict['surface'].pcolor_cmin = 0.0
    # plotaxes.plotitem_dict['surface'].pcolor_cmax = 5.0
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0,0,0,0,0,0,0]

    # ==============================================================
    #  Debugging Plots, only really work if using interactive plots
    # ==============================================================
    #
    # Water Velocity Components
    #
    plotfigure = plotdata.new_plotfigure(name='Velocity Components - Entire Domain',  
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = False

    # X-Component
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(121)"
    plotaxes.title = 'Velocity, X-Component'
    plotaxes.scaled = True
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.afteraxes = gulf_after_axes

    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.plot.water_u
    plotitem.pcolor_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.pcolor_cmin = -speed_limits[1]
    plotitem.pcolor_cmax = speed_limits[1]
    plotitem.colorbar_shrink = gulf_shrink
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]

    surge.plot.add_land(plotaxes)

    # Y-Component
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(122)"
    plotaxes.title = 'Velocity, Y-Component'
    plotaxes.scaled = True
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.afteraxes = gulf_after_axes

    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.plot.water_v
    plotitem.pcolor_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.pcolor_cmin = -speed_limits[1]
    plotitem.pcolor_cmax = speed_limits[1]
    plotitem.colorbar_shrink = gulf_shrink
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]
    
    surge.plot.add_land(plotaxes)

    # 
    # Depth
    # 
    plotfigure = plotdata.new_plotfigure(name='Depth - Entire Domain', 
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'depth'
    plotaxes.scaled = True
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.afteraxes = gulf_after_axes

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = 0
    plotitem.imshow_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.imshow_cmin = 0
    plotitem.imshow_cmax = 100
    plotitem.colorbar_shrink = gulf_shrink
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,1,1,1,1]

    #
    # Hurricane forcing
    #
    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure',  
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = surge_data.pressure_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = gulf_after_axes
    plotaxes.scaled = True
    
    surge.plot.add_pressure(plotaxes, bounds=pressure_limits, shrink=gulf_shrink)
    # add_pressure(plotaxes)
    surge.plot.add_land(plotaxes)
    
    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed', 
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = surge_data.wind_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = gulf_after_axes
    plotaxes.scaled = True
    
    surge.plot.add_wind(plotaxes, bounds=wind_limits, plot_type='imshow',
                                  shrink=gulf_shrink)
    # add_wind(plotaxes,bounds=wind_limits,plot_type='contour')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='quiver')
    surge.plot.add_land(plotaxes)
    
    # Surge field
    plotfigure = plotdata.new_plotfigure(name='Surge Field', 
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = ((surge_data.wind_forcing or surge_data.pressure_forcing) 
                        and False)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.title = "Storm Surge Source Term S"
    plotaxes.afteraxes = gulf_after_axes
    plotaxes.scaled = True
    
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.plot.pressure_field + 1
    plotitem.pcolor_cmap = plt.get_cmap('PuBu')
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1e-3
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = gulf_shrink
    plotitem.colorbar_label = "Source Strength"
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,0,0]
    
    surge.plot.add_land(plotaxes)

    plotfigure = plotdata.new_plotfigure(name='Friction/Coriolis Source', 
                                         figno=fig_num_counter.get_counter())
    plotfigure.show = False
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = gulf_xlimits
    plotaxes.ylimits = gulf_ylimits
    plotaxes.title = "Friction/Coriolis Source"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.plot.pressure_field + 2
    plotitem.pcolor_cmap = plt.get_cmap('PuBu')
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1e-3
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = gulf_shrink
    plotitem.colorbar_label = "Source Strength"
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,0,0]
    
    surge.plot.add_land(plotaxes)

    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'            # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

