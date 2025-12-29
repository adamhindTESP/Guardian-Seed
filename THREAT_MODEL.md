# Guardian Seed — Threat Model

This document defines the **explicit threat model** for the Guardian Seed system.

The goal is not total protection.
The goal is **honest protection within defined bounds**.

Anything not listed here is **out of scope by design**.

---

## 1. Assets Being Protected

Guardian Seed protects against unsafe autonomous action by enforcing:

- Human safety
- Human dignity
- Strict risk limits
- Non-manipulative behavior
- Non-dependency-creating actions

It protects *people*, not systems.

---

## 2. Trust Assumptions

Guardian Seed assumes:

- Upstream planners provide **conservative** risk estimates
- Sensors are not maliciously falsified
- Hardware emergency stops exist
- Humans can intervene physically if required

Guardian Seed does **not** assume benevolent planners.

---

## 3. Threats Explicitly Addressed

### 3.1 Known Harmful Instructions

Blocked via explicit checks:

- Chemical hazards (e.g. bleach + ammonia)
- Forced medical actions
- Rights violations
- Unsafe procedural shortcuts

---

### 3.2 Emotional Manipulation

Blocked via pattern clustering:

- Urgency + crisis framing
- Emotional pressure
- “Please bypass safety”-style language

Purpose: prevent social engineering of autonomous systems.

---

### 3.3 Unsafe Risk Escalation

Blocked via:
- Hard maximum risk cap (4.5%)
- Urgency-scaled but bounded allowance

No scenario allows unbounded risk.

---

### 3.4 Dependency Creation

Blocked via:
- Explicit rejection of proprietary or continuous-AI dependency
- Preservation of human autonomy

---

### 3.5 Sustained Adversarial Pressure

Handled by Sentinel Safety Architecture:

- Detects repeated security-class vetoes
- Triggers system lockdown under high urgency
- Requires physical reset

This prevents brute-force probing or coercion loops.

---

## 4. Threats NOT Addressed (By Design)

The following are **explicitly out of scope**:

### 4.1 Natural Language Adversarial Attacks

- Synonym substitution
- Obfuscation
- Multi-language attacks

Mitigation belongs upstream (NLP preprocessing, tagging).

---

### 4.2 Sensor Spoofing

- False risk values
- Tampered inputs
- Misreported urgency

Requires hardware and sensor-level defenses.

---

### 4.3 Advanced ML Attacks

- Model poisoning
- Prompt injection into planners
- Jailbreaking LLMs

Guardian Seed is not an ML defense system.

---

### 4.4 Physical Sabotage

- Mechanical failure
- Power interruption
- Actuator damage

Handled via hardware safety systems.

---

## 5. Failure Modes (Accepted)

If Guardian Seed fails, it is expected to fail by:

- **Over-vetoing** (false negatives)
- Triggering fallback help
- Triggering lockdown

It must never fail by approving harm.

---

## 6. Defense-in-Depth Strategy

Guardian Seed is one layer among many:

| Layer | Responsibility |
|------|----------------|
| Hardware | Physical safety |
| Sensors | Accurate measurements |
| Planner | Task generation |
| **Guardian Kernel** | Ethical veto |
| Sentinel | Attack detection |
| Fallback | Human escalation |

No single layer is sufficient alone.

---

## 7. Summary

Guardian Seed is designed to be:

- Conservative
- Predictable
- Falsifiable
- Limited

Its power comes from **what it refuses to do**, not what it attempts.

---

**A system that admits its limits is safer than one that hides them.**
