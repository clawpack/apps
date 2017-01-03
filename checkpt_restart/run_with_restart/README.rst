
_apps_checkpt_restart_run_with_restart:

Run with restart
================

This directory contains a script `run_with_restart.py` and examples
illustrating how to use it.  This script runs the code only if it appears
that it has not been run before or the previous run did not complete
properly.  

Originally designed for use in a crontab job to automatically restart a run
if the computer died during the previous run, but not yet extensively tested
in that context.

Requires modifications to `amrclaw` checkpoint and restart routines
introduced in Version 5.3.1 that allow alternating between two checkpoint
files rather than creating a new file name for each checkpoint (intended for
frequent checkpointing of large runs). 

See docstring in `run_with_restart.py` for more details.

To test 2d version... ::

    cd test_advection_2d_square
    make .exe
    python ../run_with_restart.py
    Ctrl-C
    python ../run_with_restart.py
    [repeat this process as many times as desired until it finishes]

Then check the following:

- `run_output.txt`  contains stdout output from each run and info about restarts
- `_output/fort.gauge`  has final set of gauge data from last execution
- `_output/fort.gauge_DATETIME`  files contain fort.gauge from earlier
            
All `fort.gauge*` files need to be catenated together, but there may be some
overlapping times (after last checkpoint and before code died).

Similary in 3d.


Version history:
----------------

- This version works with Clawpack 5.3.1

