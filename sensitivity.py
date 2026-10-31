import numpy as np
import matplotlib.pyplot as plt
from flowsheet import fresh_feed, solve_matrix

base = dict(F1=100, x1=0.10, F2=50, x2=0.60, recovery=0.95, x_dist=0.80, r=0.50)
bump = 0.05   # raise each input by 5%, one at a time


def outputs(p):
    fresh = fresh_feed(p["F1"], p["x1"], p["F2"], p["x2"])
    s = solve_matrix(fresh, p["recovery"], p["x_dist"], p["r"])
    return {
        "product flow (kg/h)": s["s4"].sum(),
        "ethanol recovery (%)": 100 * s["s4"][0] / fresh[0],
        "recycle flow (kg/h)": s["s6"].sum(),
        "column feed ethanol (wt%)": 100 * s["s3"][0] / s["s3"].sum(),
    }

ref = outputs(base)
names = list(ref)
changes = {}   # input -> % change in each output

for key in base:
    p = dict(base)
    p[key] = base[key] * (1 + bump)
    new = outputs(p)
    changes[key] = [100 * (new[n] - ref[n]) / ref[n] for n in names]

print(f"% change in each output when one input goes up by {bump:.0%}\n")
print(f"{'input':<10}" + "".join(f"{n:>28}" for n in names))
for key, row in changes.items():
    print(f"{key:<10}" + "".join(f"{v:>28.2f}" for v in row))

fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
inputs = list(changes)
for ax, j in zip(axes, [0, 2, 3]):
    ax.barh(inputs, [changes[k][j] for k in inputs])
    ax.axvline(0, color="black", lw=0.8)
    ax.set_title(names[j], fontsize=10)
    ax.set_xlabel(f"% change for +{bump:.0%} input")
axes[0].invert_yaxis()
plt.tight_layout()
plt.show()
