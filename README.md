# Material_Balance_Multi_Unit_with_Python
# Ethanol-Water Flowsheet: Steady-State Material Balance (Python)
## Problem statement

Recycle streams make process calculations circular: you can't know what comes back to the mixer until you know what leaves the column, and you can't know that until you know what enters the mixer.

This project breaks that loop. Two ethanol-water feeds are blended, separated in a distillation column, and split, with part of the overhead recycled back to the start. The program solves every stream flow and composition two ways, with a direct matrix solution and an iterative recycle solver, and checks that they agree. All done using Python

It also answers the questions an engineer would actually ask:
- **What happens to product purity if feed 2 changes?** (sensitivity sweep)
- **How much of feed 2 do I need to hit a target ethanol wt%?** (target-composition solver)

## Full report

See [`[Material Balance Project Report (3).pdf](https://github.com/user-attachments/files/34207923/Material.Balance.Project.Report.3.pdf)
 for the full derivation, assumptions and discussion.

The goal is to find all unknown stream flows and compositions at steady state.

## What the code does

- Builds the flowsheet from reusable unit models (mixer, column, splitter)
- Solves the material balances with a **matrix (linear algebra) solver**
- Handles the recycle with an **iterative solver** and compares it against the direct solution
- Runs a **sensitivity sweep** of feed 2 flow rate
- Finds the **feed 2 flow needed to hit a target ethanol wt%** in stream 3
- Saves plots to `figures/`

## Project structure

```
unit.py          unit operation models
flowsheet.py     connects units into the flowsheet
run.py           runs the solvers, sweep and plots
requirements.txt dependencies
figures/         output plots
```

## How to run

```bash
pip install -r requirements.txt
python run.py
```

Requires Python 3 with `numpy` and `matplotlib`.

## Results

<img width="343" height="118" alt="Python_result" src="https://github.com/user-attachments/assets/cffddff2-a035-4cae-9a2c-24b778aae43c" /> 

<img width="354" height="163" alt="sensitivity graphs" src="https://github.com/user-attachments/assets/5dd79fe5-921a-494f-8932-8dad9d98ccb6" />


## Assumptions

- Steady state, no accumulation
- No reaction


## Author

Shreshta Kanduri | BITS Pilani Dubai, B.E Chemical Engineering | www.linkedin.com/in/shreshta-kanduri-311230312
