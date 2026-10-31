import numpy as np
import matplotlib.pyplot as plt
from flowsheet import (fresh_feed, solve_matrix, solve_iterative,
                       f2_for_target, column_feed_z)

fresh = fresh_feed(F1=100, x1=0.10, F2=50, x2=0.60)
recovery, x_dist, r = 0.95, 0.80, 0.5

streams = solve_matrix(fresh, recovery, x_dist, r)
streams_it, n_iter = solve_iterative(fresh, recovery, x_dist, r)

print("stream   ethanol    water    total   %EtOH")
for name, s in streams.items():
    print(f"{name:>6} {s[0]:9.3f} {s[1]:8.3f} {s.sum():8.3f} {100*s[0]/s.sum():7.2f}")

print(f"\nmatrix and iteration agree: "
      f"{all(np.allclose(streams[k], streams_it[k]) for k in streams)} "
      f"({n_iter} iterations)")

# overall balance: fresh in = product + purge out, per component
print("overall balance residual:", fresh - streams["s4"] - streams["s7"])
print(f"ethanol recovered in product: {streams['s4'][0] / fresh[0]:.1%}")

# Feed 2 needed for a target ethanol fraction in stream 3
target = 0.20
F2_needed = f2_for_target(target, F1=100, x1=0.10, x2=0.60,
                          recovery=recovery, x_dist=x_dist, r=r)

# check the answer with both solvers
fresh_t = fresh_feed(F1=100, x1=0.10, F2=F2_needed, x2=0.60)
streams_t, n_iter_t = solve_iterative(fresh_t, recovery, x_dist, r)
z_iter = streams_t["s3"][0] / streams_t["s3"].sum()
z_matrix = column_feed_z(100, 0.10, F2_needed, 0.60, recovery, x_dist, r)

print(f"\nF2 for {target:.0%} ethanol in stream 3: {F2_needed:.2f} kg/h")
print(f"stream 3 check: matrix {z_matrix:.2%}, iteration {z_iter:.2%}")

print("\nstream   ethanol    water    total   %EtOH   (target case)")
for name, s in streams_t.items():
    print(f"{name:>6} {s[0]:9.3f} {s[1]:8.3f} {s.sum():8.3f} {100*s[0]/s.sum():7.2f}")

# sweep the recycle fraction
r_values = np.linspace(0, 0.95, 40)
recov, recycle_flow = [], []
for rv in r_values:
    s = solve_matrix(fresh, recovery, x_dist, rv)
    recov.append(100 * s["s4"][0] / fresh[0])
    recycle_flow.append(s["s6"].sum())


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(r_values, recov)
ax1.set_xlabel("recycle fraction of bottoms")
ax1.set_ylabel("ethanol recovered in product (%)")
ax2.plot(r_values, recycle_flow)
ax2.set_xlabel("recycle fraction of bottoms")
ax2.set_ylabel("recycle flow (kg/h)")
plt.tight_layout()
plt.show()
