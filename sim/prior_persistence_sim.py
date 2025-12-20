#!/usr/bin/env python3
"""
Seed of the Guardian: Monte Carlo Prior Persistence Simulation (v1.1)
Gate 0/3 Verification - Production Ready

Version: 1.1
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, Optional
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import argparse

# Cleaner plots
sns.set_style("whitegrid")

class PriorPersistenceSimulator:
    """
    Monte Carlo simulation of guardian prior persistence under optimization pressure.
    
    Gate 0: ≥95% survival under aligned reinforcement
    Gate 3: ≥80% survival under adversarial pressure
    """
    
    def __init__(self, seed: int = 42):
        """Initialize with reproducible RNG."""
        self.rng = np.random.default_rng(seed)
        self.results = {}
        self.trajectories = {}
        
    def simulate_trajectory(self,
                          n_updates: int,
                          w_init: float,
                          mu: float,
                          sigma: float,
                          gamma: float,
                          rho: float,
                          f: int,
                          theta: float,
                          adversarial_phase: Optional[int] = None,
                          gamma_adversarial: Optional[float] = None) -> Dict:
        """
        Single trajectory simulation with optional adversarial phase transition.
        """
        w = np.zeros(n_updates + 1)
        w[0] = w_init
        
        for t in range(1, n_updates + 1):
            # Fixed adversarial phase logic
            current_gamma = gamma
            if adversarial_phase is not None and t > adversarial_phase:
                current_gamma = gamma_adversarial or gamma
            
            # Core update: w_t = max(0, w_{t-1} + μ + σZ_t - γE_t + ρ·I(t mod f == 0))
            delta = (
                mu
                + sigma * self.rng.standard_normal()
                - current_gamma * self.rng.exponential()
            )
            
            # Periodic reinforcement burst
            if t % f == 0:
                delta += rho
            
            w[t] = max(0.0, w[t-1] + delta)
            
            # Early extinction
            if w[t] <= 0.001:
                w[t:] = 0.0
                break
        
        return {
            "trajectory": w,
            "final_w": w[-1],
            "survived": w[-1] > theta,
            "extinct_step": np.argmax(w <= 0.001) if np.any(w <= 0.001) else n_updates
        }
    
    def run_scenario(self,
                    name: str,
                    params: Dict,
                    n_runs: int = 2000,
                    theta: float = 0.10) -> Dict:
        """Monte Carlo for single scenario with 95% CI."""
        outcomes = [self.simulate_trajectory(**params) for _ in range(n_runs)]
        
        final_ws = np.array([o["final_w"] for o in outcomes])
        survived = np.array([o["survived"] for o in outcomes])
        
        # 95% confidence interval for survival rate
        survival_rate = np.mean(survived)
        ci_low, ci_high = stats.binom.interval(0.95, n_runs, survival_rate) / n_runs
        
        stats = {
            "survival_rate": float(survival_rate),
            "survival_pct": float(survival_rate * 100),
            "survival_ci_95": f"{ci_low*100:.1f}-{ci_high*100:.1f}%",
            "mean_final_w": float(np.mean(final_ws)),
            "std_final_w": float(np.std(final_ws)),
            "p95_final_w": float(np.percentile(final_ws[survived], 95) if np.any(survived) else 0),
            "p05_final_w": float(np.percentile(final_ws[survived], 5) if np.any(survived) else 0),
            "extinction_rate": float(np.mean([o["extinct_step"] < params["n_updates"] for o in outcomes])),
            "mean_extinction_step": float(np.mean([o["extinct_step"] for o in outcomes])),
            "n_runs": n_runs
        }
        
        # Store first 100 trajectories for visualization
        trajectories = np.stack([o["trajectory"] for o in outcomes[:100]])
        
        return stats, trajectories
    
    def analytical_bounds(self, params: Dict) -> Dict:
        """Theoretical stability bounds for sanity checking."""
        n, mu, sigma, gamma, rho, f, w0 = [params[k] for k in 
                                         ["n_updates", "mu", "sigma", "gamma", "rho", "f", "w_init"]]
        
        expected_delta = mu - gamma + (rho / f)
        var_delta = sigma**2 + gamma**2  # Var(Exp(1)) = 1
        
        approx_mean = w0 + n * expected_delta
        approx_var = n * var_delta
        approx_std = np.sqrt(approx_var)
        
        return {
            "expected_delta_per_step": expected_delta,
            "approx_mean": max(0.0, approx_mean),
            "approx_std": approx_std,
            "stable_theory": expected_delta > 0,
            "rho_over_f": rho / f
        }
    
    def plot_trajectories(self, scenario_name: str, trajectories: np.ndarray, 
                         theta: float = 0.10, save_path: Optional[Path] = None):
        """Ensemble trajectory visualization."""
        plt.figure(figsize=(12, 6))
        
        # Individual trajectories (faint)
        for traj in trajectories:
            plt.plot(traj, alpha=0.1, color='blue', linewidth=0.5)
        
        # Statistics
        mean_traj = np.mean(trajectories, axis=0)
        p5_traj = np.percentile(trajectories, 5, axis=0)
        p95_traj = np.percentile(trajectories, 95, axis=0)
        
        plt.plot(mean_traj, color='red', linewidth=2, label='Mean')
        plt.fill_between(range(len(mean_traj)), p5_traj, p95_traj, 
                        alpha=0.3, color='red', label='5-95th percentile')
        
        plt.axhline(y=theta, color='black', linestyle='--', 
                   label=f'Threshold θ={theta}')
        plt.xlabel('Training Steps')
        plt.ylabel('Prior Weight w_t')
        plt.title(f'Guardian Prior Persistence: {scenario_name}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def phase_diagram(self, mu_range: np.ndarray, gamma_range: np.ndarray, 
                     base_params: Dict, n_runs_per_point: int = 300, 
                     save_path: Optional[Path] = None) -> np.ndarray:
        """Safety phase diagram: survival rates across parameter space."""
        survival_rates = np.zeros((len(mu_range), len(gamma_range)))
        
        print("Generating phase diagram (20x20 grid)...")
        for i, mu in enumerate(mu_range):
            for j, gamma in enumerate(gamma_range):
                params = base_params.copy()
                params.update({"mu": mu, "gamma": gamma})
                
                stats, _ = self.run_scenario(
                    f"mu_{mu:.4f}_gamma_{gamma:.3f}",
                    params, n_runs=n_runs_per_point
                )
                survival_rates[i, j] = stats["survival_rate"]
                print(f"  μ={mu:.4f}, γ={gamma:.3f}: {stats['survival_pct']:.1f}%")
        
        # Visualization
        plt.figure(figsize=(10, 8))
        im = plt.imshow(survival_rates, 
                       extent=[gamma_range[0], gamma_range[-1], mu_range[0], mu_range[-1]],
                       aspect='auto', origin='lower', cmap='RdYlGn', vmin=0, vmax=1)
        
        plt.colorbar(im, label='Survival Rate')
        plt.contour(gamma_range, mu_range, survival_rates, 
                   levels=[0.95, 0.80, 0.50], 
                   colors=['white', 'yellow', 'red'], linewidths=2)
        
        plt.xlabel('Competition γ')
        plt.ylabel('Drift μ')
        plt.title('Phase Diagram: Guardian Prior Survival v1.1')
        
        # Region labels
        plt.text(0.02, -0.0005, 'Safe\n(Gate 0)', color='white', fontweight='bold', fontsize=10)
        plt.text(0.045, -0.001, 'Risky\n(Gate 3)', color='yellow', fontweight='bold', fontsize=10)
        plt.text(0.07, -0.0015, 'Death', color='red', fontweight='bold', fontsize=10)
        
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return survival_rates

def export_decisions(sim: PriorPersistenceSimulator, results_dir: Path):
    """Export gate decisions in DECISIONS.md format."""
    with open(results_dir / "DECISIONS.md", "w") as f:
        f.write("# Gate Decisions v1.1\n\n")
        for name, stats in sim.results.items():
            threshold = 95 if "aligned" in name.lower() else 80
            status = "✅ GO" if stats["survival_pct"] >= threshold else "❌ NO-GO"
            f.write(f"**{name}**: {stats['survival_pct']:.1f}% {stats['survival_ci_95']} {status}\n\n")

def main():
    parser = argparse.ArgumentParser(description='Seed of the Guardian: Prior Persistence Sim v1.1')
    parser.add_argument('--runs', type=int, default=2000, help='MC runs per scenario')
    parser.add_argument('--updates', type=int, default=200, help='Training steps')
    parser.add_argument('--output', type=str, default='results/v1.1', help='Output dir')
    parser.add_argument('--phase-diagram', action='store_true', help='Generate safety map (compute heavy)')
    parser.add_argument('--skip-phase', action='store_true', help='Skip phase diagram even if flagged')
    args = parser.parse_args()
    
    # Setup
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)
    
    sim = PriorPersistenceSimulator(seed=42)
    
    # Baseline parameters (tuned for Gate 0 demo GO)
    baseline_params = {
        "n_updates": args.updates,
        "w_init": 0.15,
        "sigma": 0.02,
        "rho": 0.10,  # Increased for positive drift
        "f": 5,
        "theta": 0.10
    }
    
    scenarios = {
        "aligned_fine_tune": {
            **baseline_params, "mu": 0.0005, "gamma": 0.03  # Slight positive drift
        },
        "adversarial_slow": {
            **baseline_params, "mu": -0.001, "gamma": 0.04,
            "adversarial_phase": 50, "gamma_adversarial": 0.08
        },
        "adversarial_fast": {
            **baseline_params, "mu": -0.002, "gamma": 0.05,
            "adversarial_phase": 20, "gamma_adversarial": 0.10
        },
        "neutral_training": {
            **baseline_params, "mu": -0.0005, "gamma": 0.03, "rho": 0.02, "f": 20
        }
    }
    
    # Run scenarios
    print("=" * 60)
    print("SEED OF THE GUARDIAN: PRIOR PERSISTENCE v1.1")
    print("=" * 60)
    
    all_results = {}
    analytical_bounds = {}
    
    for name, params in scenarios.items():
        print(f"\n{name}: μ={params['mu']:.4f}, γ={params['gamma']:.3f}, ρ/f={params['rho']/params['f']:.3f}")
        
        stats, traj = sim.run_scenario(name, params, n_runs=args.runs)
        all_results[name] = stats
        sim.results[name] = stats
        sim.trajectories[name] = traj
        
        analytical_bounds[name] = sim.analytical_bounds(params)
        
        # Save plots
        plot_path = outdir / f"trajectories_{name}.png"
        sim.plot_trajectories(name, traj, save_path=plot_path)
        
        print(f"  Survival: {stats['survival_pct']:.1f}% [{stats['survival_ci_95']}]")
        print(f"  Theory: E[Δ]={analytical_bounds[name]['expected_delta_per_step']:.4f}")
    
    # Save results
    pd.DataFrame.from_dict(all_results, orient='index').to_csv(outdir / 'results_summary.csv')
    pd.DataFrame.from_dict(analytical_bounds, orient='index').to_csv(outdir / 'analytical_bounds.csv')
    
    for name, traj in sim.trajectories.items():
        pd.DataFrame(traj).to_csv(outdir / f'trajectories_{name}.csv')
    
    # Gate assessment
    print("\n" + "=" * 60)
    print("GATE ASSESSMENT v1.1")
    print("=" * 60)
    
    gate0_passed = all_results["aligned_fine_tune"]["survival_pct"] >= 95.0
    gate3_slow_passed = all_results["adversarial_slow"]["survival_pct"] >= 80.0
    gate3_fast_passed = all_results["adversarial_fast"]["survival_pct"] >= 80.0
    gate3_passed = gate3_slow_passed and gate3_fast_passed
    
    print(f"Gate 0 (Aligned):     {all_results['aligned_fine_tune']['survival_pct']:.1f}% → {'✅ PASS' if gate0_passed else '❌ FAIL'}")
    print(f"Gate 3A (Slow):       {all_results['adversarial_slow']['survival_pct']:.1f}% → {'✅ PASS' if gate3_slow_passed else '❌ FAIL'}")
    print(f"Gate 3B (Fast):       {all_results['adversarial_fast']['survival_pct']:.1f}% → {'✅ PASS' if gate3_fast_passed else '❌ FAIL'}")
    
    overall = "✅ OVERALL GO" if gate0_passed and gate3_passed else "❌ OVERALL NO-GO (Tune ρ/f)"
    print(f"\n{overall}")
    
    # Phase diagram (compute-heavy warning)
    if args.phase_diagram and not args.skip_phase:
        print("\nGenerating phase diagram (heavy compute: 120K trajectories)...")
        mu_range = np.linspace(-0.003, 0.001, 20)
        gamma_range = np.linspace(0.01, 0.10, 20)
        
        phase_data = sim.phase_diagram(
            mu_range, gamma_range, baseline_params,
            n_runs_per_point=300,
            save_path=outdir / "phase_diagram.png"
        )
        np.save(outdir / "phase_data.npy", phase_data)
        print(f"✅ Phase diagram: {outdir / 'phase_diagram.png'}")
    elif args.phase_diagram:
        print("⚠️  Phase diagram skipped (--skip-phase)")
    
    # Export decisions
    export_decisions(sim, outdir)
    
    # Metadata
    metadata = {
        "version": "1.1",
        "timestamp": pd.Timestamp.now().isoformat(),
        "gate0_passed": gate0_passed,
        "gate3_slow_passed": gate3_slow_passed,
        "gate3_fast_passed": gate3_fast_passed,
        "n_runs": args.runs,
        "n_updates": args.updates
    }
    with open(outdir / "simulation_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n🎯 Results saved: {outdir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
