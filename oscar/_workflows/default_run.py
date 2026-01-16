"""
OSCAR - Default Workflow
Author: Biqing Zhu
"""
import xarray as xr
import matplotlib.pyplot as plt
from .._core.mod_process import OSCAR
from .._io.paths import get_bootstrap_dir, get_out_dir
from .._utils.load_config import load_config  # Use your helper

def run_default(show_plot=True, run_model=True):
    # 1. Load instructions from YAML
    cfg = load_config()['bootstrap_specs']
    b_dir = get_bootstrap_dir()
    out_dir = get_out_dir() / "default_run"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "oscar_default_results.nc"

    if run_model:
        # 2. Load the "Starter Kit"
        print("Loading forcing data and parameters...")
        Par = xr.open_dataset(b_dir / "parameters_mc_default.nc").load()
        For = xr.open_dataset(b_dir / "forcing_scen_default.nc").load()
        Out_hist = xr.open_dataset(b_dir / "output_hist_default.nc").load()
        Ini = xr.open_dataset(b_dir / "scen_initial_state_default.nc").load()
        
        For = For.sel(year=slice(cfg['scen_start_year'], cfg['scen_end_year']))
        
        # 3. Run the model projection
        print(f"Running OSCAR projection for scenario {cfg['scenario_default']}...")
        Out_scen = OSCAR(Ini=Ini, Par=Par, For=For, nt=4)
        Out_scen_sel = Out_scen[cfg['var_select']]
        
        # 4. Combine
        Out_all = xr.concat([Out_hist, Out_scen_sel], dim='year')

        # 5. Save results
        Out_all.to_netcdf(out_file)
        print(f"Success! Data saved to: {out_file}")
    else:
        # --- PLOT ONLY MODE ---
        print(f"Loading existing results for plotting from: {out_file}")
        if not out_file.exists():
            raise FileNotFoundError(f"No results found at {out_file}. Run with run_model=True first.")
        Out_all = xr.open_dataset(out_file).load()

    # 6. Generate Summary Plot
    # We pass cfg['var_select'] to the plotter
    _plot_summary(Out_all, cfg['hist_end_year'], cfg['var_select'], out_dir=out_dir, show_plot=show_plot)
    
    return Out_all

def _plot_summary(ds, split_year, var_list, out_dir, show_plot=True):
    """Plotting logic for variables with varying dimensions."""
    import matplotlib.pyplot as plt

    for var in var_list:
        if var not in ds: continue
        
        plt.figure(figsize=(8, 5))
        # Split into Historical and Scenario
        h = ds.sel(year=slice(None, split_year))
        s = ds.sel(year=slice(split_year + 1, None))

        # --- Plot Historical ---
        # If 'scen' exists, we pick the first one just for the historical black line
        # since historical is usually the same across scenarios.
        h_var = h[var].isel(scen=0) if 'scen' in h.dims else h[var]
        
        # Calculate mean across config if it exists
        mh = h_var.mean('config') if 'config' in h_var.dims else h_var
        plt.plot(h.year, mh, color='k', lw=2, label='hist')
        
        # Plot uncertainty only if 'config' exists
        if 'config' in h_var.dims:
            sh = h_var.std('config')
            plt.fill_between(h.year, mh - sh, mh + sh, color='k', alpha=0.2)

        # --- Plot Scenario ---
        # We loop through 'scen' to show all 9 scenario lines
        for sn in s.scen.values:
            s_var = s[var].sel(scen=sn)
            ms = s_var.mean('config') if 'config' in s_var.dims else s_var
            
            line, = plt.plot(s.year, ms, lw=1.5, label=sn)
            
            # Fill uncertainty only for the ensemble variable (D_Tg)
            if 'config' in s_var.dims:
                ss = s_var.std('config')
                plt.fill_between(s.year, ms - ss, ms + ss, color=line.get_color(), alpha=0.2)

        # Formatting
        plt.title(f"{var} ({ds.attrs.get('model', 'OSCAR')})")
        plt.ylabel(ds[var].attrs.get('units', 'n/a'))
        plt.legend(loc='upper left', fontsize='x-small', ncol=2)
        plt.grid(True, alpha=0.3)

        # --- Save plot ---
        plot_file = out_dir / f"plt_{var}.png"
        plt.savefig(plot_file)
        print(f"Plot saved: {plot_file}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()