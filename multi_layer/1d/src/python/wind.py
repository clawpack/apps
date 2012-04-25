#!/usr/bin/env python
# encoding: utf-8

"""Functions for including wind fields in the 1d swe equations

The parameter WIND_FIELD controls which field is assumed to contain the wind
field in the aux array.  Also includes a function for calculating the wind
drag coefficient.
"""

import numpy as np

WIND_FIELD = 1

def set_no_wind(state):
    """Set wind field to zero"""
    state.aux[WIND_FIELD,:] = 0.0

def set_oscillatory_wind(state,A=5.0,N=2.0,omega=2.0,t_length=10.0):
    """Assigns an oscillatory wind field to state
    
    """
    print "here at t=%s" % state.t
    L = state.grid.upper[0] - state.grid.lower[0]
    x = state.grid.dimensions[0].centers
    state.aux[WIND_FIELD,:] = A * np.sin(np.pi*N*x/L) \
                       * np.sin(2.0*np.pi*omega/t_length*state.t)


def wind_drag(wind_speed):
    """Calculate wind drag coefficient
    
    Piece-wise defined, limited function for effective wind drag
    """

    if wind_speed <= 11.0:
        wind_drag = 1.2
    elif wind_speed > 11.0 and wind_speed <= 25.0:
        wind_drag = 0.49 + 0.065 * wind_speed
    else:
        wind_drag = 0.49 + 0.065 * 25.0
        
    return wind_drag * 1e-2
