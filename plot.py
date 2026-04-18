"""
Visualization
==============
Three plots:
  1. Time series     -- prey and predator populations over time
  2. Phase portrait  -- predator vs prey (parametric trajectory)
  3. Method comparison -- Euler vs RK4 divergence on same axes
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ── Colour palette ────────────────────────────────────────────────────────────
PREY_COLOR      = "#2196F3"   # blue
PRED_COLOR      = "#F44336"   # red
EULER_COLOR     = "#FF9800"   # orange  (used in comparison plot)
RK4_COLOR       = "#4CAF50"   # green
BG_COLOR        = "#0D1117"   # dark background
GRID_COLOR      = "#21262D"
TEXT_COLOR      = "#E6EDF3"


def _apply_dark_style(ax, title, xlabel, ylabel):
    """Apply consistent dark theme to an axes object."""
    ax.set_facecolor(BG_COLOR)
    ax.set_title(title,  color=TEXT_COLOR, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(xlabel, color=TEXT_COLOR, fontsize=10)
    ax.set_ylabel(ylabel, color=TEXT_COLOR, fontsize=10)
    ax.tick_params(colors=TEXT_COLOR)
    ax.grid(True, color=GRID_COLOR, linewidth=0.6, linestyle='--')
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.legend(facecolor="#161B22", edgecolor=GRID_COLOR,
              labelcolor=TEXT_COLOR, fontsize=9)


def plot_time_series(times, states, title="Population Dynamics over Time",
                     save_path=None):
    """
    Plot prey and predator populations as a function of time.

    Parameters
    ----------
    times      : list[float]
    states     : list[list[float]]   -- each entry is [prey, predator]
    title      : str
    save_path  : str | None          -- if given, saves to file instead of showing
    """
    prey      = [s[0] for s in states]
    predators = [s[1] for s in states]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG_COLOR)

    ax.plot(times, prey,      color=PREY_COLOR, linewidth=1.8, label="Prey (x)")
    ax.plot(times, predators, color=PRED_COLOR, linewidth=1.8, label="Predator (y)")

    _apply_dark_style(ax, title, "Time (arbitrary units)", "Population")

    plt.tight_layout()
    _save_or_show(fig, save_path)


def plot_phase_portrait(states, title="Phase Portrait — Predator vs Prey",
                        save_path=None):
    """
    Parametric plot of predator population vs prey population.
    Closed loops indicate stable oscillations.

    Parameters
    ----------
    states    : list[list[float]]
    title     : str
    save_path : str | None
    """
    prey      = [s[0] for s in states]
    predators = [s[1] for s in states]

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor(BG_COLOR)

    # Gradient colouring to show direction of time
    n = len(prey)
    for i in range(n - 1):
        alpha = 0.3 + 0.7 * (i / n)          # fade in over time
        ax.plot(prey[i:i+2], predators[i:i+2],
                color=RK4_COLOR, alpha=alpha, linewidth=1.2)

    # Mark start point
    ax.scatter(prey[0], predators[0], color="white", s=60, zorder=5,
               label=f"Start ({prey[0]:.0f}, {predators[0]:.0f})")

    _apply_dark_style(ax, title, "Prey population (x)", "Predator population (y)")
    plt.tight_layout()
    _save_or_show(fig, save_path)


def plot_method_comparison(times_euler, states_euler,
                           times_rk4,   states_rk4,
                           save_path=None):
    """
    Side-by-side comparison of Euler and RK4 solutions.
    Shows how numerical error accumulates in the lower-order method.

    Parameters
    ----------
    times_euler, states_euler : Euler solution
    times_rk4,   states_rk4  : RK4 solution
    save_path : str | None
    """
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor(BG_COLOR)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # ── Top-left: Euler time series ───────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    _plot_ts(ax1, times_euler, states_euler,
             "Euler — Time Series", EULER_COLOR, "#EF9A9A")

    # ── Top-right: RK4 time series ────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    _plot_ts(ax2, times_rk4, states_rk4,
             "RK4 — Time Series", RK4_COLOR, "#81C784")

    # ── Bottom-left: Euler phase portrait ─────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    _plot_phase(ax3, states_euler, "Euler — Phase Portrait", EULER_COLOR)

    # ── Bottom-right: RK4 phase portrait ──────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    _plot_phase(ax4, states_rk4, "RK4 — Phase Portrait", RK4_COLOR)

    fig.suptitle("Euler vs RK4 — Numerical Method Comparison",
                 color=TEXT_COLOR, fontsize=14, fontweight='bold', y=1.01)

    _save_or_show(fig, save_path)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _plot_ts(ax, times, states, title, prey_c, pred_c):
    prey = [s[0] for s in states]
    pred = [s[1] for s in states]
    ax.plot(times, prey, color=prey_c, linewidth=1.5, label="Prey")
    ax.plot(times, pred, color=pred_c, linewidth=1.5, label="Predator", linestyle='--')
    _apply_dark_style(ax, title, "Time", "Population")


def _plot_phase(ax, states, title, color):
    prey = [s[0] for s in states]
    pred = [s[1] for s in states]
    ax.plot(prey, pred, color=color, linewidth=1.2, alpha=0.85, label="Trajectory")
    ax.scatter(prey[0], pred[0], color="white", s=50, zorder=5, label="Start")
    _apply_dark_style(ax, title, "Prey (x)", "Predator (y)")


def _save_or_show(fig, save_path):
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight',
                    facecolor=fig.get_facecolor())
        print(f"  Saved → {save_path}")
        plt.close(fig)
    else:
        plt.show()