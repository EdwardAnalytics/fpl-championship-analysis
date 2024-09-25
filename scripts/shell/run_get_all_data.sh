#!/bin/bash

# Set PYTHONPATH and run the Python script
export PYTHONPATH=$(pwd)
python scripts/python/get_championship_data.py
python scripts/python/get_fpl_data.py