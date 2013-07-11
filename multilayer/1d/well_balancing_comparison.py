#!/usr/bin/env python

r"""Script for computing the error due to a non-well-balanced method"""

import os

import numpy

import clawpack.pyclaw.solution as solution

# Parameters
sea_level = 0.0

def compute_error(q, aux, eta, rho, norm=1):
    r"""Compute the steady state error where eta are the surfaces"""

    num_cells = q.shape[1]

    # Create h from eta for true solution, assumes top layer is not dry
    h_true = numpy.empty((2,num_cells))
    hu_true = numpy.zeros((2,num_cells))
    eta_true = numpy.zeros((2,num_cells))
    h_compare = numpy.zeros((2,num_cells))
    h_compare[0,:] = numpy.ones(num_cells) * eta[1] - aux[0,:]
    h_true[1,:] = numpy.max(h_compare, axis=0)
    eta_true[0,:] = numpy.zeros(num_cells)
    eta_true[1,:] = h_true[1,:] + aux[0,:]
    h_true[0,:] = (numpy.ones(num_cells) * eta[0] - (h_true[1,:] + aux[0,:])) * rho[0]
    h_true[1,:] = h_true[1,:] * rho[1]

    h = []
    hu = []
    eta_comp = []
    h.append(q[0,...])
    h.append(q[2,...])
    hu.append(q[1,...])
    hu.append(q[3,...])
    eta_comp.append(h[0] / rho[0] + h[1] / rho[1] + aux[0,...])
    eta_comp.append(h[1] / rho[1] + aux[0,...])

    layers = 2
    error = numpy.empty(3*layers)
    for i in xrange(layers):
        error[3*i] = numpy.linalg.norm(h[i] - h_true[i,:], ord=norm)
        error[3*i+1] = numpy.linalg.norm(hu[i] - hu_true[i,:], ord=norm)
        error[3*i+2] = numpy.linalg.norm(eta_comp[i] - eta_true[i,:], ord=norm)

    return error


def sig_fig_round(x, figs=1):
    for (i,value) in enumerate(x):
        if value != 0.0:
            x[i] = numpy.round(value, -int(numpy.floor(numpy.log10(value))) + (figs - 1))
    # Truncate digits
    raw_string = r"%." + str(figs) + "g"
    x = [float(raw_string % value) for value in x]
    return x


if __name__ == '__main__':
    # Construct path to solutions
    data_path = os.environ["DATA_PATH"]
    eigen_method = 2
    rho = [0.98, 1.0]
    for test in ['smooth','jump']:
        for dry in [True, False]:
            sol_path = os.path.join(data_path,"well_balancing_%s" % test,
                                                "ml_e%s_d%s_output" % (eigen_method, dry))

            sol = solution.Solution(1, path=sol_path, read_aux=True)
            if dry:
                eta = [0.0, -6.0]
            else:
                eta = [0.0, -4.0] 

            print "%s, %s =" % (test, dry)
            print "       ",sig_fig_round(compute_error(sol.q, sol.aux, eta, rho, norm=1),figs=3)
            print "       ",sig_fig_round(compute_error(sol.q, sol.aux, eta, rho, norm=numpy.inf),figs=3)