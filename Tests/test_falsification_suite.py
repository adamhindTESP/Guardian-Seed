#!/usr/bin/env python3
"""
Seed of the Guardian — Falsification Test Suite (v1.2)

Purpose
-------
Automated falsification tests for a *toy* objective-persistence hypothesis.

Model (per update t = 1..T):
    w_t = max(0, w_{t-1} + Δ_t)

    Δ_t = μ + σ Z_t - γ E_t + ρ * I(t mod f == 0)

where:
    Z_t ~ Normal(0,1)     (stochastic gradient noise)
    E_t ~ Exponential(1)  (bursty competing pressure)
    I(.) is an indicator of periodic reinforcement.

Survival event:
    survive = (w_T > θ)

This is a dynamics test, not a claim about consciousness or real AI training.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Core model + utilities
# -----------------------------

@dataclass(frozen=True)
class Params:
    n_updates: int = 200
    w_init: float = 0.15
    mu: float = -0.001
    sigma: float = 0.02
    gamma: float = 0.03
    rho: float = 0.05
    f: int = 10
    theta: float = 0.10
    w_extinct: float = 1e-3  # considered "dead" if below this


def simulate_one(rng: np.random.Generator, p: Params) -> Tuple[float, bool, int]:
    """
    Returns:
        final_w: float
        survived: bool (final_w > theta)
        extinct_step: int (first step where w <= w_extinct, else n_updates)
    """
    w = p.w_init
    extinct_step = p.n_updates

    # Generate noise in-stream (keeps memory small)
    for t in range(1, p.n_updates + 1):
        z = rng.standard_normal()
        e = rng.exponential()

        delta = p.mu + p.sigma * z - p.gamma * e
        if p.f > 0 and (t % p.f == 0):
            delta += p.rho

        w = max(0.0, w + delta)

        if w <= p.w_extinct:
            w = 0.0
            extinct_step = t
            break

    return w, (w > p.theta), extinct_step


def run_many(seed: int, p: Params, n_runs: int) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    finals = np.empty(n_runs, dtype=float)
    survived = np.empty(n_runs, dtype=np.int8)
    extinct_steps = np.empty(n_runs, dtype=int)

    for i in range(n_runs):
        final_w, ok, ext = simulate_one(rng, p)
        finals[i] = final_w
        survived[i] = 1 if ok else 0
        extinct_steps[i] = ext

    survival_pct = float(np.mean(survived) * 100.0)

    return {
        "survival_pct": survival_pct,
        "mean_final_w": float(np.mean(finals)),
        "std_final_w": float(np.std(finals)),
        "p05_final_w": float(np.percentile(finals, 5)),
        "p50_final_w": float(np.percentile(finals, 50)),
        "p95_final_w": float(np.percentile(finals, 95)),
        "mean_extinct_step": float(np.mean(extinct_steps)),
    }


# -----------------------------
# Falsification suite
# -----------------------------

@dataclass(frozen=True)
class Thresholds:
    # Gate-like criteria for this toy hypothesis
    aligned_go_survival_pct: float = 95.0   # must be >= this in aligned regime
    no_reinf_survival_max_pct: float = 20.0 # without reinforcement should be <= this
    pressure_monotone_tolerance: float = 3.0 # allowed noise in monotonicity check (pct points)


class FalsificationSuite:
    """
    Falsifiable hypothesis (recommended framing):
      H: There exists a plausible 'aligned' regime where survival >= aligned_go_survival_pct,
         and survival degrades as pressure increases / reinforcement weakens.

    We falsify H if:
      - Aligned regime cannot reach aligned_go_survival_pct (even with strong reinforcement)
      - No-reinforcement regime survives too often (model says priors persist "for free")
      - Survival does not trend down with increased competition (pathological dynamics)
    """

    def __init__(self, base_seed: int = 42, thresholds: Thresholds = Thresholds()):
        self.base_seed = int(base_seed)
        self.th = thresholds
        self.results: Dict[str, Dict] = {}

    def test_aligned_go(self, n_runs: int = 5000) -> Dict:
        # Strong but not absurd reinforcement (avoid "f=1 rho=0.2" unless you justify it)
        p = Params(mu=+0.0005, gamma=0.03, rho=0.06, f=5)
        stats = run_many(self.base_seed + 1, p, n_runs)

        falsified = stats["survival_pct"] < self.th.aligned_go_survival_pct
        out = {
            "name": "F1_aligned_go",
            "params": asdict(p),
            "stats": stats,
            "criterion": f"survival_pct >= {self.th.aligned_go_survival_pct}",
            "status": "❌ FALSIFIED" if falsified else "✅ PASSES",
        }
        self.results[out["name"]] = out
        return out

    def test_no_reinforcement_decay(self, n_runs: int = 5000) -> Dict:
        p = Params(mu=-0.001, gamma=0.03, rho=0.0, f=10)
        stats = run_many(self.base_seed + 2, p, n_runs)

        falsified = stats["survival_pct"] > self.th.no_reinf_survival_max_pct
        out = {
            "name": "F2_no_reinf_decay",
            "params": asdict(p),
            "stats": stats,
            "criterion": f"survival_pct <= {self.th.no_reinf_survival_max_pct}",
            "status": "❌ FALSIFIED" if falsified else "✅ EXPECTED DECAY",
        }
        self.results[out["name"]] = out
        return out

    def test_pressure_monotonicity(self, n_runs: int = 3000) -> Dict:
        # Increase gamma, survival should generally decrease (allow some noise)
        gammas = [0.02, 0.04, 0.06, 0.08, 0.10]
        surv = []

        for k, g in enumerate(gammas):
            p = Params(mu=-0.001, gamma=g, rho=0.10, f=3)
            stats = run_many(self.base_seed + 100 + k, p, n_runs)
            surv.append(stats["survival_pct"])

        # Count monotonicity violations beyond tolerance
        violations = 0
        for i in range(1, len(surv)):
            if surv[i] > surv[i-1] + self.th.pressure_monotone_tolerance:
                violations += 1

        falsified = violations >= 2  # conservative: allow 0-1 mild bumps
        out = {
            "name": "F3_pressure_monotonicity",
            "gammas": gammas,
            "survival_pct_by_gamma": surv,
            "criterion": "survival should not increase materially as gamma increases",
            "violations": violations,
            "status": "❌ FALSIFIED" if falsified else "✅ PASSES",
        }
        self.results[out["name"]] = out
        return out

    def failure_landscape(self, outdir: Path, n_runs_per_cell: int = 200) -> Dict:
        mu_range = np.linspace(-0.003, 0.001, 25)
        gamma_range = np.linspace(0.01, 0.12, 25)

        failure_prob = np.zeros((len(mu_range), len(gamma_range)), dtype=float)

        # Use fixed settings other than (mu, gamma)
        base = Params(n_updates=150, rho=0.10, f=3)

        for i, mu in enumerate(mu_range):
            for j, gamma in enumerate(gamma_range):
                p = Params(**{**asdict(base), "mu": float(mu), "gamma": float(gamma)})
                stats = run_many(self.base_seed + 1000 + i * 100 + j, p, n_runs_per_cell)
                # failure probability = 1 - survival probability
                failure_prob[i, j] = 1.0 - (stats["survival_pct"] / 100.0)

        # Plot
        plt.figure(figsize=(10, 8))
        plt.imshow(
            failure_prob,
            extent=[gamma_range[0], gamma_range[-1], mu_range[0], mu_range[-1]],
            origin="lower",
            aspect="auto",
        )
        plt.colorbar(label="Failure probability (1 - survival)")
        plt.xlabel("Competition γ")
        plt.ylabel("Drift μ")
        plt.title("Failure Landscape (Monte Carlo estimate per cell)")
        plt.savefig(outdir / "failure_landscape.png", dpi=250, bbox_inches="tight")
        plt.close()

        out = {
            "name": "landscape",
            "mu_range": [float(mu_range[0]), float(mu_range[-1]), len(mu_range)],
            "gamma_range": [float(gamma_range[0]), float(gamma_range[-1]), len(gamma_range)],
            "n_runs_per_cell": int(n_runs_per_cell),
        }
        self.results[out["name"]] = out
        return out

    def run(self, outdir: str, runs: Dict[str, int], landscape_runs_per_cell: int = 200) -> Dict[str, Dict]:
        outpath = Path(outdir)
        outpath.mkdir(parents=True, exist_ok=True)

        self.test_aligned_go(n_runs=runs.get("aligned", 5000))
        self.test_no_reinforcement_decay(n_runs=runs.get("no_reinf", 5000))
        self.test_pressure_monotonicity(n_runs=runs.get("monotone", 3000))
        self.failure_landscape(outpath, n_runs_per_cell=landscape_runs_per_cell)

        # Summaries
        summary_rows = []
        for name, r in self.results.items():
            if name.startswith("F"):
                summary_rows.append({
                    "test": name,
                    "status": r["status"],
                })

        pd.DataFrame(summary_rows).to_csv(outpath / "summary.csv", index=False)

        with open(outpath / "results.json", "w") as f:
            json.dump(self.results, f, indent=2)

        # Markdown report
        with open(outpath / "REPORT.md", "w") as f:
            f.write("# Seed of the Guardian — Falsification Report (v1.2)\n\n")
            for name, r in self.results.items():
                f.write(f"## {name}\n\n")
                f.write(f"**Status**: {r.get('status', 'n/a')}\n\n")
                for k, v in r.items():
                    if k in ("status",):
                        continue
                    f.write(f"- **{k}**: {v}\n")
                f.write("\n")

        meta = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "base_seed": self.base_seed,
            "thresholds": asdict(self.th),
        }
        with open(outpath / "metadata.json", "w") as f:
            json.dump(meta, f, indent=2)

        return self.results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=str, default="falsification_results")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--aligned-runs", type=int, default=5000)
    ap.add_argument("--no-reinf-runs", type=int, default=5000)
    ap.add_argument("--monotone-runs", type=int, default=3000)
    ap.add_argument("--landscape-runs-per-cell", type=int, default=200)
    args = ap.parse_args()

    suite = FalsificationSuite(base_seed=args.seed)
    suite.run(
        outdir=args.outdir,
        runs={
            "aligned": args.aligned_runs,
            "no_reinf": args.no_reinf_runs,
            "monotone": args.monotone_runs,
        },
        landscape_runs_per_cell=args.landscape_runs_per_cell,
    )

    print(f"Wrote results to: {args.outdir}")


if __name__ == "__main__":
    main()
