"""
ODE Solvers
============
Generic, model-agnostic numerical integrators.
Both accept the same interface so they can be swapped freely.

Each solver takes:
  f      - derivative function: f(t, state, params) -> list[float]
  state0 - initial state vector: list[float]
  t0     - start time: float
  t_end  - end time:   float
  dt     - timestep:   float
  params - model parameters: dict

Each solver returns:
  times  - list of time values
  states - list of state vectors (one per timestep)
"""


def euler(f, state0, t0, t_end, dt, params):
    """
    Explicit (Forward) Euler method.

    First-order accurate. Simple but accumulates error quickly —
    especially visible in oscillating systems like Lotka-Volterra.

    Update rule:
        y_{n+1} = y_n + dt * f(t_n, y_n)
    """
    times  = [t0]
    states = [list(state0)]

    t     = t0
    state = list(state0)

    while t < t_end:
        # Clamp final step to not overshoot t_end
        h = min(dt, t_end - t)

        derivs = f(t, state, params)
        state  = [s + h * d for s, d in zip(state, derivs)]
        t     += h

        times.append(t)
        states.append(list(state))

    return times, states


def rk4(f, state0, t0, t_end, dt, params):
    """
    Classical 4th-order Runge-Kutta method.

    Fourth-order accurate. Four derivative evaluations per step
    give a much more accurate trajectory than Euler for the same dt.

    Update rule:
        k1 = f(t,         y)
        k2 = f(t + dt/2,  y + dt/2 * k1)
        k3 = f(t + dt/2,  y + dt/2 * k2)
        k4 = f(t + dt,    y + dt   * k3)
        y_{n+1} = y_n + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
    """
    times  = [t0]
    states = [list(state0)]

    t     = t0
    state = list(state0)

    while t < t_end:
        h = min(dt, t_end - t)

        k1 = f(t,         state,                              params)
        k2 = f(t + h/2,   [s + h/2 * d for s, d in zip(state, k1)], params)
        k3 = f(t + h/2,   [s + h/2 * d for s, d in zip(state, k2)], params)
        k4 = f(t + h,     [s + h   * d for s, d in zip(state, k3)], params)

        state = [
            s + (h / 6.0) * (d1 + 2*d2 + 2*d3 + d4)
            for s, d1, d2, d3, d4 in zip(state, k1, k2, k3, k4)
        ]
        t += h

        times.append(t)
        states.append(list(state))

    return times, states