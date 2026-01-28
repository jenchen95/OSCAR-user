"""
OSCAR - Bootstrap Generator
Internal utility to freeze the 'standard' run state.
"""
import xarray as xr

from .._io.paths import get_bootstrap_dir, get_in_dir
from .._core.fct_genMC import generate_config
from .._core.mod_process import OSCAR
from .load_config import load_config

def generate_bootstrap():
    # Load the "Source of Truth" from YAML
    full_cfg = load_config()
    cfg = full_cfg['bootstrap_specs']  # Match the heading in your YAML
    
    b_dir = get_bootstrap_dir()
    b_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. LOAD PARAMETERS using config values
    from .._core.fct_loadP import load_all_param
    # Loading parameters
    Par0 = load_all_param(mod_region=cfg['region'])
    # Generate Monte Carlo parameters
    Par = generate_config(Par0, nMC=cfg['nMC'])

    # 2. COMPILE For_hist
    from .get_SSP_drivers import For_hist
    print(f"Compiling historical forcings up to {cfg['hist_end_year']}...")
    # move parameters from For to Par
    Par = xr.merge([Par, For_hist.drop_vars([VAR for VAR in For_hist if 'year' in For_hist[VAR].dims])])
    # remove variables without 'year' dimension from For_hist
    For_hist = For_hist.drop_vars([VAR for VAR in For_hist if 'year' not in For_hist[VAR].dims])
    For_hist = For_hist.sel(year=slice(cfg['hist_start_year'], cfg['hist_end_year'])).fillna(0.)
    
    # 3. SAVE PARAMETERS & HISTORICAL FORCINGS
    Par.to_netcdf(b_dir / "parameters_mc_standard.nc")
    print("Par saved.")
    For_hist.to_netcdf(b_dir / "forcing_hist_standard.nc")
    print("For_hist saved.")

    # 4. Prepare & SAVE SCENARIO FORCINGS
    from .get_SSP_drivers import For_scen
    For_scen = For_scen.sel(year=slice(cfg['scen_start_year'], cfg['scen_end_year']))
    For_scen.to_netcdf(b_dir / "forcing_scen_standard.nc")
    print("For_scen saved.")

    # 5. RUN HISTORICAL & FREEZE STATE    
    print(f"Running historical simulation ({cfg['hist_start_year']} to {cfg['hist_end_year']})...")
    Out_hist = OSCAR(Ini=None, Par=Par, For=For_hist)
    # save Out_hist with a subset of variables to reduce size
    Out_hist_select = Out_hist[cfg['var_select']]
    Out_hist_select.to_netcdf(b_dir / "output_hist_standard.nc")
    print("Out_hist saved.")
    # save last year state as initial condition for future runs
    Ini = Out_hist.isel(year=-1, drop=True)
    Ini.to_netcdf(b_dir / "scen_initial_state_standard.nc")

    print(f"Bootstrap generation complete in {b_dir}")

if __name__ == "__main__":
    # This block only runs if the file is executed directly
    print("Initializing bootstrap generation...")
    generate_bootstrap()