
# Makefile to create make rendered html versions of Jupyter notebooks.
# This is a stripped down version of $CLAW/clawutil/src/Makefile.common
#
# If there is a README.rst file in the directory, perhaps with links to
# one or more notebooks, this will also be converted to README.html.
# 
# Usage:
#
# In a directory containing notebook(s):
#   make notebook_htmls -f $CLAW/apps/notebooks/Makefile
#

CLAW_PYTHON ?= $(PYTHON)

NBCONVERT = jupyter nbconvert --to html --execute --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=1200 

%.ipynb.html: %.ipynb ; $(NBCONVERT) $<

NOTEBOOK_HTML = \
  $(subst .ipynb,.ipynb.html,$(wildcard *.ipynb)) \

# to create README.html:
readme: 
	@echo Converting README.rst...
	$(CLAW_PYTHON) $(CLAW)/clawutil/src/python/clawutil/convert_readme.py

.htmls: $(HTML) readme;

# make .html files from .ipynb notebooks using nbconvert, 
# and also remake README.html in case it links these in:
notebook_htmls: $(NOTEBOOK_HTML) readme;

