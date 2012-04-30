#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import types
import glob

import numpy as np

import wind
import clawutil.runclaw as runclaw

# Aux array indices
bathy_index = 0
wind_index = 1
h_hat_index = [2,3]
kappa_index = 4

# Function called before each time step
def before_step(solver,solution,wind_func=wind.set_no_wind,
                dry_tolerance=1e-3,richardson_tolerance=0.95,
                stop_on_fail=False):
    r""""""
    # Extract relevant data
    num_layers = solution.states[0].problem_data['num_layers']
    rho = solution.states[0].problem_data['rho']
    g = solution.states[0].problem_data['g']
    one_minus_r = solution.states[0].problem_data['one_minus_r']
    
    # State arrays
    q = solution.states[0].q
    aux = solution.states[0].aux
    
    # Zero out negative values
    q = q * (q > 0.0)
    
    # Calculate wind
    wind_func(solution.state)
    # Want to apply new aux values into auxbc
    solver.apply_aux_bcs(solution.state)
    
    # Calculate kappa
    h = np.zeros((num_layers,q.shape[1]))
    u = np.zeros(h.shape)
    for layer in xrange(num_layers):
        layer_index = 2*layer
        h[layer,:] = solution.q[layer_index,:] / rho[layer]
        wet_index = h[layer,:] > dry_tolerance
        u[layer,wet_index] = solution.q[layer_index+1,wet_index] / solution.q[layer_index,wet_index]
    aux[kappa_index,:] = (u[0,:] - u[1,:])**2 / (g * one_minus_r * (h[0,:] + h[1,:]))
    if np.any(aux[kappa_index,wet_index] > richardson_tolerance):
        # Actually calculate where the indices failed
        bad_indices = (aux[kappa_index,wet_index] > richardson_tolerance).nonzero()[0]
        print "Hyperbolicity may have failed at the following points:"
        for i in bad_indices:
            print "\tkappa(%s) = %s" % (i,aux[kappa_index,i+1])
        if stop_on_fail:
            raise Exception("Richardson tolerance exceeded!")
            

# Friction source function
def friction_source(solver,state,dt,TOLERANCE=1e-30):
    r""""""
    num_layers = state.problem_data['num_layers']
    manning = state.problem_data['manning']
    g = state.problem_data['g']
    rho = state.problem_data['rho']
    dry_tolerance = state.problem_data['dry_tolerance']
    
    if manning > TOLERANCE:

        for i in xrange(state.q.shape[1]):
            h = state.q[2,i] / rho[1]
            if h < dry_tolerance:
                h = state.q[0,i] / rho[0]
                u = state.q[1,i] / rho[0]
                layer_index = 0
            else:
                u = state.q[2,i] / rho[1]
                layer_index = 1
        
            gamma = u * g * manning**2 / h**(4/3)
            dgamma = 1.0 + dt * gamma
            hu_index = 2 * (layer_index) + 1
            state.q[hu_index,i] = state.q[hu_index,i] / dgamma * rho[layer_index]

            
def setup(lower=0.0,upper=1.0,num_layers=2,num_cells=100,log_path='./pyclaw.log',
          use_petsc=False,iplot=False,htmlplot=False,outdir='./_output',solver_type='classic'):
    r"""Generic setup routine for all 1d multi-layer runs in PyClaw
    
    :Input:
    
    :Output:
     - *solver* (pyclaw.solver) 
     - *solution* (pyclaw.solution)
     - *controller* (pyclaw.controller)
    """
    
    # Load in appropriate PyClaw library
    if use_petsc:
        import petclaw as pyclaw
    else:
        import pyclaw
    
    # Redirect loggers
    runclaw.replace_stream_handlers('io',log_path,log_file_append=False)
    for logger_name in ['io','solution','plot','evolve','f2py','data']:
        runclaw.replace_stream_handlers(logger_name,log_path)
        
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
    solver.before_step = before_step
    solver.step_source = friction_source
            
    # Create solution
    x = pyclaw.Dimension('x',lower,upper,num_cells)
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
    state.problem_data['eigen_method'] = 2
    state.problem_data['inundation_method'] = 2
    state.problem_data['entropy_fix'] = False
        
    solution = pyclaw.Solution(state,domain)
    solution.t = 0.0
    
    # Create controller
    controller = pyclaw.Controller()
    controller.solution = solution
    controller.solver = solver
    controller.output_style = 1
    controller.tfinal = 0.5
    controller.num_output_times = 50
    controller.outdir = './_output'
    controller.write_aux_init = True
    
    return solver,solution,controller


def set_jump_bathymetry(state,jump_location,depths):
    """
    Set bathymetry representing a jump from depths[0] to depths[1] at 
    jump_location.
    """
    
    x = state.grid.dimensions[0].centers
    state.aux[bathy_index,:] = (x < jump_location) * depths[0]  + \
                               (x >= jump_location) * depths[1]

def set_h_hat(state,jump_location,eta_left,eta_right):
    """Set the initial surfaces for Riemann solver use"""
    b = state.aux[bathy_index,:]

    for (i,x) in enumerate(state.grid.dimensions[0].centers):
        if x < jump_location:
            if eta_left[1] > b[i]:
                state.aux[h_hat_index[0],i] = eta_left[0] - eta_left[1]
                state.aux[h_hat_index[1],i] = eta_left[1] - b[i]
            else:
                state.aux[h_hat_index[0],i] = eta_left[0] - b[i]
                state.aux[h_hat_index[1],i] = 0.0
        else:
            if eta_right[1] > b[i]:
                state.aux[h_hat_index[0],i] = eta_right[0] - eta_right[1]
                state.aux[h_hat_index[1],i] = eta_right[1] - b[i]
            else:
                state.aux[h_hat_index[0],i] = eta_right[0] - b[i]
                state.aux[h_hat_index[1],i] = 0.0
    
