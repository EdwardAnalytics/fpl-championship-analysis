#!/bin/bash

# Set PYTHONPATH and run the Python script
export PYTHONPATH=$(pwd)
python scripts/python/analysis_welchs_ttest.py
python scripts/python/analysis_championship_player_performance.py
python scripts/python/analysis_team_performance.py
python scripts/python/analysis_box_plot.py
python scripts/python/analysis_fwd_corr_matrix.py

