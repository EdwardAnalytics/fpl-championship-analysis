#!/bin/bash

# Set PYTHONPATH and run the Python script
export PYTHONPATH=$(pwd)
python scripts/python/analysis_welchs_ttest.py
python scripts/python/analysis_championship_performance.py