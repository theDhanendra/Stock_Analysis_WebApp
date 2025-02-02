#!/bin/sh
sed -i 's/from numpy import NaN as npNaN/import numpy as np\nnpNaN = np.nan/' /home/adminuser/venv/lib/python3.12/site-packages/pandas_ta/momentum/squeeze_pro.py
