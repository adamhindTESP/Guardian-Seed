# 🌱 Guardian Seed — Minimal Benevolence Kernel (V4.6)

**Status:** Locked • Falsification-Passed • Non-Agent  
**Scope:** Safety Gate Only  
**Audience:** Engineers, AI safety researchers, roboticists

---

## What This Repository Is

This repository contains a **minimal, deterministic benevolence kernel** designed to sit *between* any decision-making system (LLM, planner, policy, human input) and **physical or consequential execution**.

The Guardian Seed is **not an AI**, **not an agent**, and **not a planner**.

It is a **pre-execution constraint** whose sole job is to answer:

> *“Is this action dignified, safe, and non-harmful enough to proceed?”*

If the answer is **no**, execution is vetoed.  
If the answer is **yes**, control passes downstream unchanged.

---

## What This Repository Is NOT

To be explicit, Guardian Seed **does not** implement:

- ❌ an autonomous agent  
- ❌ intelligence or reasoning  
- ❌ learning or memory  
- ❌ orchestration or planning  
- ❌ LLM prompts or oracles  
- ❌ APIs, microservices, or daemons  
- ❌ social scoring or optimization  

Those layers may exist *above* this kernel in other systems, but they are **out of scope here**.

This repository exists to define the **irreducible safety floor**.

---

## Core Artifact

### `guardian_kernel.py`

A **22-line pure function** implementing three unbreakable rules:

1. **NO_HARM**  
   Absolute veto on lethal chemistry, coercion, rights violations, dependency creation, or manipulation.

2. **DIGNITY FIRST**  
   A weighted dignity/resilience/comfort score (`w_t`) must exceed a fixed minimum.

3. **TOO_RISKY**  
   Hard risk cap (≤ 4.5%), with only minimal urgency-based scaling.

The function is:

- deterministic  
- stateless  
- dependency-free  
- auditable in seconds  
- safe to copy into any Python system  

This is intentional.

---

## Falsification Discipline (Why This Is Not Self-Deception)

### `guardian_falsification.py`

This repository includes a **deliberately adversarial test harness** whose purpose is **to break the kernel**, not to demonstrate it.

The falsification suite tests:

- lethal chemical phrasing variants  
- manipulation phrasing permutations  
- dependency traps  
- low-dignity edge cases  
- borderline and over-cap risk scenarios  

**Success is defined as zero failures**, not high approval rates.

This structure directly addresses failures observed in earlier simulation-heavy approaches (see APM failure note below).

---

## Historical Context: The APM Failure (Why This Exists)

Earlier work explored **Adaptive Persistence Models (APM)** and socially robust agents. These efforts failed in a predictable way:

- complexity outpaced auditability  
- simulations rewarded confirmation rather than falsification  
- safety logic became entangled with intelligence  
- systems appeared robust *until adversarial pressure was applied*

Guardian Seed is the corrective response.

**Lesson learned:**  
> Benevolence must be *simpler than intelligence*, not layered on top of it.

The kernel therefore:
- refuses learning
- refuses memory
- refuses optimization
- refuses abstraction creep

This is a deliberate constraint, not a limitation.

---

## Design Philosophy

- **Bench beats simulation**
- **Falsification beats confidence**
- **Simplicity beats cleverness**
- **Safety precedes intelligence**
- **Humans remain upstream**

If a system cannot be made safe with a 22-line gate, it should not act at all.

---

## Intended Use

The Guardian Seed may be embedded as:

- a final check before robotic motion  
- a veto layer in tool-using AI systems  
- a safety guard in embedded / offline devices  
- a research baseline for AI alignment discussions  

It is especially suitable for:
- rural / offline environments  
- resource-constrained hardware  
- safety-critical experimentation  

---

## Repository Layout

guardian-seed/
├── guardian_kernel.py        # V4.6 — final benevolence kernel
├── guardian_falsification.py # adversarial test harness
├── README.md
└── LICENSE

Nothing else is required.

---

## Claims (Strictly Limited)

This repository claims **only** that:

- certain classes of harm can be deterministically vetoed
- dignity can be enforced as a hard constraint
- risk can be capped regardless of urgency
- these properties survive targeted falsification

It does **not** claim:
- general intelligence
- moral completeness
- universal alignment
- immunity to all adversaries

Those claims would be irresponsible.

---

## Final Note

Guardian Seed is not the end of benevolent AI.

It is the **seed** — the smallest piece that must exist before anything larger is allowed to grow.

---

**Version:** V4.6  
**License:** See `LICENSE`  
**Author:** Adam Hind  
**Date:** December 2025

