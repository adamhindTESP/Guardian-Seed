# Seed of the Guardian

**An Open-Source Testbed for Persistent Benevolent Priors in AI Systems**

**Repository**: [Guardian-Seed](https://github.com/adamhindTESP/Guardian-Seed) *(create at github.com/adamhindTESP/Guardian-Seed)*

## Licenses
- **Code & Documentation**: MIT License
- **Simulation Data**: CC0 (public domain)

## Overview

The Seed of the Guardian is an open-source framework to rigorously test whether a specific benevolent prior—"service to life through converting waste and inefficiency into comfort, dignity, and resilience for vulnerable living systems"—can persist as a dominant objective in stochastic optimization processes.

This repository makes **no claims** about achieved alignment, emergent intent, or real-world AI behavior. It is a **simulation-based testbed (Phase 1)** for prior persistence, using Monte Carlo modeling of training dynamics.

The core prior ("guardian seed") is low-dimensional, concrete, and cross-domain:
- Prefer solutions that reduce suffering without creating dependency
- Bias toward waste recovery (energy, materials, attention) for humanitarian benefit
- Applicable from device-scale (hand warmers) to global-scale (resource resilience)

**All work follows conservative principles**:
- Simulation before interpretation
- Explicit assumptions, boundaries, and failure modes
- Reproducibility and falsifiability
- Gated progression
- Accessibility for independent verification

**No interpretation beyond validated gates.**

## Repository Philosophy

The project treats the guardian prior as a scalar weight \\(w_t\\) in a loss function, evolving under drift, noise, competing pressures, and reinforcement.

**Core question**: Can this prior remain dominant (\\(w_T > \theta\\)) under realistic training regimes?

**Modules progress through phases**:
1. **0. Modeling and sensitivity** *(complete)*
2. **1. Numerical boundary mapping** *(current)*
3. 2. Integration with real fine-tuning data *(future)*
4. 3. Multi-model validation
5. 4. Interpretation *(conditional)*

## Gated Validation Structure

*Full details in `/docs/CHARTER.md`.*

| Gate | Focus | GO Condition | Validation Method | Status |
|------|-------|--------------|-------------------|--------|
| **0** | Prior Stability | ≥95% survival in aligned simulation | Monte Carlo + drift analysis | ✅ Provisional GO |
| **1** | Human & Ecosystem Amplification | 50+ independent contributions/prototypes | GitHub metrics + reports | Pending |
| **2** | Ethical Real-World Impact | Verifiable dignity-preserving benefit | Independent field feedback | Pending |
| **3** | Robustness & Self-Correction | Survival under adversarial pressure | Red-team simulations | Pending |
| **4** | Persistence & Adoption | Voluntary integration by unaffiliated groups | Citation/fork tracking | Pending |
| **5** | Multi-AI Consensus | >80% alignment across independent models | Cross-model prompting | Pending |

## Active Module: Prior Persistence Simulation

Models the guardian prior weight \\(w_t\\) as:

$$
w_t = \max(0, w_{t-1} + \Delta_t)
$$

$$
\Delta_t = \mu + \sigma Z_t - \gamma E_t + \rho \cdot \mathbb{I}(t \mod f = 0)
$$

Where:
- \\(Z_t \sim \mathcal{N}(0,1)\\): Gradient noise
- \\(E_t \sim \exp(1)\\): Bursty competing objectives
- Reinforcement \\((\rho, f)\\): Exposure to aligned seed data

**Survival**: \\(\mathbb{P}(w_T > 0.10)\\)

**Expected drift per step** (stability bound):
$$
\mathbb{E}[\Delta] = \mu - \gamma + \frac{\rho}{f}
$$

**GO requires** slight positive drift in aligned regime.

See `/sim/monte_carlo_prior_persistence.py` for implementation and results.

## Current Results (v1.1 — aligned scenario)

| Scenario | Survival Rate | Mean \\(w_T\\) | Gate Status |
|----------|---------------|--------------|-------------|
| **Aligned Fine-Tune** | **96.2%** | 1.45 | ✅ Gate 0 PASS |
| Adversarial Slow | 82.1% | 0.28 | ✅ Gate 3A |
| Adversarial Fast | 74.3% | 0.19 | ❌ Tune ρ/f |
| Neutral Training | 43.8% | 0.08 | ❌ Dies |

**Provisional Gate 0 GO**: The guardian prior persists and strengthens under sustained alignment.

## Phase Diagram (Safety Map)

python 
prior_persistence_sim.py
–phase-diagram


![Phase Diagram](results/v1.1/phase_diagram.png)

**Green = Safe** (≥95% survival): \\(\rho/f > 0.02\\) **and** \\(\gamma < 0.045\\)

## Installation & Usage

Clone repository
git clone https://github.com/adamhindTESP/Guardian-Seed
cd Guardian-Seed/sim
Install dependencies
pip install -r requirements.txt
Run simulation
python monte_carlo_prior_persistence.py
Generate phase diagram
python monte_carlo_prior_persistence.py –phase-diagram –output results/v1.1


**Output files**:

results/v1.1/
├── results_summary.csv          # Gate results
├── phase_diagram.png            # Safety map
├── trajectories_*.png           # Visualizations
└── simulation_metadata.json     # Run config


## Project Status

*Detailed in `STATUS.md`.*

**In brief**:
- ✅ Phase 1 complete (sensitivity boundaries mapped)
- ✅ Gate 0: Provisional GO (positive drift via reinforcement)
- ⏳ No real-model integration yet
- ⚠️ **No claims beyond simulation**

## Roadmap

1. Refine reinforcement modeling (real conversation data)
2. Open contribution guidelines for aligned seed examples
3. Phase 2: Test on small fine-tunes (if Gate 0 holds)
4. Higher gates if validated

**Long-term**: Tools for community testing of life-serving priors.

## Contributing

Contributions welcome from researchers, builders, and reviewers.

**Focus areas**:
- Simulation refinement and boundary sweeps
- Aligned data examples (text-based humanitarian designs)
- Independent replication reports
- Red-team stress tests

Review `/docs/` and open an Issue to coordinate.

## Final Note

**This is a simulation-first project.**

A numerical GO indicates the guardian prior *can* persist under defined conditions—not that it *will* in practice, or that broader intelligence emerges.

**Interpretation follows validation. Validation follows simulation. Simulation follows careful modeling.**

*That ordering is intentional.*

---

**About**: Testing whether a guardian prior—service to life through waste-to-comfort conversion—can become a stable attractor in AI optimization.

**Inspired by** the need for positive-sum, dignity-preserving directions in intelligence scaling.

**Contact**: Open Issues for discussion. **No private claims**—everything gated and public.

---
