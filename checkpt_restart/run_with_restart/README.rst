
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
- `_output/gauge*.txt` should contain the gauge output for the full time
            
Note that the `_output/gauge*.txt` might contain some repeated times 
since the restart will append to the end, starting at the restart time.
There might also be some missing times from gauge data buffered but not yet
written to `gauge*.txt` when the run was aborted.

Similary in 3d.


Version history:
----------------

- This version works with Clawpack 5.3.1

- This version works with Clawpack 5.4.1 and Python2 or Python3
