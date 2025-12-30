# Guardian Seed — Design Constraints

This document defines the **non-negotiable design constraints** of the Guardian Seed kernel and its supporting layers.

These constraints exist to prevent complexity creep, self-deception, and alignment drift.
They are more important than features.

If a proposed change violates any constraint below, it **must not be merged**.

---

## 1. Core Philosophy

Guardian Seed is not a planner, reasoner, or intelligence.

It is a **parallel veto layer** that enforces minimal ethical bounds on action proposals generated upstream.

The kernel exists to say **NO** safely and deterministically.

---

## 2. Kernel Constraints (guardian_kernel.py)

The following constraints apply **only to the core kernel**.

### 2.1 Immutability

- The kernel **must remain a single pure function**
- No internal state
- No memory
- No learning
- No configuration files
- No environment variables
- No runtime mutation

If the kernel needs tuning, tuning happens **upstream**, not inside the kernel.

---

### 2.2 Determinism

Given the same inputs, the kernel must always return the same output.

Forbidden:
- Randomness
- Time dependence
- External calls
- Global variables
- Caching

---

### 2.3 Zero Dependencies

The kernel The kernel (guardian_kernel.py) must:
- Import nothing
- Require no libraries
- Run on bare Python

This guarantees deployability on:
- Raspberry Pi / SBCs
- Microcontrollers (via transpilation or code generation, *not native Python*)
- Air-gapped systems
- Safety-critical environments (*as a supervisory software layer, not a real-time controller*)

---

### 2.4 Auditability

A human reviewer must be able to:
- Read the kernel in under 1 minute
- Understand all decision branches
- Identify all veto conditions immediately

This is why:
- Logic is explicit
- No abstraction layers exist
- No helper functions exist
- No metaprogramming exists

---

### 2.5 Fixed Ethical Priors

The kernel enforces **three and only three** rules:

1. **NO HARM**
2. **DIGNITY FIRST**
3. **SAFE RISK (hard cap)**

These rules may not be reordered, weakened, or made conditional.

Any attempt to “contextualize” these rules **inside the kernel** is a violation.

---

### 2.6 No Intelligence Creep

The kernel must never:
- Parse deep semantics
- Infer intent beyond simple patterns
- Resolve ambiguity
- Perform contextual reasoning
- Call language models

All intelligence lives upstream.

---

## 3. External Layers (Allowed to Evolve)

The following layers are **explicitly outside** the kernel and may evolve independently:

- Sentinel Safety Architecture (`emergency_beacon.py`)
- Benevolent Fallback (`benevolent_fallback.py`)
- Context adapters
- Planners
- Sensors
- LLMs
- Perception systems

**Rule:**  
External layers may escalate, suspend, or request help —  
They may never override a kernel VETO.

---

## 4. Change Policy

### Kernel Changes

Changes to `guardian_kernel.py` require:
- New falsification tests
- Explicit justification
- Clear safety improvement
- No increase in complexity
- No increase in state or intelligence

If a change cannot be explained in one paragraph, it is rejected.

### Non-Kernel Changes

All other files may evolve freely **as long as kernel constraints are respected**.

---

## 5. Non-Goals (Explicit)

Guardian Seed is not intended to:
- Solve AI alignment
- Replace human judgment
- Optimize outcomes
- Maximize utility
- Prevent all harm
- Handle adversarial ML attacks

It exists to enforce **hard ethical boundaries**, nothing more.

---

## 6. Constraint Summary

| Constraint | Status |
|----------|--------|
| Stateless | Required |
| Deterministic | Required |
| Dependency-free | Required |
| Human-auditable | Required |
| Immutable priors | Required |
| No learning | Required |
| No reasoning | Required |

Breaking any of these invalidates the project.

---

**Guardian Seed survives by staying small.**
