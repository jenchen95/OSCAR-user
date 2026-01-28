"""
OSCAR Driver Utility: get_drivers.py
Centralized functions for aggregating raw datasets into regional model drivers.
"""
import numpy as np
import xarray as xr
from .._core.fct_misc import aggreg_region, load_data
from .._core.fct_loadD import (
    load_landuse_hist, load_RFdrivers_hist, 
    load_landuse_scen, load_RFdrivers_scen
)
from .._core.fct_loadP import load_all_param

def compile_ar6_hist_drivers(mod_region):
    """
    Aggregates historical data (CEDS, LUH2, CMIP6) for the AR6 period.
    Timeline: 1750-2014.
    """
    Par0 = load_all_param(mod_region)

    # 1. load emissions
    for_h = aggreg_region(load_data('emissions_CEDS'), mod_region).sum('sector')
    for_h = for_h.rename({'E_CO2': 'Eff'})

    # 2. load LULCC
    lu_h = load_landuse_hist(mod_region, ['LUH2'], LCC='gross').sel(data_LULCC='LUH2', drop=True)
    for_h = xr.merge([for_h, lu_h])

    # 3. load RF drivers
    rf_h = load_RFdrivers_hist().sel(data_RF_contr='ICAO', data_RF_solar='CMIP6', data_RF_volc='CMIP6', drop=True)
    for_h = xr.merge([for_h, rf_h])
    for_h['RF_contr'] *= 0

    # 4. load atmospheric concentrations
    conc_h = load_data('concentrations_CMIP6').sel(region='Globe', drop=True)
    for VAR in ['CO2', 'CH4', 'N2O', 'Xhalo']:
        for_h['D_'+VAR] = conc_h[VAR] - Par0[VAR+'_0']

    # 5. missing drivers
    for_h['Eluc'] = 0 * for_h['Eff']
    for_h['E_N2O'] = 0 * for_h['Eff']
    for_h['E_Xhalo'] = 0 * for_h['D_Xhalo']
    
    return for_h.fillna(0.)

def compile_ssp_scen_drivers(mod_region, for_h):
    """
    Aggregates scenario data (ScenarioMIP) and applies SSP extensions.
    Timeline: 2015-2300.
    """
    Par0 = load_all_param(mod_region)

    # 1. load emissions
    for_s = aggreg_region(load_data('emissions_ScenarioMIP'), mod_region, old_axis='region', dataset='ScenarioMIP')
    for_s = xr.concat([for_s, for_s.sel(year=2100).assign_coords(year=2300)], dim='year')

    # 2. correction: non-CO2 emissions from FF&I decrease to 0, while those from LUC stay constant
    sectors_LU = ['Forest Burning', 'Grassland Burning', 'Peat Burning', 'Agricultural Waste Burning', 'Agriculture']
    for var in for_s.variables:
        if (var not in for_s.coords) and (var not in ['E_N2O', 'Eluc']):
            non_lu = [sec for sec in for_s.sector.values if sec not in sectors_LU]
            for_s[var].loc[{'sector': non_lu, 'year': 2300}] = 0.
    
    for_s = for_s.interp(year=np.arange(2015, 2300+1)).sum('sector')

    # 3. SSP Extension Ramps
    ## specific treatment for Eff. Does not follow O'Neill et al, 2016, but updates of extensions from the poster of Meinshausen 2019 (ScenarioForum).
    dico_dates_end_plateau = {'SSP1-1.9':2140, 'SSP1-2.6':2140, 'SSP2-4.5':2100, 'SSP3-7.0':2100, 'SSP3-7.0-LowNTCF':2100, 'SSP4-3.4':2140, 'SSP4-6.0':2100, 'SSP5-3.4-OS':2140, 'SSP5-8.5':2100}
    dico_dates_end_ramp = { 'SSP1-1.9':2190, 'SSP1-2.6':2190, 'SSP2-4.5':2250, 'SSP3-7.0':2250, 'SSP3-7.0-LowNTCF':2250, 'SSP4-3.4':2190, 'SSP4-6.0':2250, 'SSP5-3.4-OS':2170, 'SSP5-8.5':2250 }
    for scen in for_s.scen.values:
        for_s['Eff'].loc[dict(scen=scen,year=range(2100,dico_dates_end_plateau[scen]+1))] = for_s['Eff'].sel(scen=scen,year=2100) # constant over 2100-2140
        for_s['Eff'].loc[dict(scen=scen,year=np.arange(dico_dates_end_plateau[scen],dico_dates_end_ramp[scen]+1))] = np.linspace( for_s['Eff'].sel(scen=scen,year=2100) , 0.*for_s['Eff'].sel(scen=scen,year=2100) , dico_dates_end_ramp[scen]-dico_dates_end_plateau[scen]+1)  # linear ramp over 2140-2190
        for_s['Eff'].loc[dict(scen=scen,year=np.arange(dico_dates_end_ramp[scen]+1,2300+1))] = 0. # 0 afterwards

    ## specific treatment for Eluc. Does not follow O'Neill et al, 2016, but updates of extensions from the poster of Meinshausen 2019 (ScenarioForum).
    for_s['Eluc'].loc[dict(year=np.arange(2100,2150+1))] = np.linspace( for_s['Eluc'].sel(year=2100) , 0.*for_s['Eluc'].sel(year=2100) , 2150-2100+1)  # linear ramp over 2100-2150
    for_s['Eluc'].loc[dict(year=np.arange(2150+1,2300+1))] = 0. # 0 afterwards

    # 4. load LULCC
    lu_s = load_landuse_scen(mod_region, ['LUH2'], LCC='gross').rename({'scen_LULCC': 'scen'})
    lu_s.coords['scen'] = [s + '-OS' * (s == 'SSP5-3.4') for s in lu_s['scen'].values]
    lu_s = lu_s.where(lu_s.year < 2100).dropna('year')
    lu_s = xr.concat([lu_s, lu_s.sel(year=2099).assign_coords(year=2300)], dim='year').interp(year=np.arange(850, 2300+1))
    lu_s['d_Acover'] = lu_s['d_Acover'].where(lu_s.year <= 2099, 0)
    for_s = xr.merge([for_s, lu_s])

    # 5. load RF drivers
    TMP = load_RFdrivers_scen().sel(scen_RF_contr='CMIP5', scen_RF_solar='CMIP6', scen_RF_volc='CMIP6', drop=True)
    for VAR in TMP:
        years = (for_h[VAR].dropna('year').year + TMP[VAR].dropna('year').year).year
        for_s[VAR] = for_h[VAR].sel(year=years).mean('year') / TMP[VAR].sel(year=years).mean('year') * TMP[VAR]

    # 6. load atmospheric concentrations
    conc_s = load_data('concentrations_ScenarioMIP').drop('Xhalo_eq')
    for VAR in ['CO2', 'CH4', 'N2O', 'Xhalo']:
        for_s['D_'+VAR] = conc_s[VAR] - Par0[VAR+'_0']
    for_s['E_Xhalo'] = 0 * for_s['D_Xhalo']

    return for_s.fillna(0.)