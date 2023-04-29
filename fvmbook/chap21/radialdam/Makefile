
# Makefile for Clawpack code in this directory.
# This version only sets the local files and frequently changed
# options, and then includes the standard makefile pointed to by CLAWMAKE.
CLAWMAKE = $(CLAW)/clawutil/src/Makefile.common

# See the above file for details and a list of make options, or type
#   make .help
# at the unix prompt.


# Adjust these variables if desired:
# ----------------------------------

CLAW_PKG = classic                  # Clawpack package to use
EXE = xclaw                         # Executable to create
SETRUN_FILE = setrun.py             # File containing function to make data
OUTDIR = _output                    # Directory for output
SETPLOT_FILE = setplot.py           # File containing function to set plots
PLOTDIR = _plots                    # Directory for plots

OVERWRITE ?= True                   # False ==> make a copy of OUTDIR first
RESTART ?= False                    # Should = clawdata.restart in setrun

# Environment variable FC should be set to fortran compiler, e.g. gfortran

# Compiler flags can be specified here or set as an environment variable
FFLAGS ?=  

# ---------------------------------
# List of sources for this program:
# ---------------------------------

LIB = $(CLAW)/classic/src/2d

MODULES = \

SOURCES = \
  qinit.f \
  setprob.f \
  fdisc.f \
  $(CLAW)/riemann/src/rpn2_shallow_roe_with_efix.f90 \
  $(CLAW)/riemann/src/rpt2_shallow_roe_with_efix.f90 \
  $(CLAW)/classic/src/2d/cellave.f \
  $(CLAW)/classic/src/2d/setaux.f90 \
  $(CLAW)/classic/src/2d/driver.f90 \
  $(CLAW)/classic/src/2d/claw2ez.f \
  $(CLAW)/classic/src/2d/claw2.f \
  $(CLAW)/classic/src/2d/bc2.f \
  $(CLAW)/classic/src/2d/b4step2.f90 \
  $(CLAW)/classic/src/2d/step2.f90 \
  $(CLAW)/classic/src/2d/step2ds.f90 \
  $(CLAW)/classic/src/2d/dimsp2.f \
  $(CLAW)/classic/src/2d/flux2.f90 \
  $(CLAW)/classic/src/2d/copyq2.f \
  $(CLAW)/classic/src/2d/inlinelimiter.f90 \
  $(CLAW)/classic/src/2d/src2.f90 \
  $(CLAW)/classic/src/2d/out2.f \
  $(CLAW)/classic/src/2d/restart2.f \
  $(CLAW)/classic/src/2d/opendatafile.f

#-------------------------------------------------------------------
# Include Makefile containing standard definitions and make options:
include $(CLAWMAKE)

