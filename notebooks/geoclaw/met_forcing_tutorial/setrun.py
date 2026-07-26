# encoding: utf-8
"""setrun for the GeoClaw meteorological-forcing tutorial.

A deliberately small, self-contained single-grid case (flat bathymetry, no AMR,
no downloads) so the tutorial notebook runs quickly.  One build serves both
forcing families, selected by keyword:

- ``forcing="holland80"`` : parametric Holland 1980 storm (family ``parametric``)
- ``forcing="data"``      : gridded NetCDF forcing (family ``gridded``)

The wind (u, v) and pressure aux fields are a pure function of (x, y, t), so a
tiny flat domain is enough to see and compare the two forcing families.
"""

import os

from clawpack.clawutil import data


def setrun(claw_pkg="geoclaw", forcing="holland80", topo_path="flat.tt3",
           storm_path=None):

    assert claw_pkg.lower() == "geoclaw", "Expected claw_pkg = 'geoclaw'"

    if storm_path is None:
        storm_path = "met.storm" if forcing == "data" else "holland.storm"

    # GeoClaw runs the executable from the output directory, so the topo and
    # storm files must be referenced by absolute path.
    topo_path = os.path.abspath(topo_path)
    storm_path = os.path.abspath(storm_path)

    rundata = data.ClawRunData(claw_pkg, 2)
    clawdata = rundata.clawdata

    # --- Small fixed single grid over an idealized ocean patch ---
    clawdata.num_dim = 2
    clawdata.lower[0] = -5.0
    clawdata.upper[0] = 5.0
    clawdata.lower[1] = 15.0
    clawdata.upper[1] = 25.0
    clawdata.num_cells[0] = 20
    clawdata.num_cells[1] = 20

    # --- System size ---
    clawdata.num_eqn = 3
    # 3 GeoClaw geometry slots + 1 friction + 3 storm (wind_u, wind_v, pressure)
    clawdata.num_aux = 3 + 1 + 3
    clawdata.capa_index = 2

    # --- Time: a few frames across the 6 h storm window ---
    clawdata.t0 = 0.0
    clawdata.restart = False
    clawdata.output_style = 2
    clawdata.output_times = [0.0, 3.0 * 3600.0, 6.0 * 3600.0]
    clawdata.output_format = "ascii"
    clawdata.output_q_components = "all"
    clawdata.output_aux_components = "all"     # dump wind/pressure aux
    clawdata.output_aux_onlyonce = False
    clawdata.verbosity = 0

    # --- Time stepping ---
    clawdata.dt_variable = True
    clawdata.dt_initial = 1.0
    clawdata.dt_max = 1e99
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0
    clawdata.steps_max = 100000

    # --- Method ---
    clawdata.order = 2
    clawdata.dimensional_split = "unsplit"
    clawdata.transverse_waves = 2
    clawdata.num_waves = 3
    clawdata.limiter = ["mc", "mc", "mc"]
    clawdata.use_fwaves = True
    clawdata.source_split = "godunov"
    clawdata.num_ghost = 2

    clawdata.bc_lower[0] = "extrap"
    clawdata.bc_upper[0] = "extrap"
    clawdata.bc_lower[1] = "extrap"
    clawdata.bc_upper[1] = "extrap"

    # --- AMR off (single fixed grid) ---
    amrdata = rundata.amrdata
    amrdata.amr_levels_max = 1
    amrdata.refinement_ratios_x = [2]
    amrdata.refinement_ratios_y = [2]
    amrdata.refinement_ratios_t = [2]
    amrdata.aux_type = ["center", "capacity", "yleft",
                        "center", "center", "center", "center"]
    amrdata.flag_richardson = False
    amrdata.flag2refine = False
    amrdata.verbosity_regrid = 0

    # --- GeoClaw geometry / topo ---
    geo_data = rundata.geo_data
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2      # lat-lon
    geo_data.earth_radius = 6367.5e3
    geo_data.coriolis_forcing = True
    geo_data.friction_forcing = True
    geo_data.manning_coefficient = 0.025
    geo_data.dry_tolerance = 1.0e-2
    geo_data.sea_level = 0.0

    rundata.topo_data.topofiles.append([3, topo_path])

    # --- A gauge under the storm track to record wind/pressure/surface ---
    rundata.gaugedata.gauges.append([1, 0.5, 20.1, 0.0, 1.0e9])
    # Record the wind_u, wind_v, pressure aux fields at the gauge (0-based).
    rundata.gaugedata.aux_out_fields = [4, 5, 6]

    # --- Storm / met forcing, selected via the family + subtype API ---
    surge_data = rundata.surge_data
    surge_data.wind_forcing = True
    surge_data.pressure_forcing = True
    surge_data.drag_law = 1
    surge_data.wind_index = 4           # 0-based -> Fortran 5 (u), 6 (v)
    surge_data.pressure_index = 6       # 0-based -> Fortran 7 (pressure)
    surge_data.display_landfall_time = False
    surge_data.wind_refine = False
    surge_data.R_refine = False
    if forcing == "data":
        surge_data.storm_family = "gridded"
        surge_data.storm_subtype = "gridded"
    else:
        surge_data.storm_family = "parametric"
        surge_data.storm_subtype = forcing      # e.g. "holland80"
    surge_data.storm_file = storm_path

    return rundata


if __name__ == "__main__":
    import sys
    setrun(*sys.argv[1:]).write()
