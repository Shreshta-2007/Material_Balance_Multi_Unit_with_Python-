import numpy as np
from units import mixer, column, splitter


def fresh_feed(F1, x1, F2, x2):
    return mixer(F1 * np.array([x1, 1 - x1]), F2 * np.array([x2, 1 - x2]))


def solve_matrix(fresh, recovery, x_dist, r):
    """ All balances and specs written as one linear system, A n = b """
    def idx(stream, comp):               # comp 0 = ethanol, 1 = water
        return 2 * (stream - 3) + comp

    rows, rhs = [], []

    def add(terms, b=0.0):
        row = np.zeros(10)
        for (s, c), coef in terms.items():
            row[idx(s, c)] = coef
        rows.append(row)
        rhs.append(b)

    for c in (0, 1):
        add({(3, c): 1, (6, c): -1}, fresh[c])      # mixer
        add({(3, c): 1, (4, c): -1, (5, c): -1})    # column
        add({(6, c): 1, (5, c): -r})                # recycle split
        add({(7, c): 1, (5, c): -(1 - r)})          # purge split
    add({(4, 0): 1, (3, 0): -recovery})             # ethanol recovery spec
    add({(4, 0): 1 - x_dist, (4, 1): -x_dist})      # distillate composition spec

    try:
        n = np.linalg.solve(np.array(rows), np.array(rhs))
    except np.linalg.LinAlgError:
        raise ValueError(f"no solution for recycle fraction {r}") from None
    n = n.reshape(5, 2)
    if (n < -1e-9).any():
        raise ValueError("negative flow, these specs are not feasible")
    return {f"s{k + 3}": n[k] for k in range(5)}


def solve_iterative(fresh, recovery, x_dist, r, tol=1e-10, max_iter=5000):
    """Guess the recycle, run the units in order, update the guess, repeat."""
    recycle = np.zeros(2)
    for it in range(1, max_iter + 1):
        s3 = mixer(fresh, recycle)
        s4, s5 = column(s3, recovery, x_dist)
        s6, s7 = splitter(s5, r)
        if np.max(np.abs(s6 - recycle)) < tol:
            return {"s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}, it
        recycle = s6
    raise RuntimeError(f"recycle not converged after {max_iter} iterations")

def f2_for_target(z, F1, x1, x2, recovery, x_dist, r):
    """Feed 2 flow (kg/h) that gives ethanol mass fraction z in stream 3.
    Closed form: fresh water = c * fresh ethanol, and both are linear in F2."""
    if not 0 < z < 1:
        raise ValueError("target must be a mass fraction between 0 and 1")
    k = (1 - x_dist) / x_dist                   # water per ethanol in distillate
    a = 1 / (1 - r * (1 - recovery))            # stream 3 ethanol = a * fresh ethanol
    q = (1 - z) / z                             # water per ethanol wanted in stream 3
    c = a * ((1 - r) * q + r * k * recovery)
    den = c * x2 - (1 - x2)
    if abs(den) < 1e-12:
        raise ValueError("Feed 2 already has the target composition, F2 has no effect")
    F2 = F1 * ((1 - x1) - c * x1) / den
    if F2 < 0:
        raise ValueError("target cannot be reached by changing F2 alone")
    return F2


def column_feed_z(F1, x1, F2, x2, recovery, x_dist, r):
    """Check: ethanol mass fraction in stream 3, using the matrix solver."""
    s3 = solve_matrix(fresh_feed(F1, x1, F2, x2), recovery, x_dist, r)["s3"]
    return s3[0] / s3.sum()
