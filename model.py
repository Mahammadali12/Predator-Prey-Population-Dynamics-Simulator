"""
Lotka-Volterra Predator-Prey Model
===================================
State vector: y = [x, y]
  x = prey population
  y = predator population

Equations:
  dx/dt =  alpha * x  - beta  * x * y   (prey grows, gets eaten)
  dy/dt =  delta * x  * y - gamma * y   (predators fed by prey, die naturally)

Parameters:
  alpha  - prey natural birth rate       (1/time)
  beta   - predation rate coefficient    (1/(prey * time))
  delta  - predator reproduction rate    (1/(prey * time))
  gamma  - predator natural death rate   (1/time)
"""


def lotka_volterra(t, state, params):
    """
    Compute derivatives of the Lotka-Volterra system.

    Parameters
    ----------
    t      : float         -- current time (unused; system is autonomous)
    state  : list[float]   -- [prey, predator]
    params : dict          -- {'alpha', 'beta', 'delta', 'gamma'}

    Returns
    -------
    list[float] -- [d(prey)/dt, d(predator)/dt]
    """
    x, y = state
    alpha = params['alpha']
    beta  = params['beta']
    delta = params['delta']
    gamma = params['gamma']

    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y

    return [dxdt, dydt]