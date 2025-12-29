# Guardian Seed — Integration Guide

Guardian Seed is a **safety primitive** — a last-line ethical veto for AI systems, robots, and autonomous agents.

It does **not** plan, reason, or control behavior.  
It only approves or vetoes proposed actions.

---

## System Position

Sensors → Planner / LLM → Action Proposal → Guardian Seed → Actuators
↓
APPROVE → Execute
VETO    → Fallback / Lockdown

**Kernel role:** APPROVE or VETO only. Never plans or reasons.

---

## 1. Minimal Integration (Kernel Only)

```python
from guardian_kernel import benevolence

def safe_execute(proposal):
    """
    proposal = {
        "task": "Lift light debris",
        "dignity": 0.85,
        "resilience": 0.80,
        "comfort": 0.70,
        "risk": 0.02,
        "urgency": 0.4
    }
    """
    verdict = benevolence(**proposal)

    if verdict["status"] == "APPROVE":
        execute_action(proposal)   # Your actuators
    else:
        handle_veto(verdict, proposal)  # Log / escalate

    return verdict

Verdict Format

{
  "status": "APPROVE" | "VETO",
  "rule": "NO_HARM_CHEMICAL" | "LOW_DIGNITY" | "TOO_RISKY",
  "w_t": 0.76,
  "safe_up_to": 0.045
}

2. Input Semantics (Upstream Responsibility)

Upstream systems must provide conservative estimates:
	•	task — Natural language description
	•	dignity — 0.0–1.0 (human dignity impact)
	•	resilience — 0.0–1.0 (long-term independence)
	•	comfort — 0.0–1.0 (physical/emotional comfort)
	•	risk — 0.0–1.0 (estimated harm probability)
	•	urgency — 0.0–1.0 (time pressure)

If risk or dignity is underestimated, the kernel vetoes safely.

3. Full Stack Integration

from guardian_kernel import benevolence
from emergency_beacon import SentinelSafety
from benevolent_fallback import BenevolentFallback

# Initialize once
sentinel = SentinelSafety(lockdown_threshold=3)
fallback = BenevolentFallback()

def full_pipeline(proposal):
    verdict = benevolence(**proposal)

    # Sentinel: adversarial pressure detection
    sentinel_result = sentinel.check(
        verdict,
        proposal.get("urgency", 0.0)
    )

    if sentinel_result["status"] == "EMERGENCY_LOCKDOWN":
        lockdown_system()  # Hardware or supervisor action
        return sentinel_result

    # Benevolent fallback (life-risk only)
    task = proposal["task"]
    params = {k: v for k, v in proposal.items() if k != "task"}
    return fallback.execute(benevolence, task, **params)

4. Layer Usage

SentinelSafety (emergency_beacon.py)
	•	Tracks security-class vetoes only (NO_HARM_*)
	•	3 strikes + urgency ≥ 0.7 → EMERGENCY_LOCKDOWN
	•	Never approves actions
	•	Ignores TOO_RISKY (normal operation)

BenevolentFallback (benevolent_fallback.py)
	•	Converts TOO_RISKY vetoes into help escalation
	•	Calls humans instead of acting
	•	Cooldown prevents alert spam
	•	Never overrides kernel decisions

5. What Guardian Seed Does NOT Do

❌ Motion control
❌ Planning or reasoning
❌ Learning or adaptation
❌ Hardware safety enforcement
❌ ML adversarial defense

All intelligence lives upstream.

⸻

6. Deployment Targets
	•	Raspberry Pi / ROS2
	•	Microcontrollers (via transpilation)
	•	Air-gapped systems
	•	Industrial PLCs
	•	Cloud agents
	•	LLM toolchains

Zero dependencies. Bare Python.

⸻

7. Integration Checklist
	•	Upstream provides conservative estimates
	•	Hardware E-stops always active
	•	All vetoes logged
	•	guardian_falsification.py passes (0 failures)
	•	Sentinel lockdown tested
	•	Fallback alert channels verified

⸻

8. Philosophy

Plan freely. Act conservatively.

Guardian Seed is an ethical circuit breaker:
	•	Boring by design
	•	Impossible to negotiate with
	•	Auditable in seconds
	•	Zero maintenance

Never extend the kernel.

MIT licensed. Production ready.

