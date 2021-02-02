#!/bin/bash

# Perform beamline-specific actions before the test.

# Work-around the issue with reading .xlsx files with xlrd v2+.
conda install -y "xlrd<2"
