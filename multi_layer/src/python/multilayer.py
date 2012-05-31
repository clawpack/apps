# encoding: utf-8

import os
import sys
import types
import glob

import numpy as np

import wind
import clawutil.runclaw as runclaw

# =========================================
# = Function called before each time step =
# =========================================