"""Unit operations for the ethanol-water recycle flowsheet.
A stream is a numpy array [ethanol, water] of component flows in kg/h.
"""
import numpy as np

def mixer(*streams):
    return np.sum(streams, axis=0)

def column(feed, recovery, x_dist):
    """Split a feed into distillate and bottoms.
        recovery: fraction of the feed ethanol that goes overhead
      x_dist:   ethanol mass fraction of the distillate
      These two specs fix the distillate, and the bottoms is the rest.
    """
    d_etoh = recovery * feed[0]
    d_water = d_etoh * (1 - x_dist) / x_dist
    dist = np.array([d_etoh, d_water])
    bottoms = feed - dist
    if bottoms[1] < 0:
        raise ValueError("specs ask for more water in the distillate than the feed has")
    return dist, bottoms

def splitter(stream, frac_first):
    """Same composition in both outlets; frac_first goes to the first one."""
    return frac_first * stream, (1 - frac_first) * stream


   
