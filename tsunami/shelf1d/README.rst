
.. _apps_tsunami_shelf1d:

Tsunami interacting with 1d continental shelf
=============================================

This one dimensional test problem consists of a flat ocean floor, linear
continental slope, flat continental shelf, and a solid wall reflecting
boundary.

It is designed to illustrate how a tsunami wave is modified as it moves from
the deep ocean onto the continental shelf, and the manner in which some of
the energy can be trapped on the shelf and bounce back and forth.

Try the following bathymetry by changing lines in the file `setrun.py`
and the rerunning the code and plotting the results via::

   make .plots

Original: a step discontinuity between deep ocean and shallow shelf::

    Bocean = -4000.
    Bshelf = -200.
    width = 1.
    start = -30.e3

With a shallower shelf, note that the wave moves slower but is more amplified::

    Bocean = -4000.
    Bshelf = -50.
    width = 1.
    start = -30.e3

With a wide continental shelf rather than a discontinuity, 
note that there is less energy trapped on the shelf::

    Bocean = -4000.
    Bshelf = -200.
    width = 100.e3
    start = -130.e3

The IPython notebook `Shelf_1d.ipynb` illustrates these cases.

Version
-------

- This code runs with Clawpack 5.2.2.
- Added December, 2014
- Tools used in the notebook `Shelf_1d.ipynb` are still under development.

