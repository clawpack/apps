
# Makefile to create make rendered html versions of Jupyter notebooks.
# This is a stripped down version of $CLAW/clawutil/src/Makefile.common
#
# Usage:
#
# In a directory containing notebook(s):
#   make notebook_htmls -f $CLAW/apps/notebooks/Makefile
#
# If the directory contains it's own Makefile based on Makefile.common,
# this should give the same result as doing
#   make notebook_htmls
#
# If there is a README.rst file in the directory, perhaps with links to
# one or more notebooks, you might also want to do:
#   make readme
# to create README.html with links to the rendered html version of notebooks.
#

CLAW_PYTHON ?= python

NBCONVERT = jupyter nbconvert --to html --execute --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=1200 

%.ipynb.html: %.ipynb ; $(NBCONVERT) $<
%.html: %.ipynb ; $(NBCONVERT) $<

NOTEBOOK_HTML = \
  $(subst .ipynb,.ipynb.html,$(wildcard *.ipynb)) \

# make .html files from .ipynb notebooks using nbconvert: 
notebook_htmls: $(NOTEBOOK_HTML);

# to create README.html from README.rst:
readme: 
	@echo Converting README.rst...
	$(CLAW_PYTHON) $(CLAW)/clawutil/src/python/clawutil/convert_readme.py

