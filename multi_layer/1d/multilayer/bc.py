#!/usr/bin/env python
# encoding: utf-8

r"""
Module containing boundary condition routines for the multilayer
shallow water equations.

:Available Routines:
    1D - Wall boundary conditions
    2D - None
"""

# ==========================
# = 1 Dimensional Routines =
# ==========================
def wall_qbc_lower_1d(state,dim,t,qbc,num_ghost):
    for i in xrange(num_ghost):
        qbc[0,i] = qbc[0,num_ghost]
        qbc[1,i] = -qbc[1,num_ghost]
        qbc[2,i] = qbc[2,num_ghost]
        qbc[3,i] = -qbc[3,num_ghost]
    
def wall_qbc_upper_1d(state,dim,t,qbc,num_ghost):
    for i in xrange(num_ghost + dim.num_cells,
                    2*num_ghost + dim.num_cells):
        qbc[0,i] = qbc[0,num_ghost + dim.num_cells-1]
        qbc[1,i] = -qbc[1,num_ghost + dim.num_cells-1]
        qbc[2,i] = qbc[2,num_ghost + dim.num_cells-1]
        qbc[3,i] = -qbc[3,num_ghost + dim.num_cells-1]

# ==========================
# = 2 Dimensional Routines =
# ==========================
