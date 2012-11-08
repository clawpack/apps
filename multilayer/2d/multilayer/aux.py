# encoding: utf-8

r"""Modules contains information about the aux array used in the multi-layer
swe computations."""

import numpy as np

# Define aux array indices
bathy_index = 0
wind_index = [3,4]
pressure_index = 5
h_hat_index = [6,7]
vorticity_index = 9

# ==============================================
# = Sets values of h_hat for linearized solver =
# ==============================================
def set_h_hat(state,jump_location,eta_left,eta_right):
    """Set the initial surfaces for Riemann solver use"""
    b = state.aux[bathy_index,...]
    x = state.grid.dimensions[0].centers
    left_location = x < jump_location
    right_location = x >= jump_location
    
    state.aux[h_hat_index[0],...] = left_location * (eta_left[1] > b) * (eta_left[0] - eta_left[1]) + \
                                    left_location * (eta_left[1] <= b) * (eta_left[0] - b) + \
                                    right_location * (eta_right[1] > b) * (eta_right[0] - eta_right[1]) + \
                                    right_location * (eta_right[1] <= b) * (eta_right[0] - b)
                                    
    state.aux[h_hat_index[1],...] = left_location * (eta_left[1] > b) * (eta_left[1] - b) + \
                                    left_location * (eta_left[1] <= b) *np.zeros(b.shape) + \
                                    right_location * (eta_right[1] > b) * (eta_right[1] - b) + \
                                    right_location * (eta_right[1] <= b) * np.zeros(b.shape)


# ==================
# = Wind functions =
# ==================
def set_no_wind(state):
    """Set wind field to zero"""
    state.aux[wind_index,...] = 0.0


# ========================
# = Bathymetry functions =
# ========================
def set_jump_bathymetry(state,jump_location,depths):
    """
    Set bathymetry representing a jump from depths[0] to depths[1] at 
    jump_location.
    
    This works for 1 and 2 dimensions assuming that the x-dimension is the
    first available in the grid object.
    """
    
    x = state.grid.dimensions[0].centers
    state.aux[bathy_index,...] = (x < jump_location) * depths[0]  + \
                               (x >= jump_location) * depths[1]
                               
def set_sloped_shelf_bathymetry(state,x0,x1,basin_depth,shelf_depth):
    r"""
    Set bathymetry to a simple shelf with a slope coming up from the basin
    
        (x1,shelf_depth) *-----------
                        /
                      /
                    /
        ___________* (x0,basin_depth)
    
    This works for 1 and 2 dimensions assuming that the x-dimension is the
    first available in the grid object.
    """
    
    x = state.grid.dimensions[0].centers
    slope = (basin_depth - shelf_depth) / (x0 - x1) * (x - x0) + basin_depth
    
    state.aux[bathy_index,...] = (x < x0) * basin_depth
    state.aux[bathy_index,...] += (x0 <= x) * (x < x1) * slope
    state.aux[bathy_index,...] += (x1 <= x) * shelf_depth
