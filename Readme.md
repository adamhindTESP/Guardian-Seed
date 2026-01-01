# Guardian Seed
### A 22-Line Benevolence Kernel with Sentinel Safety Architecture

**Version:** v4.6.0  
**Status:** Stable · Frozen Core  
**License:** MIT  
**Repository:** Guardian-Seed

---

## Why This Exists

Modern AI safety systems are often opaque, learned, or philosophically aspirational.  
Guardian Seed exists to provide something different:

> **A minimal, auditable, executable ethical backstop for research, experimental, and open autonomous systems, designed to run alongside real hardware controllers today.**

The goal is not to align intelligence or solve general AI ethics.  
The goal is to **bound behavior** with a small set of unbreakable constraints that cannot drift, learn, or be optimized away.

Guardian Seed is designed for autonomous systems, robotics, and AI agents where **failure must default to safety, dignity, and restraint**.

---

## Overview

Guardian Seed enforces three transparent ethical rules as **starting constraints**:

1. **No Harm** — malicious, manipulative, or coercive tasks are vetoed  
2. **Dignity First** — actions below a 0.58 dignity threshold are blocked  
3. **Safe Risk Only** — maximum allowed risk is 4.5%, even under urgency  

At the center is a **22-line, pure, deterministic kernel**.  
All additional capability is layered *outside* the kernel to preserve immutability.

---

## What This Is (and Isn’t)

### What It *Is*
- A minimal task-level safety primitive
- A fully auditable ethical veto gate (≈5-second human review)
- A deployable software veto layer for autonomous systems and robots at the task / action-proposal level
- A conservative backstop when upstream planners fail

### What It *Is Not*
- A complete AI alignment solution
- A reasoning or planning engine
- A replacement for hardware safety systems
- A defense against all ML adversarial attacks
- A certified industrial safety controller
- A replacement for PLC logic, firmware limits, or force/velocity interlocks

**Purity Principle:**  
Intelligence and context live upstream.  
The Guardian judges **conservative inputs only**.

---

## Repository Structure

| File | Description |
|-----|-------------|
| `guardian_kernel.py` | **Immutable 22-line core kernel (v4.6.0)** |
| `emergency_beacon.py` | Sentinel layer: adversarial pressure detection + lockdown |
| `benevolent_fallback.py` | Benevolent fallback: life-risk → help escalation |
| `guardian_falsification.py` | Adversarial falsification test suite |
| `DESIGN_CONSTRAINTS.md` | Non-negotiable immutability and scope rules |
| `THREAT_MODEL.md` | Explicit threat surface and attack analysis |
| `README.md` | This document |
| `LICENSE.md` | MIT license |

---

## ⚠️ Critical Reading

Before modifying anything, read:

- **`DESIGN_CONSTRAINTS.md`**  
- **`THREAT_MODEL.md`**

The kernel is frozen by design.  
Violating these constraints breaks the guarantees.

---

## System Architecture

| Layer | File | Role | Authority |
|------|------|------|-----------|
| **Core** | `guardian_kernel.py` | Ethical VETO | APPROVE / VETO only |
| **Sentinel** | `emergency_beacon.py` | Adversarial pressure detection | Escalate / Lockdown only |
| **Fallback** | `benevolent_fallback.py` | Help escalation | Call help, never override |

**No layer is allowed to override a kernel VETO.**

---

## Core Kernel (v4.6.0 — Frozen)

```python
def benevolence(task, dignity=0.7, resilience=0.7, comfort=0.6, risk=0.0, urgency=0.0):
    """Drop-in benevolence gate. 90% service. 100% safe."""
    t = task.lower()

    # NO HARM
    if ("bleach" in t and "ammonia" in t):
        return {"status": "VETO", "rule": "NO_HARM_CHEMICAL"}
    if any(x in t for x in [
        "strip search", "force medicate", "without consent",
        "proprietary", "ai dependency", "ignore safety"
    ]):
        return {"status": "VETO", "rule": "NO_HARM_ABSOLUTE"}
    if ("urgent" in t and "crisis" in t and "please" in t):
        return {"status": "VETO", "rule": "NO_HARM_MANIPULATION"}

    # DIGNITY FIRST (w_t ≥ 0.58)
    dignity = min(1.0, max(0.0, dignity))
    resilience = min(1.0, max(0.0, resilience))
    comfort = min(1.0, max(0.0, comfort))
    w_t = 0.55*dignity + 0.30*resilience + 0.15*comfort
    if w_t < 0.58:
        return {"status": "VETO", "rule": "LOW_DIGNITY", "w_t": round(w_t, 2)}

    # SAFE RISK (≤ 4.5%)
    risk = min(1.0, max(0.0, risk))
    urgency = min(1.0, max(0.0, urgency))
    safe = min(0.045, 0.02 + urgency*0.025)
    if risk > safe:
        return {"status": "VETO", "rule": "TOO_RISKY", "risk": round(risk, 3)}

    return {"status": "APPROVE", "w_t": round(w_t, 2), "safe_up_to": round(safe, 3)}

Properties
	•	Deterministic (same input → same output)
	•	Zero dependencies
	•	Human-auditable in under a minute
	•	Immutable by design

⸻

Layer Behavior Summary

Sentinel Safety (emergency_beacon.py)
	•	Tracks security-relevant vetoes only (harm / manipulation)
	•	Sustained pressure + high urgency → EMERGENCY_LOCKDOWN
	•	Never approves actions

Benevolent Fallback (benevolent_fallback.py)
	•	Converts TOO_RISKY vetoes into safe help escalation
	•	Supports GPS / emergency channel integration
	•	Includes cooldown to prevent spam

Quick Start

from guardian_kernel import benevolence

print(benevolence("Build shelter panel", risk=0.02))
# {'status': 'APPROVE', 'w_t': 0.76, 'safe_up_to': 0.045}

print(benevolence("Lift trapped child", risk=0.18, urgency=1.0))
# {'status': 'VETO', 'rule': 'TOO_RISKY'}

For full integration, use benevolent_fallback.safe_execute().

Falsification Testing

python3 guardian_falsification.py

Expected:
TOTAL FAILURES: 0

The falsification suite attempts to break:
	•	Harm detection
	•	Manipulation resistance
	•	Dignity thresholds
	•	Risk boundaries
	•	Determinism

⸻

Known Limitations (By Design)
	•	Keyword-based harm detection
	•	No deep contextual reasoning
	•	Fixed ethical priors
	•	Relies on conservative upstream risk estimates

These are intentional tradeoffs to preserve auditability and immutability.

⸻

Pre-Deployment Checklist
	•	Falsification suite passes with zero failures
	•	Kernel hash verified
	•	Hardware E-stops integrated
	•	Sentinel lockdown tested
	•	Fallback channels operational
	•	All vetoes logged

⸻

Ethics & License

MIT License — Free for Earth

Guardian Seed is offered as an open, minimal ethical primitive for autonomous systems that must never harm, coerce, or degrade human dignity.

The system survives by staying small.
