#!/usr/bin/env python
# encoding: utf-8

r""" Run the suite of tests for the 1d two-layer equations"""

import os
import sys
import types

import numpy as np

from pyclaw.plot import plot
import clawutil.runclaw as runclaw

# Add src/python local directory to python path for multilayer specific tests
sys.path.append('../src/python/')

import multilayer as ml
        
def dry_state(num_cells,eigen_method,entropy_fix,**kargs):
    r"""docstring for oscillatory_wind"""
    
    # Parameters
    num_layers = 2
    kappa_index = ml.aux_index_1d.index('kappa')
    bathy_index = ml.aux_index_1d.index('bathy')
    
    # Extract possible keyword arguments
    use_petsc = kargs.get('use_petsc',False)
    solver_type = kargs.get('solver_type','classic')

    # Construct output and plot directory paths
    name = 'dry_state'
    prefix = 'ml_e%s_m%s_fix' % (eigen_method,num_cells)
    
    if entropy_fix:
        prefix = "".join((prefix,"T"))
    else:
        prefix = "".join((prefix,"F"))
    outdir,plotdir,log_path = runclaw.create_output_paths(name,prefix,**kargs)
    
    # =========================================================================
    # Load in appropriate PyClaw library
    if use_petsc:
        import petclaw as pyclaw
    else:
        import pyclaw
    
    # Redirect loggers to output to the log path requested
    runclaw.replace_stream_handlers('io',log_path,log_file_append=False)
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
        runclaw.replace_stream_handlers(logger_name,log_path)
        
    # =========================================================================
    # Create solver object
    if solver_type == 'classic':
        solver = pyclaw.ClawSolver1D()
    else:
        raise NotImplementedError("Classic is the only solver type supported currently")
        
    # Solver parameters
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 1
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    solver.cfl_desired = 0.9
    solver.cfl_max = 1.0
    solver.max_steps = 5000
    solver.fwave = True
    solver.kernel_language = 'Fortran'
    solver.num_waves = 4
    solver.limiters = 3
    solver.source_split = 1
        
    # Setup Riemann solver
    import riemann
    solver.rp = riemann.rp1_layered_shallow_water
    
    # Set callback functions    
    solver.before_step = lambda solver,solution:ml.before_step(solver,solution
                                                    ,stop_on_fail=False)
    solver.step_source = ml.source.friction_source_1d
            
    # =========================================================================
    # Create solution
    x = pyclaw.Dimension('x',0.0,1.0,num_cells)
    domain = pyclaw.Domain([x])
    state = pyclaw.State(domain,2*num_layers,3+num_layers)
    state.aux[kappa_index,:] = 0.0

    # Set physics data
    state.problem_data['g'] = 9.8
    state.problem_data['manning'] = 0.0
    state.problem_data['rho_air'] = 1.15e-3
    state.problem_data['rho'] = [0.95,1.0]
    state.problem_data['r'] = state.problem_data['rho'][0] / state.problem_data['rho'][1]
    state.problem_data['one_minus_r'] = 1.0 - state.problem_data['r']
    state.problem_data['num_layers'] = num_layers
        
    # Need to send some problem parameters through to the fortran
    state.problem_data['dry_tolerance'] = 1e-3
    state.problem_data['eigen_method'] = eigen_method
    state.problem_data['inundation_method'] = 2
    state.problem_data['entropy_fix'] = entropy_fix
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    ml.bathy.set_jump_bathymetry(state,0.5,[-1.0,-1.0])
    ml.wind.set_no_wind(state)
    ml.qinit.set_h_hat(state,0.5,[0.0,-0.5],[0.0,-1.0])
    
    solution = pyclaw.Solution(state,domain)
    solution.t = 0.0
    
    # =========================================================================
    # Create controller
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    controller.output_style = 1
    controller.tfinal = 0.5
    controller.num_output_times = 50
    controller.outdir = './_output'
    controller.write_aux_init = True
    controller.write_aux_always = False
    
    # Set output
    controller.outdir = outdir
    controller.output_style = 3
    controller.nstepout = 1
    controller.num_output_times = 100
    controller.write_aux = True
    
    # Run simulation
    status = controller.run()
    print status
    
    # Plotting
    plot_kargs = {'rho':solution.state.problem_data['rho'],
                  'dry_tolerance':solution.state.problem_data['dry_tolerance']}
    plot(setplot_path="./setplot_drystate.py",outdir=outdir,plotdir=plotdir,
         htmlplot=kargs.get('htmlplot',False),iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)

if __name__ == "__main__":
    # Run test case for eigen method = 2 turning on and off entropy fix
    dry_state(500,2,True)
    dry_state(500,2,False)