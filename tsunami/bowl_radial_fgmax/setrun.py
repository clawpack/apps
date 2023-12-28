"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
import numpy
from clawpack.geoclaw import fgmax_tools


#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    from clawpack.clawutil import data

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------
    rundata = setgeo(rundata)

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------
    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

    # Lower and upper edge of computational domain:
    clawdata.lower[0] = -100.0
    clawdata.upper[0] = 100.0

    clawdata.lower[1] = -100.0
    clawdata.upper[1] = 100.0



    # Number of grid cells: Coarsest grid
    clawdata.num_cells[0] = 50
    clawdata.num_cells[1] = 50


    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 1

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 0

    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0


    # Restart from checkpoint file of a previous run?
    # Note: If restarting, you must also change the Makefile to set:
    #    RESTART = True
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False               # True to restart from prior results
    clawdata.restart_file = 'fort.chk00006'  # File to use for restart data

    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.num_output_times = 5
        clawdata.tfinal = 5.0
        clawdata.output_t0 = True  # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = [0.5, 1.0]

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 1
        clawdata.output_t0 = True
        

    clawdata.output_format = 'ascii'      # 'ascii' or 'netcdf' 

    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'none'  # could be list
    clawdata.output_aux_onlyonce = True    # output aux arrays only at t0



    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 2



    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = True

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 0.016

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.9
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 5000




    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2
    
    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'
    
    # For unsplit method, transverse_waves can be 
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 2

    # Number of waves in the Riemann solution:
    clawdata.num_waves = 3
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc', 'mc', 'mc']

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms
    
    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'


    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.bc_lower[0] = 'extrap'
    clawdata.bc_upper[0] = 'extrap'

    clawdata.bc_lower[1] = 'extrap'
    clawdata.bc_upper[1] = 'extrap'

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 0

    if clawdata.checkpt_style == 0:
        # Do not checkpoint at all
        pass

    elif clawdata.checkpt_style == 1:
        # Checkpoint only at tfinal.
        pass

    elif clawdata.checkpt_style == 2:
        # Specify a list of checkpoint times.  
        clawdata.checkpt_times = [0.1,0.15]

    elif clawdata.checkpt_style == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5

    # ---------------
    # AMR parameters:
    # ---------------
    amrdata = rundata.amrdata

    # max number of refinement levels:
    amrdata.amr_levels_max = 4

    # List of refinement ratios at each level (length at least mxnest-1)
    amrdata.refinement_ratios_x = [4,4,4]
    amrdata.refinement_ratios_y = [4,4,4]
    amrdata.refinement_ratios_t = [4,4,4]


    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center']


    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0  


    #  ----- For developers ----- 
    # Toggle debugging print statements:
    amrdata.dprint = False      # print domain flags
    amrdata.eprint = False      # print err est flags
    amrdata.edebug = False      # even more err est flags
    amrdata.gprint = False      # grid bisection/clustering
    amrdata.nprint = False      # proper nesting output
    amrdata.pprint = False      # proj. of tagged points
    amrdata.rprint = False      # print regridding summary
    amrdata.sprint = False      # space/memory output
    amrdata.tprint = False      # time step reporting each level
    amrdata.uprint = False      # update/upbnd reporting
    
    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    # == setregions.data values ==
    regions = rundata.regiondata.regions
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    regions.append([1, 1, 0., 1.e10, -100.,100., -100.,100.])
    regions.append([1, 2, 0., 1.e10,    0.,100.,  -20.,100.])
    regions.append([2, 3, 3., 1.e10,   52., 72.,   52., 72.])
    regions.append([2, 3, 3., 1.e10,   75., 95.,   -10.,  10.])
    regions.append([2, 4, 3.4, 1.e10,   55., 70.,   55., 70.])
    regions.append([2, 4, 3.4, 1.e10,   83., 93.,   -10.,  10.])

    # == setgauges.data values ==
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    # rundata.gaugedata.add_gauge()

    # gauges along x-axis:
    gaugeno = 0
    for r in numpy.linspace(86., 93., 9):
        gaugeno = gaugeno+1
        x = r + .001  # shift a bit away from cell corners
        y = .001
        rundata.gaugedata.gauges.append([gaugeno, x, y, 0., 1e10])

    # gauges along diagonal:
    gaugeno = 100
    for r in numpy.linspace(86., 93., 9):
        gaugeno = gaugeno+1
        x = (r + .001) / numpy.sqrt(2.)
        y = (r + .001) / numpy.sqrt(2.)
        rundata.gaugedata.gauges.append([gaugeno, x, y, 0., 1e10])
    

    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print("*** Error, this rundata has no geo_data attribute")
        raise AttributeError("Missing geo_data attribute")

       
    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 1
    geo_data.earth_radius = 6367.5e3

    # == Forcing Options
    geo_data.coriolis_forcing = False

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 1.e-3
    geo_data.friction_forcing = True
    geo_data.manning_coefficient = 0.025
    geo_data.friction_depth = 20.0

    # Refinement data
    refinement_data = rundata.refinement_data
    refinement_data.wave_tolerance = 1.e-2
    refinement_data.variable_dt_refinement_ratios = True

    # == settopo.data values ==
    topo_data = rundata.topo_data
    # for topography, append lines of the form
    #    [topotype, fname]
    topo_data.topofiles.append([2, 'bowl.topotype2'])

    # == setdtopo.data values ==
    dtopo_data = rundata.dtopo_data
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #   [topotype, fname]

    # == setqinit.data values ==
    rundata.qinit_data.qinit_type = 4
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]
    rundata.qinit_data.qinitfiles.append([1, 2, 'hump.xyz'])

    # == fgmax_grids.data values ==
    # NEW STYLE STARTING IN v5.7.0

    # set num_fgmax_val = 1 to save only max depth,
    #                     2 to also save max speed,
    #                     5 to also save max hs,hss,hmin
    rundata.fgmax_data.num_fgmax_val = 1  # Save depth

    fgmax_grids = rundata.fgmax_data.fgmax_grids  # empty list to start

    # Now append to this list objects of class fgmax_tools.FGmaxGrid
    # specifying any fgmax grids.

    # For illustration, set up several fgmax grids of different types:

    # Default values (might be changed below)
    tstart_max =  4.       # when to start monitoring max values
    tend_max = 1.e10       # when to stop monitoring max values
    dt_check = 0.1         # target time (sec) increment between updating 
                           # max values
    min_level_check = 4    # which levels to monitor max on
    arrival_tol = 1.e-2    # tolerance for flagging arrival
    interp_method = 0      # pw constant in FV cell, not interpolated

    # ======================== 
    # Lat-Long grid on x-axis:

    fg = fgmax_tools.FGmaxGrid()
    fg.point_style = 2       # will specify a 2d grid of points
    fg.nx = 100
    fg.ny = 80
    fg.x1 = 88.
    fg.y1 = -2.
    fg.x2 = 93.
    fg.y2 = 2.
    fg.tstart_max = tstart_max
    fg.tend_max = tend_max
    fg.dt_check = dt_check
    fg.min_level_check = min_level_check
    fg.arrival_tol = arrival_tol
    fg.interp_method = interp_method
    fgmax_grids.append(fg)    # written to fgmax_grids.data

    # ===============================
    # Quadrilateral grid on diagonal:

    fg = fgmax_tools.FGmaxGrid()
    fg.point_style = 3       # will specify a 2d grid of points
    fg.n12 = 100
    fg.n23 = 80

    # rotate grid1 from above by pi/4 to place on diagonal:
    x1 = 88.
    y1 = -2.
    x2 = 93.
    y2 = -2.
    x3 = 93.
    y3 = 2.
    x4 = 88.
    y4 = 2.
    c = numpy.cos(numpy.pi / 4.)
    s = numpy.sin(numpy.pi / 4.)
    fg.x1 = c*x1 - s*y1
    fg.y1 = s*x1 + c*y1
    fg.x2 = c*x2 - s*y2
    fg.y2 = s*x2 + c*y2
    fg.x3 = c*x3 - s*y3
    fg.y3 = s*x3 + c*y3
    fg.x4 = c*x4 - s*y4
    fg.y4 = s*x4 + c*y4

    fg.tstart_max = tstart_max
    fg.tend_max = tend_max
    fg.dt_check = dt_check
    fg.min_level_check = min_level_check
    fg.arrival_tol = arrival_tol
    fg.interp_method = interp_method
    fgmax_grids.append(fg)    # written to fgmax_grids.data

    # ===============================
    # Transect on x-axis:

    fg = fgmax_tools.FGmaxGrid()
    fg.point_style = 1       # will specify a 1d grid of points
    fg.npts = 100
    fg.x1 = 85.
    fg.y1 = 0.
    fg.x2 = 93.
    fg.y2 = 0.
    fg.tstart_max = tstart_max
    fg.tend_max = tend_max
    fg.dt_check = dt_check
    fg.min_level_check = min_level_check
    fg.arrival_tol = arrival_tol
    fg.interp_method = interp_method
    fgmax_grids.append(fg)    # written to fgmax_grids.data


    # ===============================
    # Transect on diagonal:

    fg = fgmax_tools.FGmaxGrid()
    fg.point_style = 1       # will specify a 1d grid of points
    fg.npts = 100
    fg.x1 = 60.
    fg.y1 = 60.
    fg.x2 = 66.
    fg.y2 = 66.
    fg.tstart_max = tstart_max
    fg.tend_max = tend_max
    fg.dt_check = dt_check
    fg.min_level_check = min_level_check
    fg.arrival_tol = arrival_tol
    fg.interp_method = interp_method
    fgmax_grids.append(fg)    # written to fgmax_grids.data

    # ===============================
    # Points along shoreline:
    # Around circle in first quadrant at 90 meters from center

    fg = fgmax_tools.FGmaxGrid()
    fg.point_style = 0       # will specify a list of points
    fg.npts = 500

    from numpy import pi
    theta = numpy.linspace(-pi/8.,3*pi/8,fg.npts)  
    fg.X = 90.*numpy.cos(theta)  
    fg.Y = 90.*numpy.sin(theta)

    fg.tstart_max = tstart_max
    fg.tend_max = tend_max
    fg.dt_check = dt_check
    fg.min_level_check = min_level_check
    fg.arrival_tol = arrival_tol
    fg.interp_method = interp_method
    fgmax_grids.append(fg)    # written to fgmax_grids.data


    return rundata
    # end of function setgeo
    # ----------------------



if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()

