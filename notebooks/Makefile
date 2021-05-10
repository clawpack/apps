
# Makefile to create make rendered html versions of Jupyter notebooks.
# This is a stripped down version of $CLAW/clawutil/src/Makefile.common
#
# Usage:
#
# To convert a notebook nbname.ipynb to nbname.html:
#   make nbname.html -f $CLAW/apps/notebooks/Makefile
#
# In a directory containing several notebooksi, you can convert all via:
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
# To convert a notebook nbname.ipynb to a script nbname.py:
#   make nbname.py -f $CLAW/apps/notebooks/Makefile
#
# Note that any cells with the tag 'hide-py' are ignored when the command
# NBCONVERTPY below is run.  If the notebook starts with a magic command like
#       %matplotlib inline
# then this cell should be tagged 'hide-py' since or the resulting script 
# will not run properly.

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

# to create .py script from .ipynb notebook:

NBCONVERTPY = jupyter nbconvert --to python --TagRemovePreprocessor.enabled=True  --TagRemovePreprocessor.remove_cell_tags="['hide-py']"

%.py: %.ipynb ; $(NBCONVERTPY) $<

