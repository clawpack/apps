#!/usr/bin/env python
# encoding: utf-8

r""" Run the suite of tests for the 1d two-layer equations"""

from clawpack.riemann import layered_shallow_water_1D
import clawpack.clawutil.runclaw as runclaw
from clawpack.pyclaw.plot import plot

import multilayer as ml
        
def rarefaction(num_cells,eigen_method,entropy_fix,**kargs):
    r"""docstring for oscillatory_wind"""

    # Construct output and plot directory paths
    prefix = 'ml_e%s_m%s_fix' % (eigen_method,num_cells)
    if entropy_fix:
        prefix = "".join((prefix,"T"))
    else:
        prefix = "".join((prefix,"F"))
    name = 'multilayer/all_rare'
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
    solver.bc_lower[0] = 1
    solver.bc_upper[0] = 1
    solver.aux_bc_lower[0] = 1
    solver.aux_bc_upper[0] = 1
    
    # Set the Riemann solver
    solver.rp = layered_shallow_water_1D

    # Set the before step function
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
    state.problem_data['entropy_fix'] = entropy_fix
    
    solution = pyclaw.Solution(state,domain)
    solution.t = 0.0
    
    # Set aux arrays including bathymetry, wind field and linearized depths
    eta = [0.0,-0.5]
    ml.aux.set_jump_bathymetry(solution.state,0.5,[-1.0,-1.0])
    ml.aux.set_no_wind(solution.state)
    ml.aux.set_h_hat(solution.state,0.5,eta,eta)
    
    # Set sea at rest initial condition with diverging velocities
    u_left = [0.0,-0.5]
    u_right = [0.0,0.5]
    h_hat = [eta[0] - eta[1],eta[1] + 1.0]
    q_left = [h_hat[0] * state.problem_data['rho'][0],
              u_left[0] * h_hat[0] * state.problem_data['rho'][0],
              h_hat[1] * state.problem_data['rho'][1],
              u_left[1] * h_hat[1] * state.problem_data['rho'][1]]

    q_right = [h_hat[0] * state.problem_data['rho'][0],
               u_right[0] * h_hat[0] * state.problem_data['rho'][0],
               h_hat[1] * state.problem_data['rho'][1],
               u_right[1] * h_hat[1] * state.problem_data['rho'][1]]
    ml.qinit.set_riemann_init_condition(state,0.5,q_left,q_right)
    
    
    # ================================
    # = Create simulation controller =
    # ================================
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    
    # Output parameters
    controller.output_style = 3
    controller.nstepout = 1
    controller.num_output_times = 100
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
    plot_kargs = {'rho':solution.state.problem_data['rho'],
                  'dry_tolerance':solution.state.problem_data['dry_tolerance']}
    plot(setplot="./setplot_drystate.py",outdir=outdir,plotdir=plotdir,
         htmlplot=kargs.get('htmlplot',False),iplot=kargs.get('iplot',False),
         file_format=controller.output_format,**plot_kargs)

if __name__ == "__main__":
    rarefaction(100,2,False,iplot=False,htmlplot=True)