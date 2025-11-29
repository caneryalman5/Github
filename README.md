# TSP OR-Tools Example

This repository contains an example implementation of the Traveling Salesman Problem (TSP) using Google OR-Tools.

- `tsp_ortools.py`: Runnable script that builds a small TSP instance, solves it with OR-Tools and saves a route plot.
- `tsp_ortools_ran.ipynb`: Executed notebook with outputs (for reference).

Quick start
1. Create a Python virtual environment and activate it:

```bash
cd ~/Desktop/Github
python3 -m venv tsp_venv
source tsp_venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Run the script:

```bash
python tsp_ortools.py
```

Notes
- The script saves the generated route plot as `tsp_route.png` in the repo root when run.
- Do not commit your virtual environment (`tsp_venv/`) — it is included in `.gitignore`.
