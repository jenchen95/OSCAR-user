# OSCAR-user 🌍

A user-friendly, reduced-complexity Earth system model (ESM) for climate research.
This package provides a streamlined interface for running historical reconstructions and future projections across multiple scientific scenarios and regions.

---

## 🚀 Installation

OSCAR can be installed via `pip` or `uv`. We recommend **uv** for a faster and cleaner environment setup.

### Option 1: Using uv (Recommended)
*Requires [uv](https://astral.sh/uv).*
```bash
# Create a virtual environment and install OSCAR
uv venv
uv pip install git+https://github.com/bq-zhu/OSCAR-user.git

# Run the verification model
uv run oscar run
```

### Option 2: Using standard pip
```bash
# Install directly from GitHub
pip install git+https://github.com/bq-zhu/OSCAR-user.git

# Run the verification model
oscar run
```

---

## 🔍 Discovery & Help

OSCAR is self-documenting. You can explore available scientific configurations, regional aggregations, and variable lists directly from your terminal or Python session.

| To see this info... | Terminal Command | Python Command | Status |
| :--- | :--- | :--- | :--- |
| **General Overview** | `oscar` | `oscar.info()` | Available |
| **Standard Mode Specs** | `oscar info standard` | `oscar.info('standard')` | Available |
| **Official Scenario Library** | `oscar info configured` | `oscar.info('configured')` | Available |
| **Customized / Advanced** | — | — | *In Development* |

---

## 📊 Run Modes

OSCAR provides four tiers of interaction. Control the model via the **Terminal** (standard workflows) or **Python** (custom research).

| Mode | Purpose | Terminal Command | Python Command | Availability |
| :--- | :--- | :--- | :--- | :--- |
| **Standard** | Instant verification | `oscar run` | `oscar.run()` | **Now** |
| **Configured**| Official library runs | `oscar run -m configured` | `oscar.run(mode='configured')`| **Now** |
| **Customized**| User research | *(Not available)* | `oscar.run(mode='customized')`| *In Dev* |
| **Advanced** | Model development | *(Not available)* | `oscar.run(mode='advanced')` | *In Dev* |

> **Note:** Scientific modes (Configured and above) require access to a large data library. The model will automatically guide you through a one-time directory initialization upon your first request.

---

## 🛠 Usage Examples

### Terminal (Standard Mode)
Run the 2014-2100 verification simulation with a single command:
```bash
oscar run
```

### Python (Configured Mode)
Run a specific CMIP6 regional projection for multiple SSP scenarios:
```python
import oscar

# Run official scenarios for the 5 RCP regions
oscar.run(
    mode="configured", 
    scenario=["SSP1-2.6", "SSP5-8.5"], 
    region="RCP_5reg"
)
```

---

## 🗑 Uninstallation

To remove OSCAR and its associated files:

| Target | Command / Action |
| :--- | :--- |
| **Package (uv)** | Delete the `.venv` folder and the project directory. |
| **Package (pip)** | Run `pip uninstall oscar`. |
| **Data Library** | Manually delete the data folder you initialized during setup. |

---

## 📝 Citation & Contact

**OSCAR-user** is created by **Biqing Zhu**, motivated by the need to modernize the OSCAR model (based on v3.3) and provide the community with a more accessible, stable, and user-friendly interface.

- **Author & Contact:** Biqing Zhu ([zhub@iiasa.ac.at](mailto:zhub@iiasa.ac.at))
- **Scientific Core:** Based on OSCAR v3.3.
- **Citation:** If you use this package in your research, please cite the original model and this repository: *[https://doi.org/doi:10.5194/gmd-10-271-2017]*

---
*Developed by Biqing (2026) to promote reproducible and accessible climate modeling.*