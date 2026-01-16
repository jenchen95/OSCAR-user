"""
OSCAR Path Management Utility

This module centralizes all directory and file-path logic for the OSCAR model.
Location: oscar/_io/paths.py

Main Logic:
    1. PACKAGE_ROOT: Identifies the top-level project folder (OSCAR/).
    2. Inputs: Stable link to 'input_data' (drivers, observations).
    3. Outputs: Manages results with automatic folder creation.

Usage:
    # 1. In data loading functions:
    from .paths import get_in_dir
    input_data_path = get_in_dir()


    # 2. In the main run API:
    from ._io.paths import get_out_dir
    output_data_path = get_out_dir()
"""

# Imports
import os
from pathlib import Path

# The absolute path to the OSCAR package root
PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent

# DEFAULT LOCATIONS
DEFAULT_BOOTSTRAP_DIR = PACKAGE_ROOT / "oscar" / "_resources"/"bootstrap"
DEFAULT_INPUT_DIR = PACKAGE_ROOT / "data" / "input_data"
DEFAULT_OUTPUT_DIR = PACKAGE_ROOT / "data" / "results"

def get_out_dir(user_provided=None):
    """
    Logic: User Arg > Environment Variable > Default
    Ensures the directory exists before returning it.
    """
    if user_provided:
        path = Path(user_provided)
    else:
        path = DEFAULT_OUTPUT_DIR

    # 3. CRITICAL: Expand ~ (user home) and make absolute
    path = path.expanduser().resolve()
    
    # 4. Auto-create the folder so the model doesn't crash on the first run
    path.mkdir(parents=True, exist_ok=True)
    
    return path

def get_in_dir(user_provided=None): #TODO: to be updated distinguishing raw and compiled input
    """
    Returns the Path object for input data.
    Useful for fct_loadD.py to know where to look.
    """
    path = Path(user_provided) if user_provided else DEFAULT_INPUT_DIR
    return path.expanduser().resolve()

def get_bootstrap_dir():
    """Returns the Path to the pre-initialized/compiled bootstrap data."""
    path = DEFAULT_BOOTSTRAP_DIR
    return path.expanduser().resolve()