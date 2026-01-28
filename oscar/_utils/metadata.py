"""
OSCAR Metadata Manager
Location: oscar/_utils/metadata.py

This module handles the registration of scientific metadata (units, long names)
onto model objects. It serves as the bridge between raw model output and
international reporting standards (CF-Conventions).
"""

import yaml
from .._io.paths import PACKAGE_ROOT

def load_var_registry():
    """
    Loads the official variable definitions from the resources folder.
    Uses utf-8-sig to safely handle Windows/Network drive encodings.
    """
    path = PACKAGE_ROOT / "oscar" / "_resources" / "variables.yaml"
    
    if not path.exists():
        raise FileNotFoundError(f"Metadata Registry missing: {path}")
        
    with open(path, "r", encoding="utf-8-sig") as f:
        # Load the dictionary under the 'variables' key
        data = yaml.safe_load(f)
        return data.get('variables', {})

def apply_variable_metadata(ds):
    """
    Attaches units, long_names, and sci_names to an xarray.Dataset.
    
    Usage:
        ds = apply_variable_metadata(ds)
        ds.to_netcdf("output.nc")
    """
    registry = load_var_registry()
    
    # Iterate through every data variable in the xarray Dataset
    for var in ds.data_vars:
        if var in registry:
            meta = registry[var]
            
            # Map YAML keys to NetCDF/Xarray attributes
            # .get() ensures we don't crash if a specific field is missing
            updates = {
                'units': meta.get('unit', 'n/a'),
                'long_name': meta.get('long_name', var),
                'sci_name': meta.get('sci_name', var)
            }
            
            # Apply the attributes to the variable
            ds[var].attrs.update(updates)
            
    return ds

# --- Future-Proofing placeholders ---

def apply_parameter_metadata(par_ds):
    """
    (Placeholder) To be implemented in later versions for 
    labeling Monte Carlo parameter sets.
    """
    pass