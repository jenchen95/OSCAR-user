# OSCAR-user

A brief one-sentence description of what OSCAR does goes here.

## 🚀 Quick Start

Choose your preferred installation method. **uv** is recommended for the fastest experience.

### Option 1: Using uv (Fastest & Cleanest)
Best for users who want an isolated environment without the overhead of Conda.
```bash
# Install
uv venv && uv pip install git+https://github.com/bq-zhu/OSCAR-user.git

# Run
uv run python -c "import oscar; oscar.run()"
```

### Option 2: Using Conda
Best if you are already working inside a Conda environment.
```bash
# Install (Faster than pip)
uv pip install git+https://github.com/bq-zhu/OSCAR-user.git

# Run
python -c "import oscar; oscar.run()"
```

### Option 3: Using pip
The standard method, no additional tools required.
```bash
# Install
pip install git+https://github.com/bq-zhu/OSCAR-user.git

# Run
python -c "import oscar; oscar.run()"
```

---

## 🛠 Usage
If you are writing a script, simply import and run:
```python
import oscar

oscar.run()
```

## 🗑 Uninstallation
Depending on your install method:

| Method | Command |
| :--- | :--- |
| **uv** | `rm -rf .venv` |
| **Conda** | `uv pip uninstall oscar` |
| **pip** | `pip uninstall oscar` |

