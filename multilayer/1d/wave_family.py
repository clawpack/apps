#!/usr/bin/env python
# encoding: utf-8

r""" Run the suite of tests for the 1d two-layer equations"""

import sys

from clawpack.riemann import layered_shallow_water_1D
import clawpack.clawutil.runclaw as runclaw
from clawpack.pyclaw.plot import plot

import multilayer as ml
        
def wave_family(num_cells,eigen_method,wave_family,dry_state=True,**kargs):
    r"""docstring for oscillatory_wind"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_n%s' % (eigen_method,num_cells)
    if dry_state:
        name = 'multilayer/dry_wave_%s' % wave_family
    else:
        name = 'multilayer/wet_wave_%s' % wave_family
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)
    
    # Redirect loggers
    # This is not working for all cases, see comments in runclaw.py
    for logger_name in ['pyclaw.io','pyclaw.solution','plot','pyclaw.solver','f2py','data']:
        runclaw.replace_stream_handlers(logger_name,log_path,log_file_append=False)

    # Load in appropriate PyClaw version
    if kargs.get('use_petsc',False):
        import clawpack.petclaw as pyclaw
    else:
        import clawpack.pyclaw as pyclaw

    # =================
    # = Create Solver =
    # =================
    if kargs.get('solver_type','classic') == 'classic':
        solver = pyclaw.ClawSolver1D()
    else:
        raise NotImplementedError('Classic is currently the only supported solver.')
        
    # Solver method parameters
    solver.cfl_desired = 0.9
    solver.cfl_max = 1.0
    solver.max_steps = 5000
    solver.fwave = True
    solver.kernel_language = 'Fortran'
    solver.num_waves = 4
    solver.limiters = 3
    solver.source_split = 1
        
    # Boundary conditions
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 1
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1

    # Set the Riemann solver
    solver.rp = layered_shallow_water_1D

    # Set the before step functioning including the wind forcing
    solver.before_step = lambda solver,solution:ml.step.before_step(solver,solution)
                                            
    # Use simple friction source term
    solver.step_source = ml.step.friction_source
    
    
    # ============================
    # = Create Initial Condition =
    # ============================
    num_layers = 2
    
    x = pyclaw.Dimension('x',0.0,1.0,num_cells)
    domain = pyclaw.Domain([x])
    state = pyclaw.State(domain,2*num_layers,3+num_layers)
    state.aux[ml.aux.kappa_index,:] = 0.0

    # Set physics data
    state.problem_data['g'] = 9.8
    state.problem_data['manning'] = 0.0
    state.problem_data['rho_air'] = 1.15e-3
    state.problem_data['rho'] = [0.95,1.0]
    state.problem_data['r'] = state.problem_data['rho'][0] / state.problem_data['rho'][1]
    state.problem_data['one_minus_r'] = 1.0 - state.problem_data['r']
    state.problem_data['num_layers'] = num_layers
    
    # Set method parameters, this ensures it gets to the Fortran routines
    state.problem_data['eigen_method'] = eigen_method
    state.problem_data['dry_tolerance'] = 1e-3
    state.problem_data['inundation_method'] = 2
    state.problem_data['entropy_fix'] = False
    
    solution = pyclaw.Solution(state,domain)
    solution.t = 0.0
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    if dry_state:
        ml.aux.set_jump_bathymetry(solution.state,0.5,[-1.0,-0.2])
    else:
        ml.aux.set_jump_bathymetry(solution.state,0.5,[-1.0,-1.0])
    ml.aux.set_no_wind(solution.state)
    ml.aux.set_h_hat(solution.state,0.5,[0.0,-0.6],[0.0,-0.6])
    
    # Set initial condition
    if wave_family == 3:
        ml.qinit.set_wave_family_init_condition(solution.state,wave_family,0.45,0.1)
    elif wave_family == 4:
        # The perturbation must be less in this case otherwise the internal
        # wave will crest the bathymetry jump
        ml.qinit.set_wave_family_init_condition(solution.state,wave_family,0.45,0.04)

    
    # ================================
    # = Create simulation controller =
    # ================================
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    
    # Output parameters
    controller.output_style = 1
    controller.tfinal = 0.5
    controller.num_output_times = 50
    controller.write_aux_init = True
    controller.outdir = outdir
    controller.write_aux = True
    
    # ==================
    # = Run Simulation =
    # ==================
    state = controller.run()
    
    # ============
    # = Plotting =
    # ============
    plot_kargs = {'wave_family':wave_family,
                  'rho':solution.state.problem_data['rho'],
                  'dry_tolerance':solution.state.problem_data['dry_tolerance']}
    plot(setplot="./setplot_wave_family.py",outdir=outdir,plotdir=plotdir,
         htmlplot=kargs.get('htmlplot',False),iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)


if __name__ == "__main__":
    # Run the test for the 3rd and 4th wave families for each eigen method
    if len(sys.argv) > 1:
        eig_methods = []
        for value in sys.argv[1:]:
            eig_methods.append(int(value))
    else:
        eig_methods = [1,2,3,4]

    # Display runs
    resolution = 500
    for family in [3,4]:
        for dry_state in [False,True]:
            for method in eig_methods:
                print "Running family=%s dry=%s eigen=%s resolution=%s" % (family,dry_state,method,resolution)
                wave_family(resolution,method,family,dry_state,iplot=False,htmlplot=True)

    # Resolutions for tests
    # resolutions = [64,128,256,512,1024,5000]

    # Run for comparison runs
    # for family in [3,4]:
    #     for dry_state in [False,True]:
    #         for method in eig_methods:
    #             for resolution in resolutions:
    #                 print "Running family=%s dry=%s eigen=%s resolution=%s" % (family,dry_state,method,resolution)
    #                 wave_family(resolution,method,family,dry_state,iplot=False,htmlplot=False)