def set_quiescent_init_condition(state):
    """Set a quiescent (stationary) initial condition
    
    This assumes that you have already set the h hat values.
    """
    state.q[0,:] = state.aux[h_hat_index[0],:] * state.problem_data['rho'][0]
    state.q[2,:] = state.aux[h_hat_index[1],:] * state.problem_data['rho'][1]
    state.q[1,:] = np.zeros((state.grid.dimensions[0].num_cells))
    state.q[3,:] = np.zeros((state.grid.dimensions[0].num_cells))
    
def set_wave_family_init_condition(state,wave_family,jump_location,epsilon):
    """Set initial condition of a jump in the specified wave family"""
    
    # Set stationary initial state, perturb off of that
    set_quiescent_init_condition(state)
    
    r = state.problem_data['r']
    rho = state.problem_data['rho']
    g = state.problem_data['g']

    for (i,x) in enumerate(state.grid.dimensions[0].centers):
        gamma = state.aux[h_hat_index[1],i] / state.aux[h_hat_index[0],i]
        if wave_family == 1:
            alpha = 0.5 * (gamma - 1.0 + np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
            eig_value = -np.sqrt(g * state.aux[h_hat_index[0],i] * (1.0 + alpha))
        elif wave_family == 2:
            alpha = 0.5 * (gamma - 1.0 - np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
            eig_value = -np.sqrt(g * state.aux[h_hat_index[0],i] * (1.0 + alpha))
        elif wave_family == 3:
            alpha = 0.5 * (gamma - 1.0 - np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
            eig_value = np.sqrt(g * state.aux[h_hat_index[0],i] * (1.0 + alpha))
        elif wave_family == 4:
            alpha = 0.5 * (gamma - 1.0 + np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
            eig_value = np.sqrt(g * state.aux[h_hat_index[0],i] * (1.0 + alpha))
        else:
            raise Exception("Unsupported wave family %s requested!" % wave_family)
            
        if x < jump_location and wave_family >= 3:
            state.q[0,i] += rho[0] * epsilon
            state.q[1,i] += rho[0] * epsilon * eig_value
            state.q[2,i] += rho[1] * epsilon * alpha
            state.q[3,i] += rho[1] * epsilon * eig_value * alpha
        elif x >= jump_location and wave_family < 3:
            state.q[0,i] += rho[0] * epsilon
            state.q[1,i] += rho[0] * epsilon * eig_value
            state.q[2,i] += rho[1] * epsilon * alpha
            state.q[3,i] += rho[1] * epsilon * eig_value * alpha
            
    # x = state.grid.dimensions[0].centers
    # 
    # gamma = state.aux[h_hat_index[1],:] / state.aux[h_hat_index[0],:]
    # if wave_family == 1:
    #     alpha = 0.5 * (gamma - 1.0 + np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
    #     eig_value = -np.sqrt(g*state.aux[h_hat_index[0],:]*(1.0+alpha))
    # elif wave_family == 2:
    #     alpha = 0.5 * (gamma - 1.0 - np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
    #     eig_value = -np.sqrt(g*state.aux[h_hat_index[0],:]*(1.0+alpha))
    # elif wave_family == 3:
    #     alpha = 0.5 * (gamma - 1.0 - np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
    #     eig_value = np.sqrt(g*state.aux[h_hat_index[0],:]*(1.0+alpha))
    # elif wave_family == 4:
    #     alpha = 0.5 * (gamma - 1.0 + np.sqrt((gamma - 1.0)**2 + 4.0 * r * gamma))
    #     eig_value = np.sqrt(g*state.aux[h_hat_index[0],:]*(1.0+alpha))
    # else:
    #     raise Exception("Unsupported wave family %s requested." % wave_family)
    # 
    # if wave_family >= 3:
    #     location_condition = x < jump_location
    #     state.q[0,:] += location_condition * rho[0] * epsilon
    #     state.q[1,:] += location_condition * rho[0] * epsilon * eig_value
    #     state.q[2,:] += location_condition * rho[1] * epsilon * alpha
    #     state.q[3,:] += location_condition * rho[1] * epsilon * alpha * eig_value
    # elif wave_family < 3:
    #     location_condition = (x > jump_location)
    #     state.q[0,:] += location_condition * rho[0] * epsilon
    #     state.q[1,:] += location_condition * rho[0] * epsilon * eig_value
    #     state.q[2,:] += location_condition * rho[1] * epsilon * alpha
    #     state.q[3,:] += location_condition * rho[1] * epsilon * alpha * eig_value
    

def set_gaussian_init_condition(state,A,location,sigma,internal_layer=False):
    """Set initial condition to a gaussian hump of water
    
    Sets the condition for what should act like a shallow water wave.  If a
    gaussian on only the interal layer is desired set internal_only = True
    """
    
    # Set stationary initial state, perturb off of that
    set_quiescent_init_condition(state)
    
    raise NotImplemented("Gaussian initial condition not yet implemented!")
    
def set_acta_numerica_init_condition(state,A):
    """Set initial condition based on the intitial condition in
    
    LeVeque, R. J., George, D. L. & Berger, M. J. Tsunami Propagation and 
    inundation with adaptively refined finite volume methods. Acta Numerica 
    211–289 (2011).  doi:10.1017/S0962492904
    """
    
    # Set stationary initial state, perturb off of that
    set_quiescent_init_condition(state)
    
    raise NotImplemented("Acta Numerica initial condition not yet implemented!")
    
    
            
