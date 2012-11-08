# encoding: utf-8

r"""
Functions for intializing q

Note there are a number of unimplmented intialization functions here mainly 
becuase they were in the original Fortran code.
"""

import numpy as np

# Get locations in the aux array of pertinent quantities
from aux import kappa_index,h_hat_index

def set_riemann_init_condition(state,jump_location,q_left,q_right):
    r"""Set a Riemann type initial condition"""

    x = state.grid.dimensions[0].centers
            
    for m in xrange(state.num_eqn):
        state.q[m,...] = (x < jump_location) * q_left[m] * np.ones(state.grid.num_cells) + \
                         (x >= jump_location) * q_right[m] * np.ones(state.grid.num_cells)
    

def set_quiescent_init_condition(state):
    """Set a quiescent (stationary) initial condition
    
    This assumes that you have already set the h hat values and the densities.
    """
    state.q[0,:] = state.aux[h_hat_index[0],...] * state.problem_data['rho'][0]
    state.q[1,:] = np.zeros(state.grid.num_cells)
    state.q[2,:] = np.zeros(state.grid.num_cells)
    state.q[3,:] = state.aux[h_hat_index[1],...] * state.problem_data['rho'][1]
    state.q[4,:] = np.zeros(state.grid.num_cells)
    state.q[5,:] = np.zeros(state.grid.num_cells)

    

def set_wave_family_init_condition(state,wave_family,jump_location,epsilon):
    """Set initial condition of a jump in the specified wave family
    
    Note that these only work in the x-direction"""
    
    # Set stationary initial state, perturb off of that
    set_quiescent_init_condition(state)
    
    raise NotImplemented("Wave family init condition not implemented.")
    
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


def set_gaussian_init_condition(state,A,location,sigma,internal_layer=False):
    """Set initial condition to a gaussian hump of water
    
    Sets the condition for what should act like a shallow water wave.  If a
    gaussian on only the interal layer is desired set internal_only = True
    """
    
    # Set stationary initial state, perturb off of that
    set_quiescent_init_condition(state)
    
    raise NotImplemented("Gaussian initial condition not yet implemented!")
    

def set_acta_numerica_init_condition(state,epsilon):
    """Set initial condition based on the intitial condition in
    
    LeVeque, R. J., George, D. L. & Berger, M. J. Tsunami Propagation and 
    inundation with adaptively refined finite volume methods. Acta Numerica 
    211–289 (2011).  doi:10.1017/S0962492904
    """
    
    # Set stationary initial state, perturb off of that
    set_quiescent_init_condition(state)

    rho = state.problem_data['rho']
    x = state.grid.dimensions[0].centers
    
    gamma = state.aux[h_hat_index[1],...] / state.aux[h_hat_index[0],...]
    alpha = 0.0
    xmid = 0.5 * (-180e3 - 80e3)
    
    deta = epsilon * np.sin((x-xmid) * np.pi / (-80e3 - xmid))
    state.q[2,...] += (x > -130e3) * (x < -80e3) * rho[1] * alpha * deta
    state.q[0,...] += (x > -130e3) * (x < -80e3) * rho[0] * deta * (1.0 - alpha)
