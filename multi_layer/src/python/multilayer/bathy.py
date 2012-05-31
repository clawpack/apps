# encoding: utf-8
r"""
Module contains functions for setting bathymetry
"""

def set_jump_bathymetry(state,jump_location,depths):
    """
    Set bathymetry representing a jump from depths[0] to depths[1] at 
    jump_location.
    
    This works for 1 and 2 dimensions assuming that the x-dimension is the
    first available in the grid object.
    """

    bathy_index = 1
    
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

    bathy_index = 1
    
    x = state.grid.dimensions[0].centers
    slope = (basin_depth - shelf_depth) / (x0 - x1) * (x - x0) + basin_depth
    
    state.aux[bathy_index,...] = (x < x0) * basin_depth
    state.aux[bathy_index,...] += (x0 <= x) * (x < x1) * slope
    state.aux[bathy_index,...] += (x1 <= x) * shelf_depth