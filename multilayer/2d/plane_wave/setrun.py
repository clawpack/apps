#!/usr/bin/env python
# encoding: utf-8
""" 
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.
    
""" 

import sys

import clawpack.clawutil.clawdata as data
import clawpack.geoclaw.surge as surge
import clawpack.geoclaw.multilayer as multilayer

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

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)
    
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
    clawdata.lower[0] = -1.0
    clawdata.upper[0] = 2.0

    clawdata.lower[1] = -1.0
    clawdata.upper[1] = 2.0



    # Number of grid cells: Coarsest grid
    clawdata.num_cells[0] = 100
    clawdata.num_cells[1] = 100

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 6

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 10
    
    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 0
    
    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0
    
    
    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1
    
    
    if clawdata.output_style==1:
        clawdata.num_output_times = 80
        # if wave_family < 4 and wave_family > 1:
        clawdata.tfinal = 1.0
        clawdata.output_t0 = True
        # else:
            # clawdata.tfinal = 0.1

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = [0.5, 1.0]
    elif clawdata.outstyle == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 80
        clawdata.output_t0 = True
    


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
    # clawdata.dt_initial = 0.64e2
    clawdata.dt_initial = 0.575e-03
    
    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99
    
    # Desired Courant number if variable dt used, and max to allow without 
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.8
    clawdata.cfl_max = 0.9
    # clawdata.cfl_desired = 0.4
    # clawdata.cfl_max = 0.5
    
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
    clawdata.num_waves = 6

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc','mc','mc','mc','mc','mc']
    
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


    # ---------------
    # AMR parameters:
    # ---------------


    # max number of refinement levels:
    clawdata.amr_levels_max = 1

    # List of refinement ratios at each level (length at least mxnest-1)
    clawdata.refinement_ratios_x = [2,6]
    clawdata.refinement_ratios_y = [2,6]
    clawdata.refinement_ratios_t = [2,6]


    # Specify type of each aux variable in clawdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    clawdata.aux_type = ['center','center','yleft','center','center','center',
                         'center','center','center','center','center']


    # Flag using refinement routine flag2refine rather than richardson error
    clawdata.flag_richardson = False    # use Richardson?
    clawdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    clawdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    clawdata.regrid_buffer_width  = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    clawdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    clawdata.verbosity_regrid = 0  

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


    #  ----- For developers ----- 
    # Toggle debugging print statements:
    clawdata.dprint = False      # print domain flags
    clawdata.eprint = False      # print err est flags
    clawdata.edebug = False      # even more err est flags
    clawdata.gprint = False      # grid bisection/clustering
    clawdata.nprint = False      # proper nesting output
    clawdata.pprint = False      # proj. of tagged points
    clawdata.rprint = False      # print regridding summary
    clawdata.sprint = False      # space/memory output
    clawdata.tprint = True       # time step reporting each level
    clawdata.uprint = False      # update/upbnd reporting
    
    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    # == setregions.data values ==
    rundata.regiondata.regions = []
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    # rundata.regiondata.regions.append([3, 3, 0., 10000., -85,-72,-38,-25])
    # rundata.regiondata.regions.append([3, 3, 8000., 26000., -90,-80,-30,-15])

    # == setgauges.data values ==
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    # rundata.gaugedata.gauges.append([32412, -86.392, -17.975, 0., 1.e10])

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
        geodata = rundata.geodata
    except:
        print "*** Error, this rundata has no geodata attribute"
        raise AttributeError("Missing geodata attribute")

    # == setgeo.data values ==

    geodata.variable_dt_refinement_ratios = False

    geodata.gravity = 9.81
    geodata.coordinate_system = 1
    geodata.earth_radius = 6367.5e3

    # Forcing options
    geodata.coriolis_forcing = False
    geodata.friction_forcing = True
    geodata.manning_coefficient = 0.025
    geodata.friction_depth = 20.0

    # == settsunami.data values ==
    geodata.dry_tolerance = 1.e-3
    geodata.wave_tolerance = 0.1
    geodata.speed_tolerance = [0.25,0.5,1.0,2.0,3.0,4.0]
    geodata.depthdeep = 2.e2
    geodata.maxleveldeep = 4

    # == settopo.data values ==
    geodata.topofiles = []
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]
    geodata.topofiles.append([2, 1, 5, 0., 1e10, 'topo.data'])
    
    # == setdtopo.data values ==
    # Unsupported in the multilayer case
    geodata.dtopofiles = []

    # == setqinit.data values ==
    qinitdata = rundata.qinitdata
    # Note that this is a different sort of perturbation from the single-layer
    # version.  These are idealized perturbations for the time being
    qinitdata.qinit_type = 6
    qinitdata.init_location = [0.25,0.25]
    qinitdata.wave_family = 4
    qinitdata.epsilon = 0.02
    qinitdata.angle = 0.0
    qinitdata.sigma = 0.02

    # == setfixedgrids.data values ==
    geodata.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]
    # geodata.fixedgrids.append([1., 2., 4, 0., 100., 0., 100., 11, 11, 0, 0])
    
    
    # # Bathy settings (2D is written out as a topo file)
    # data.bathy_type = 1
    # data.bathy_left = -1.0
    # data.bathy_location = 0.6
    # data.bathy_right = -0.2
    
    return rundata
    # end of function setgeo
    # ----------------------


def set_storm_data(rundata):

    data = rundata.stormdata
    
    # Storm parameters
    data.storm_type = 0 # Type of storm

    return data


def set_friction_data(rundata):

    data = rundata.frictiondata

    # Variable friction
    data.variable_friction = False

    return data

def set_multilayer_data(rundata):

    data = rundata.multilayerdata



    # Multilayer setup
    data.num_layers = 2
    data.rho = [0.90,1.0]
    data.eta_init = [0.0,-0.6]

    # Algorithm parameters
    data.check_richardson = False
    data.richardson_tolerance = 0.95
    data.eigen_method = 2
    data.inundation_method = 2


    # These values override GeoClaw parameters as per-layer options
    data.dry_tolerance = [1.e-3,1.e-3]
    data.wave_tolerance = [0.1,0.1]

    
# =====================
#  Main run function 
# =====================
if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    if len(sys.argv) == 2:
        rundata = setrun(sys.argv[1])
    else:
        rundata = setrun()

    # Add storm, friction and multilayer data to rundata object
    rundata.add_data(surge.data.SurgeData(),'stormdata')
    rundata.add_data(surge.data.FrictionData(),'frictiondata')
    rundata.add_data(multilayer.data.MultilayerData(),'multilayerdata')
    
    # Set additional data objects
    set_multilayer_data(rundata)
    set_friction_data(rundata)
    set_storm_data(rundata)

    # Write out all data
    rundata.write()
