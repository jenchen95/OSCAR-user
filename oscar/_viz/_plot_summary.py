"""
OSCAR Visualization Module
Time-series plotting for global variables.
"""
import matplotlib.pyplot as plt
import xarray as xr

def plot_timeseries_summary(ds, split_year, var_list, out_dir, show_plot=True):
    """
    Plots historical vs scenario time-series with professional scientific titles.
    Format: Long Name | Sci Name | Var Name [Unit]
    """
    for var in var_list:
        if var not in ds:
            continue
        
        plt.figure(figsize=(9, 6))
        
        # 1. Select the variable DataArray and squeeze extra dims (like region)
        # Squeezing here ensures we have a clean (year, config, [scen]) object
        da = ds[var].squeeze()
        
        # 2. Split Timeline
        h = da.sel(year=slice(None, split_year))
        s = da.sel(year=slice(split_year + 1, None))

        # 3. Plot Historical (Black line + ribbon)
        # pick the first scenario if 'scen' exists to avoid multiple black lines
        h_plot = h.isel(scen=0) if 'scen' in h.dims else h
        
        if 'config' in h_plot.dims:
            mh, sh = h_plot.mean('config'), h_plot.std('config')
            plt.plot(h_plot.year, mh, color='k', lw=2, label='Historical')
            plt.fill_between(h_plot.year, mh - sh, mh + sh, color='k', alpha=0.2)
        else:
            plt.plot(h_plot.year, h_plot, color='k', lw=2, label='Historical')

        # 4. Plot Scenario (Colored lines per scenario)
        scens = s.scen.values if 'scen' in s.dims else [None]
        for sn in scens:
            s_sub = s.sel(scen=sn) if sn is not None else s
            label = str(sn) if sn is not None else "Projection"
            
            if 'config' in s_sub.dims:
                ms, ss = s_sub.mean('config'), s_sub.std('config')
                line, = plt.plot(s.year, ms, lw=1.5, label=label)
                plt.fill_between(s.year, ms - ss, ms + ss, 
                                 color=line.get_color(), alpha=0.2)
            else:
                plt.plot(s.year, s_sub, lw=1.5, label=label)

        # --- 5. Professional Scientific Title Logic ---
        long_name = da.attrs.get('long_name', var)
        sci_name  = da.attrs.get('sci_name', '')
        units     = da.attrs.get('units', 'n/a')
        
        # Build a descriptive title: "Long Name (Symbol: ΔTg | ID: D_Tg)"
        title_str = f"{long_name}"
        if sci_name:
            title_str += f" ({sci_name} | ID: {var})"
        else:
            title_str += f" (ID: {var})"
        
        plt.title(title_str, fontsize=12, fontweight='normal', pad=10)
        plt.ylabel(f"[{units}]", fontsize=11)
        plt.xlabel("Year", fontsize=11)
        plt.legend(loc='upper left', fontsize='small', ncol=2 if len(scens) > 1 else 1)
        plt.grid(True, alpha=0.3)

        # 6. Save and Close
        plot_file = out_dir / f"plt_{var}.png"
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"Plot saved: {plot_file}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()