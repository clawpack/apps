
.. _apps_tsunami_chile2010_fgmax:

Chile 2010 test case for fgmax routines  
=======================================

Illustrates how to set up a grid of points to monitor the maximum amplitude of
the wave at each point in the domain and the arrival times.
This uses the "fgmax" (fixed grid maxima monitoring)
capabilities described in http://www.clawpack.org/fgmax.html.


To test::

    python make_fgmax.py   # to create fgmax_grid.txt
    make .output
    python plot_fgmax.py   # to plot fgmax results
    make plots

Or simply::

    make all

This should produce 
`_plots/amplitude_times.png <./_plots/amplitude_times.png>`_, 
a color map of maximum amplitudes along with contours of arrival
time.  A link to this plot should show up in `_plots/_PlotIndex.html`
along with the usual time frame plots.

*Note:*

- See http://www.clawpack.org/fgmax.html for more information about
  specifying fgmax parameters.

- The file `make_fgmax.py` is used to create the input file for 
  `fgmax_grid.txt` that is needed as input for the Fortran code.
  The following lines in `setrun.py` specify this::

        # == fgmax.data values ==
        fgmax_files = rundata.fgmax_data.fgmax_files
        # for fixed grids append to this list names of any fgmax input files
        fgmax_files.append('fgmax_grid.txt')
        rundata.fgmax_data.num_fgmax_val = 1  # Save depth only

  The last line above indicates that we only want to keep track of maximum
  depth (and elevation), not speed, momentum flux, etc.

- The time `tstart_max` in this file is set to 10 seconds so that the
  topography in the source region has been finalized following the
  earthquake before we start monitoring the maxima.  (Since the topo on the
  fixed grid must also be stored for later postprocessing.)

- The refinement parameters and regions are set so that the maximum
  amplitude we wish to capture always appears on a level 3 grid and
  `min_level_check = 3` is set in `make_fgmax.py`.  Other choices of these
  parameters may give misleading or bizarre results.  The fgmax capabilities
  were designed with the assumption that the region of interest will always
  be refined to the maximum level allowed.

- The file `plot_fgmax.py` is used to plot the fgmax results. Also the file
  `setplot.py` includes the lines::

       otherfigure = plotdata.new_otherfigure(name='max amplitude and arrival times', 
                    fname='amplitude_times.png')


  This results in the link found on `_plots/_PlotIndex.html`.

Version history:  
----------------

- Updated for Clawpack 5.3.0 on 15 Sept 2015

