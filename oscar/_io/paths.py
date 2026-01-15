"""
This is a placeholder for path handling functions for the OSCAR model.
"""

# placeholder, to be updated with actual logic
import os
from pathlib import Path

# The absolute path to the OSCAR package root
PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent

# DEFAULT LOCATIONS -> path to be updated with data moving around #TODO
DEFAULT_INPUT_DIR = PACKAGE_ROOT / "data"
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_DIR / "results"

def get_out_dir(user_provided=None):
    """Logic: User Arg > Environment Variable > Default"""
    if user_provided:
        return Path(user_provided)
    
    # Allows a Level-2 user to set a path once in their terminal
    env_path = os.getenv("OSCAR_OUTPUT")
    if env_path:
        return Path(env_path)
        
    return DEFAULT_RESULT_DIR