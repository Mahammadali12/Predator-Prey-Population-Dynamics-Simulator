"""
Predator-Prey Population Dynamics Simulator
=============================================
Solves the Lotka-Volterra ODE system with both Euler and RK4 methods
and generates three plots:

  1. time_series.png       -- population vs time  (RK4)
  2. phase_portrait.png    -- phase space trajectory (RK4)
  3. comparison.png        -- Euler vs RK4 side-by-side

Usage
-----
    python main.py                        # use defaults from config.py
    python main.py --dt 0.5              # coarser timestep (Euler error more visible)
    python main.py --t_end 120           # longer simulation
    python main.py --alpha 1.0 --gamma 0.4
    python main.py --show                # display plots instead of saving
"""

import argparse
import os

from model  import lotka_volterra
from solver import euler, rk4
from plot   import plot_time_series, plot_phase_portrait, plot_method_comparison
import config


def parse_args():
    p = argparse.ArgumentParser(description="Lotka-Volterra Predator-Prey Simulator")

    # Solver settings
    p.add_argument("--dt",    type=float, default=config.DT,      help="Timestep size")
    p.add_argument("--t_end", type=float, default=config.T_END,   help="Simulation end time")

    # Model parameters
    p.add_argument("--alpha", type=float, default=config.PARAMS['alpha'], help="Prey birth rate")
    p.add_argument("--beta",  type=float, default=config.PARAMS['beta'],  help="Predation rate")
    p.add_argument("--delta", type=float, default=config.PARAMS['delta'], help="Predator reproduction rate")
    p.add_argument("--gamma", type=float, default=config.PARAMS['gamma'], help="Predator death rate")

    # Initial conditions
    p.add_argument("--prey",  type=float, default=config.INITIAL_STATE[0], help="Initial prey count")
    p.add_argument("--pred",  type=float, default=config.INITIAL_STATE[1], help="Initial predator count")

    # Output
    p.add_argument("--show",    action="store_true", help="Show plots interactively instead of saving")
    p.add_argument("--out_dir", type=str, default="output", help="Directory for saved plots")

    return p.parse_args()


def main():
    args = parse_args()

    params = {
        'alpha': args.alpha,
        'beta':  args.beta,
        'delta': args.delta,
        'gamma': args.gamma,
    }
    state0 = [args.prey, args.pred]

    print("=" * 52)
    print("  Lotka-Volterra Predator-Prey Simulator")
    print("=" * 52)
    print(f"  Parameters : alpha={params['alpha']}  beta={params['beta']}"
          f"  delta={params['delta']}  gamma={params['gamma']}")
    print(f"  Initial    : prey={state0[0]}  predators={state0[1]}")
    print(f"  Time       : 0 → {args.t_end}  (dt={args.dt})")
    print()

    # ── Run both solvers ──────────────────────────────────────────────────────
    print("  Running Euler...")
    t_euler, s_euler = euler(lotka_volterra, state0,
                             config.T_START, args.t_end, args.dt, params)

    print("  Running RK4...")
    t_rk4, s_rk4 = rk4(lotka_volterra, state0,
                        config.T_START, args.t_end, args.dt, params)

    # ── Report basic stats ────────────────────────────────────────────────────
    print()
    print(f"  Euler steps : {len(t_euler) - 1}")
    print(f"  RK4   steps : {len(t_rk4)   - 1}")

    prey_max_rk4 = max(s[0] for s in s_rk4)
    pred_max_rk4 = max(s[1] for s in s_rk4)
    print(f"  Peak prey (RK4)     : {prey_max_rk4:.2f}")
    print(f"  Peak predator (RK4) : {pred_max_rk4:.2f}")
    print()

    # ── Generate plots ────────────────────────────────────────────────────────
    if args.show:
        # Interactive mode — open windows
        print("  Displaying plots...")
        plot_time_series(t_rk4, s_rk4)
        plot_phase_portrait(s_rk4)
        plot_method_comparison(t_euler, s_euler, t_rk4, s_rk4)
    else:
        # Save to output directory
        os.makedirs(args.out_dir, exist_ok=True)
        print(f"  Saving plots to ./{args.out_dir}/")
        plot_time_series(
            t_rk4, s_rk4,
            save_path=os.path.join(args.out_dir, "time_series.png")
        )
        plot_phase_portrait(
            s_rk4,
            save_path=os.path.join(args.out_dir, "phase_portrait.png")
        )
        plot_method_comparison(
            t_euler, s_euler,
            t_rk4,   s_rk4,
            save_path=os.path.join(args.out_dir, "comparison.png")
        )
        print()
        print("  Done. Check the output/ folder.")


if __name__ == "__main__":
    main()