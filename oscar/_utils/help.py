"""
OSCAR Help Utility
Location: oscar/_utils/help.py

Provides contextual information about run modes, official scientific 
scenarios, and regional configurations.
"""
from .load_config import load_config
from .metadata import load_var_registry  # Import your metadata loader

def show_info(mode=None):
    """Router for the OSCAR information system."""
    full_cfg = load_config()
    
    # Normalize mode string
    m = str(mode).lower() if mode else None

    if m is None or m == 'none':
        _print_general()
    elif m == 'standard':
        _print_standard(full_cfg['bootstrap_specs'])
    elif m == 'configured':
        _print_configured(full_cfg['configured_options'])
    elif m == 'customized':
        _print_customized()
    elif m == 'advanced':
        _print_advanced()
    else:
        print(f"\n[!] Unknown mode: '{mode}'")
        print("Available modes are: 'standard', 'configured', 'customized', 'advanced'")

def _print_general():
    width = 90
    print("\n" + "="*width)
    print(f"{'OSCAR MODEL - GENERAL OVERVIEW':^90}")
    print("="*width)
    print("A reduced-complexity Earth system model for climate research.")
    
    print("\nAvailable Run Modes:")
    # Aligned descriptions pointing to Terminal commands
    print(f"  {'standard':<12} : Fast verification (no setup). → Command: oscar run")
    print(f"  {'configured':<12} : Official CMIP runs.           → Info:    oscar info configured")
    print(f"  {'customized':<12} : [DEV] User-defined research.   (Status: Not available yet)")
    print(f"  {'advanced':<12} : [DEV] Model sub-modules.       (Status: Not available yet)")
    print("="*width + "\n")

def _print_standard(cfg):
    """Displays information for the Standard verification mode."""
    width = 90
    print("\n" + "="*width)
    print(f"{'MODE: STANDARD (Verification)':^90}")
    print("="*width)
    print("Goal:        Fast proof-of-concept run for the model installation.")
    print(f"Data source: Internal package bootstrap ({cfg['nMC']} members).")
    print(f"Timeline:    Pre-industrial (1750) to {cfg['scen_end_year']}.")
    print(f"Scenario:    Historical + 9 marker SSPs.")
    print(f"Region:      Fixed ({cfg['region']}).")
    
    print("\nExample Commands:")
    print("  [Terminal] : oscar run")
    print("  [Python]   : import oscar; oscar.run()")
    
    print("\nNote: This mode is self-contained and requires no additional data setup.")
    print("="*width + "\n")

def _print_configured(cfg):
    """
    Displays the official scientific library options.
    Synchronized with '_list' naming convention in config.yaml.
    """
    width = 95
    print("\n" + "="*width)
    print(f"{'MODE: CONFIGURED (Scientific Library)':^95}")
    print("="*width)
    print("Official scientific experiments using curated forcing and parameter libraries.")
    
    print("\nAvailable Options (Valid for use with mode='configured'):")
    # Using new '_list' keys from YAML
    print(f"  {'Histories':<12} : {', '.join(cfg['hist_list'].keys())}")
    print(f"  {'Regions':<12} : {', '.join(cfg['region_list'])}")
    print(f"  {'Scenarios':<12} : {', '.join(cfg['scen_list'])}")
    
    # Metadata lookup from the registry
    from .metadata import load_var_registry
    reg = load_var_registry()
    print(f"  {'Output Vars':<12} :")
    for var in cfg['var_list']:
        long_name = reg.get(var, {}).get('long_name', 'No description available')
        print(f"{'':<15}- {var:<10}: {long_name}")

    print(f"  {'MC Ensemble':<12} : {cfg['official_nMC']} configurations (Fixed)")

    print("\nExample Commands:")
    print("  [Terminal] : oscar run -m configured -s SSP2-4.5 -s SSP5-8.5 -r RCP_5reg -v D_Tg -v D_CO2")
    print("  [Python]   : oscar.run(mode='configured', scenario=['SSP2-4.5', 'SSP5-8.5'], variables=['D_Tg', 'D_CO2'])")
    
    print("\nNote: Required data will be downloaded automatically upon the first request.")
    print("="*width + "\n")

def _print_customized():
    print("\n" + "-"*60)
    print(" MODE: CUSTOMIZED (User Research) ")
    print("-"*60)
    print("Run OSCAR with your own experimental forcing data.")
    print("\nRequirements:")
    print("  1. Formated inputs.")
    print("  2. Background forcing information.")
    print("-"*60 + "\n")

def _print_advanced():
    print("\n" + "*"*60)
    print(" MODE: ADVANCED (Model Development) ")
    print("*"*60)
    print("Direct control over sub-module execution and parameters.")
    print("\nCommon Use Cases:")
    print("  - Running ONLY the Land Carbon cycle module.")
    print("  - Generating new Monte Carlo constraint sets.")
    print("  - Modifying numerical sub-steps (nt).")
    print("*"*60 + "\n")