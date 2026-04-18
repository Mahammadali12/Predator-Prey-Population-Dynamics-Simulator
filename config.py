"""
Default simulation parameters.
Edit these or override via main.py arguments.

Biological interpretation:
  alpha  = 0.8   prey double roughly every 1/0.8 ≈ 1.25 time units (absent predators)
  beta   = 0.05  each predator-prey encounter reduces prey growth noticeably
  delta  = 0.05  predators reproduce from successful hunts at same rate
  gamma  = 0.5   predator half-life ≈ 1/0.5 = 2 time units (absent prey)
"""

PARAMS = {
    'alpha': 0.8,    # prey birth rate
    'beta':  0.05,   # predation rate
    'delta': 0.05,   # predator reproduction rate per prey eaten
    'gamma': 0.5,    # predator death rate
}

INITIAL_STATE = [40.0, 9.0]    # [prey, predators]

T_START = 0.0
T_END   = 60.0
DT      = 0.05