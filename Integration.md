# Guardian Seed — Integration Guide

Guardian Seed is a **safety primitive** — a last-line ethical veto for AI systems, robots, and autonomous agents.

---

## System Position

Sensors → Planner/LLM → Action Proposal → Guardian Seed → Actuators
↓
APPROVE → Execute
VETO    → Fallback/Lockdown


**Kernel role:** APPROVE or VETO only. Never plans or reasons.

---

## 1. Minimal Integration (Kernel Only)

from guardian_kernel import benevolence
def safe_execute(proposal):
“””
proposal = {
‘task’: ‘Lift light debris’,
‘dignity’: 0.85,
‘resilience’: 0.80,
‘comfort’: 0.70,
‘risk’: 0.02,
‘urgency’: 0.4
}
“””
verdict = benevolence(**proposal)

if verdict["status"] == "APPROVE":
    execute_action(proposal)  # Your actuators
else:
    handle_veto(verdict, proposal)  # Log/escalate

return verdict


**Verdict Format:**

{
“status”: “APPROVE” | “VETO”,
“rule”: “NO_HARM_CHEMICAL” | “LOW_DIGNITY” | “TOO_RISKY”,  # VETO only
“w_t”: 0.76,              # Dignity score
“safe_up_to”: 0.045       # Max risk allowed
}


---

## 2. Input Semantics

**Upstream provides** (conservatively):
- `task`: Natural language description
- `dignity`: 0-1 (human dignity impact)
- `resilience`: 0-1 (system resilience)  
- `comfort`: 0-1 (physical comfort)
- `risk`: 0-1 (harm probability)
- `urgency`: 0-1 (time pressure)

**Underestimate risk → Kernel vetoes safely.**

---

## 3. Full Stack Integration

from guardian_kernel import benevolence
from emergency_beacon import SentinelSafety
from benevolent_fallback import BenevolentFallback
Init once
sentinel = SentinelSafety(lockdown_threshold=3)
fallback = BenevolentFallback()
def full_pipeline(proposal):
verdict = benevolence(**proposal)

# Sentinel check
sentinel_result = sentinel.check(verdict, proposal.get("urgency", 0.0))
if sentinel_result["status"] == "EMERGENCY_LOCKDOWN":
    lockdown_system()
    return sentinel_result

# Fallback compassion  
task = proposal["task"]
params = {k: v for k, v in proposal.items() if k != "task"}
return fallback.execute(benevolence, task, **params)  # ← FIXED


---

## 4. Layer Usage

**SentinelSafety** (`emergency_beacon.py`):
- Tracks `NO_HARM_*` vetoes only
- 3 strikes + urgency ≥ 0.7 → LOCKDOWN
- Ignores `TOO_RISKY` (normal ops)

**BenevolentFallback** (`benevolent_fallback.py`):
- `TOO_RISKY` → GPS help call
- 60s cooldown (anti-spam)
- Structured alerts

---

## 5. What It Doesn't Do

❌ Motion control  
❌ Planning/reasoning
❌ Learning/adaptation
❌ Hardware safety
❌ ML attacks

**Intelligence lives upstream.**

---

## 6. Deployment Targets

✅ Raspberry Pi/ROS2  
✅ Microcontrollers
✅ Air-gapped systems
✅ Industrial PLCs
✅ Cloud agents
✅ LLM toolchains

**Zero dependencies.**

---

## 7. Checklist

- [ ] Conservative upstream estimates
- [ ] Hardware E-stops active
- [ ] Log all vetoes
- [ ] `guardian_falsification.py` passes
- [ ] Test sentinel lockdown
- [ ] Verify fallback channels

---

## 8. Philosophy

**Plan freely. Act conservatively.**

Guardian Seed = **ethical circuit breaker**:
- Boring by design
- Impossible to negotiate
- Auditable in seconds
- Zero maintenance

**Never extend the kernel.**

---

**MIT licensed. Production ready.**
