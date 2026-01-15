"""
This is a placeholder for default workflow functions for running the OSCAR model.
It is the default script called by oscar.run_default().
"""
## these are placeholders, to be updated with actual logic
from .._core.mod_process import OSCAR
from .._io.paths import get_bootstrap_path

def run_default():
    """Exact reproduction of the standard historical + SSP2 case."""
    # Uses bootstrap/pre-initialized data for speed
    ini = get_bootstrap_path("init_2014.nc")
    par = get_bootstrap_path("par_standard_200.nc")
    # ... logic to run ...
    return results