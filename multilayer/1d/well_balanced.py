#!/usr/bin/env python
# encoding: utf-8

r"""Test case for well balancing"""

import sys
import numpy

from clawpack.riemann import layered_shallow_water_1D
import clawpack.clawutil.runclaw as runclaw
from clawpack.pyclaw.plot import plot

import multilayer as ml
        
def smooth_test(eigen_method, dry=False, **kargs):
    r"""Smooth well-balanced test"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_d%s' % (eigen_method,dry)
    name = 'well_balancing_smooth'
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)
    
    # Redirect loggers
    # This is not working for all cases, see comments in runclaw.py
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
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
    # Use wall boundary condition at beach
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 1
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    
    # Set the Riemann solver
    solver.rp = layered_shallow_water_1D

    # Set the before step function
    solver.before_step = lambda solver,solution:ml.step.before_step(solver,
                                                                    solution)
                                            
    # Use simple friction source term
    solver.step_source = ml.step.friction_source

    
    # ============================
    # = Create Initial Condition =
    # ============================
    num_layers = 2
    
    x = pyclaw.Dimension('x',0.0,10.0,200)
    domain = pyclaw.Domain([x])
    state = pyclaw.State(domain,2*num_layers,3+num_layers)
    state.aux[ml.aux.kappa_index,:] = 0.0

    # Set physics data
    state.problem_data['g'] = 9.8
    state.problem_data['manning'] = 0.0
    state.problem_data['rho_air'] = 1.15
    state.problem_data['rho'] = [0.98,1.0]
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
    ml.aux.set_gaussian_bathymetry(solution.state,10.0,5,numpy.sqrt(5/2),5.0)
    ml.aux.set_no_wind(solution.state)
    if dry:
        ml.aux.set_h_hat(solution.state,0.5,[0.0,-6.0],[0.0,-6.0])
    else:
        ml.aux.set_h_hat(solution.state,0.5,[0.0,-4.0],[0.0,-4.0])

    # Set perturbation to sea at rest
    ml.qinit.set_quiescent_init_condition(solution.state)
    
    
    # ================================
    # = Create simulation controller =
    # ================================
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    
    # Output parameters
    controller.output_style = 1
    controller.tfinal = 10.0
    controller.num_output_times = 1
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
    plot_kargs = {"rho":solution.state.problem_data['rho'],
                  "dry_tolerance":solution.state.problem_data['dry_tolerance']}
    plot(setplot="./setplot_well_balanced.py",outdir=outdir,
         plotdir=plotdir, htmlplot=kargs.get('htmlplot',False),
         iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)


def jump_test(eigen_method, dry=False, **kargs):
    r"""Bathymetry with jump discontinuity"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_d%s' % (eigen_method,dry)
    name = 'well_balancing_jump'
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)
    
    # Redirect loggers
    # This is not working for all cases, see comments in runclaw.py
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
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
    # Use wall boundary condition at beach
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 1
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    
    # Set the Riemann solver
    solver.rp = riemann.layered_shallow_water_1D

    # Set the before step function
    solver.before_step = lambda solver,solution:ml.step.before_step(solver,
                                                                    solution)
                                            
    # Use simple friction source term
    solver.step_source = ml.step.friction_source

    
    # ============================
    # = Create Initial Condition =
    # ============================
    num_layers = 2
    
    x = pyclaw.Dimension('x',0.0,10.0,200)
    domain = pyclaw.Domain([x])
    state = pyclaw.State(domain,2*num_layers,3+num_layers)
    state.aux[ml.aux.kappa_index,:] = 0.0

    # Set physics data
    state.problem_data['g'] = 9.8
    state.problem_data['manning'] = 0.0
    state.problem_data['rho_air'] = 1.15
    state.problem_data['rho'] = [0.98,1.0]
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
    ml.aux.set_jump_bathymetry(solution.state,5.0,[-10.0,-5.0])
    ml.aux.set_no_wind(solution.state)
    if dry:
        ml.aux.set_h_hat(solution.state,0.5,[0.0,-6.0],[0.0,-6.0])
    else:
        ml.aux.set_h_hat(solution.state,0.5,[0.0,-4.0],[0.0,-4.0])

    # Set perturbation to sea at rest
    ml.qinit.set_quiescent_init_condition(solution.state)
    
    
    # ================================
    # = Create simulation controller =
    # ================================
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    
    # Output parameters
    controller.output_style = 1
    controller.tfinal = 10.0
    controller.num_output_times = 1
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
    plot_kargs = {"rho":solution.state.problem_data['rho'],
                  "dry_tolerance":solution.state.problem_data['dry_tolerance']}
    plot(setplot="./setplot_well_balanced.py",outdir=outdir,
         plotdir=plotdir, htmlplot=kargs.get('htmlplot',False),
         iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)


if __name__ == "__main__":
    # Run the test for the requested eigen methods for the jump and slope bathys
    if len(sys.argv) > 1:
        eig_methods = []
        for value in sys.argv[1:]:
            eig_methods.append(int(value))
    else:
        eig_methods = [2]
    
    for dry in [True, False]:    
        for method in eig_methods:
            smooth_test(method, dry=dry, iplot=False, htmlplot=True)
            jump_test(method, dry=dry, iplot=False, htmlplot=True)