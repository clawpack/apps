"""Set up the plot figures for the met-forcing tutorial.

Small idealized domain; plots the wind, pressure, and surface fields plus a
single gauge.  Works for both forcing families: the storm-track overlay is only
drawn when a ``fort.track`` is present (parametric storms write one; gridded
forcing does not).
"""

import os

import numpy as np
import matplotlib.pyplot as plt

import clawpack.clawutil.data
import clawpack.geoclaw.data

import clawpack.geoclaw.surge.plot as surge


def setplot(plotdata):
    r"""Setplot for the met-forcing tutorial."""

    plotdata.clearfigures()
    plotdata.format = "ascii"

    # Load run configuration from the output directory.
    clawdata = clawpack.clawutil.data.ClawInputData(2)
    clawdata.read(os.path.join(plotdata.outdir, "claw.data"))
    physics = clawpack.geoclaw.data.GeoClawData()
    physics.read(os.path.join(plotdata.outdir, "geoclaw.data"))
    surge_data = clawpack.geoclaw.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir, "surge.data"))

    # Storm track overlay only exists for parametric (centered) forcing.
    track_path = os.path.join(plotdata.outdir, "fort.track")
    track = surge.track_data(track_path) if os.path.exists(track_path) else None

    def surge_afteraxes(cd):
        if track is not None:
            surge.surge_afteraxes(cd, track, plot_direction=False)

    xlimits = [clawdata.lower[0], clawdata.upper[0]]
    ylimits = [clawdata.lower[1], clawdata.upper[1]]

    surface_limits = [physics.sea_level - 0.5, physics.sea_level + 0.5]
    wind_limits = [0.0, 50.0]
    pressure_limits = [950.0, 1015.0]

    # --- Surface elevation ---
    plotfigure = plotdata.new_plotfigure(name="Surface", figno=0)
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Surface elevation (m)"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = surge_afteraxes
    surge.add_surface_elevation(plotaxes, bounds=surface_limits)
    surge.add_land(plotaxes)

    # --- Wind field ---
    plotfigure = plotdata.new_plotfigure(name="Wind Speed", figno=1)
    plotfigure.show = surge_data.wind_forcing
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Wind speed (m/s)"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = surge_afteraxes
    surge.add_wind(plotaxes, bounds=wind_limits)
    surge.add_land(plotaxes)

    # --- Pressure field ---
    plotfigure = plotdata.new_plotfigure(name="Pressure", figno=2)
    plotfigure.show = surge_data.pressure_forcing
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Sea-level pressure (mbar)"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = surge_afteraxes
    surge.add_pressure(plotaxes, bounds=pressure_limits)
    surge.add_land(plotaxes)

    # --- Gauge: surface time series ---
    plotfigure = plotdata.new_plotfigure(name="Gauge Surface", figno=300,
                                         type="each_gauge")
    plotfigure.clf_each_gauge = True
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Surface at gauge"
    plotaxes.xlabel = "t (s)"
    plotaxes.ylabel = "Surface (m)"
    plotitem = plotaxes.new_plotitem(plot_type="1d_plot")
    plotitem.plot_var = 3
    plotitem.plotstyle = "b-"

    # Hardcopy parameters.
    plotdata.printfigs = True
    plotdata.print_format = "png"
    plotdata.print_framenos = "all"
    plotdata.print_gaugenos = "all"
    plotdata.print_fignos = "all"
    plotdata.html = True
    plotdata.latex = False

    return plotdata
