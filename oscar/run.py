# oscar/run.py
from ._workflows import standard_run, configured_runs, customized_runs, advanced_runs

def run(mode="default", **kwargs):
    """
    Main entry point for OSCAR simulations.

    Modes:
      - standard:   Instant run (2014-2100) using bootstrap starter-kit.
      - configured: Scientific runs using official library (CMIP6/7 + SSPs).
      - customized: Runs using user-provided external forcing data.
      - advanced:   Sub-module execution and advanced model development.
    """
    if mode == "standard":
        return standard_run.run_standard(**kwargs)

    if mode == "configured":
        # Uses your pre-verified 'menu' of scenarios/regions/ensembles
        return configured_runs.run_configured(**kwargs)

    if mode == "customized":
        # Passes EVERYTHING to the flexible workflow
        return customized_runs.run_customized(**kwargs)

    if mode == "advanced":
        # Direct access to sub-modules for development
        return advanced_runs.run_advanced(**kwargs)
        
    raise ValueError(f"Unknown mode: {mode}")