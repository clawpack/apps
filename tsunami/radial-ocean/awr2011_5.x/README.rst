
.. _apps_tsunami_radial-ocean_awr2011_5.x:

Radial ocean test case from AWR 2011 paper
==========================================


These codes were developed to accompany the paper:


The GeoClaw software for depth-averaged flows with adaptive refinement, 
by M.J. Berger, D.L. George, R.J. LeVeque, and K.M.  Mandli.  
Advances in Water Resources 34 (2011), pp. 1195-1206.
`link <http://www.amath.washington/edu/~rjl/pubs/awr10>`_

Radially symmetric ocean on a lat-long grid, so it doesn't look circular in the
computational coordinates.

The profile of the ocean is set in function topo of `maketopo.py`.
You must first set the desired value `theta_island` in `setrun.py` and do::

    make data
    make topo
    make output

To run both test problems from the paper and produce some plots::

    source make_all.sh


