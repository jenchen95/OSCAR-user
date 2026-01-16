"""
OSCAR Public API
"""
from ._workflows.default_run import run_default

def run(mode="default", **kwargs):
    """
    The main entry point for OSCAR.
    
    Usage:
        import oscar
        oscar.run()  # This is the one-line execution
    """
    if mode == "default":
        # Simply return the result of your workflow
        print("Running OSCAR in 'default' mode...")
        return run_default(**kwargs)
    
    # Placeholder for future modes
    raise ValueError(f"Unknown mode: {mode}")