#!/usr/bin/env python
# encoding: utf-8

"""Solution initialization routines for 1d multilayer swe examples"""

import numpy as np

# Aux array indices
bathy_index = 1
h_hat_index = 3

def set_jump_bathymetry(state,jump_location,depths):
    """
    Set bathymetry representing a jump from depths[0] to depths[1] at 
    jump_location.
    """
    x = state.grid.dimensions[0].centers
    state.aux[0,:] = (x < jump_location) * depths[0]  + \
                     (x >= jump_location) * depths[1]

def set_h_hat(state,jump_location,eta_left,eta_right):
    """Set the initial surfaces for Riemann solver use"""
    x_left = (state.grid.dimensions[0].centers < jump_location)
    x_right = (state.grid.dimensions[0].center >= jump_location)
    b = state.aux[bathy_index,:]
    
    state.aux[h_hat_index,:] = x_left  * (eta_left[1] > b)   * (eta_left[0] - eta_left[1]) \
                             + x_left  * (eta_left[1] <= b)  * (eta_left[0] - b) \
                             + x_right * (eta_right[1] > b)  * (eta_right[0] - eta_right[1]) \
                             + x_right * (eta_right[1] <= b) * (eta_right[0] - b)
    state.aux[h_hat_index+1,:] = x_left  * (eta_left[1] > b)   * (eta_left[1] - b) \
                               + x_left  * (eta_left[1] <= b)  * b \
                               + x_right * (eta_right[1] > b)  * (eta_right[1] - b) \
                               + x_right * (eta_right[1] <= b) * b
    
def set_quiescent_init_condition(state):
    """Set a quiescent (stationary) initial condition
    
    This assumes that you have already set the h hat values.
    """
    state.q[0,:] = state.aux[h_hat_index,:] * state.problem_data['rho'][0]
    state.q[2,:] = state.aux[h_hat_index+1,:] * state.problem_data['rho'][1]
    state.q[1,:] = np.zeros((state.grid.dimensions[0].num_cells[0]))
    state.q[3,:] = np.zeros((state.grid.dimensions[0].num_cells[0]))
    
def set_wave_family_init_condition(state,wave_family):
    """Set initial condition of a jump in the specified wave family"""
    
    # Set stationary initial state, perturb off of that
    set_quiescent_init_condition(state)
    
    raise NotImplemented("Wave family initial condition not yet implemented!")

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
