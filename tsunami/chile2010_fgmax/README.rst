
.. _apps_tsunami_chile2010_fgmax:

Test case for fgmax routines  
=============================

Illustrates how to set up a grid of points to monitor maximum amplitude of
wave, and also a 1-dimensional transect.  

To test::

    python make_fgmax.py   # to create fgmax_grid.txt and fgmax_transect.txt
    make .output
    python plot_fgmax_grid.py
    python plot_fgmax_transect.py
    make plots

Or simply::

    make all


This should produce the following files in `./_plots`:

 - `zeta.png`             maximum amplitude along with contours of arrival times
 - `arrival_times.png`    color map of arrival times
 - `zetatimes.png`        color map of time of maximum amplitude

 - `zeta_transect.png`           1d plot of solution on a transect (from FG2)
 - `arrival_times_transect.png`  arrival times along transect

These should also show up in `_plots/_PlotIndex.html`

