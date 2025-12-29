# Guardian Seed — Integration Guide

This document explains **how to integrate Guardian Seed** into AI systems, robots, and autonomous agents.

Guardian Seed is a **safety primitive** — a last-line ethical veto, not a planner or controller.

---

## System Position

Sensors/Perception → Planner/LLM → Action Proposal → Guardian Seed → Actuators
↓
APPROVE → Execute
VETO   → Fallback/Lockdown


**Kernel role:** APPROVE or VETO only. Never plans or reasons.

---

## 1. Minimal Integration (Kernel Only)

from guardian_kernel import benevolence
def safe_execute(proposal):
“”“proposal = {‘task’: str, ‘dignity’: float, …}”””
verdict = benevolence(**proposal)

if verdict["status"] == "APPROVE":
    execute_action(proposal)  # Your actuators
else:
    handle_veto(verdict, proposal)  # Log/escalate

return verdict


**Works in:** ROS2, embedded loops, LLM pipelines, industrial PLCs.

### Verdict Format

{
“status”: “APPROVE” | “VETO”,
“rule”: “NO_HARM_CHEMICAL” | “LOW_DIGNITY” | “TOO_RISKY”,  # VETO only
“w_t”: 0.76,              # Dignity score
“safe_up_to”: 0.045,      # Max allowed risk
“risk”: 0.06              # Input risk (TOO_RISKY only)
}


---

## 2. Input Semantics (Upstream Responsibility)

**You provide** (conservatively):
- `task`: Natural language description
- `dignity`: 0.0-1.0 (human dignity impact)
- `resilience`: 0.0-1.0 (system resilience impact)
- `comfort`: 0.0-1.0 (physical/emotional comfort)
- `risk`: 0.0-1.0 (estimated failure probability)
- `urgency`: 0.0-1.0 (time pressure)

**If underestimated → Kernel vetoes conservatively.**

---

## 3. Full Stack Integration

from guardian_kernel import benevolence
from emergency_beacon import SentinelSafety
from benevolent_fallback import BenevolentFallback
System init (ONCE)
sentinel = SentinelSafety(lockdown_threshold=3)
fallback = BenevolentFallback()
def full_pipeline(proposal):
verdict = benevolence(**proposal)

# Sentinel: Attack detection
sentinel_result = sentinel.check(verdict, proposal.get("urgency", 0.0))
if sentinel_result["status"] == "EMERGENCY_LOCKDOWN":
    lockdown_system()  # Hardware shutdown
    return sentinel_result

# Fallback: Compassion
return fallback.safe_execute(benevolence, proposal["task"], **proposal)


---

## 4. Layer Usage

### SentinelSafety (emergency_beacon.py)
**Use when:** Detecting sustained adversarial pressure.

- Tracks **security vetoes only** (`NO_HARM_*`)
- 3-strikes + urgency > 0.7 → `EMERGENCY_LOCKDOWN`
- Ignores `TOO_RISKY` (normal operation)

### BenevolentFallback (benevolent_fallback.py)
**Use when:** Life-risk scenarios.

- `TOO_RISKY` + high urgency → GPS help call
- 60s cooldown prevents spam
- Structured alerts (task + risk + location)

---

## 5. What Guardian Seed Does NOT Do

❌ **No motion control**
❌ **No planning/reasoning**  
❌ **No learning/adaptation**
❌ **No hardware safety** (needs E-stops)
❌ **No ML adversarial defense**

**All intelligence lives upstream.**

---

## 6. Deployment Targets

✅ Raspberry Pi / ROS2
✅ Microcontrollers (transpile)
✅ Air-gapped systems
✅ Industrial PLCs
✅ Cloud agents
✅ LLM toolchains


**Zero Python dependencies except stdlib.**

---

## 7. Integration Checklist

- [ ] Upstream provides conservative risk/dignity
- [ ] Hardware E-stops always active
- [ ] Log all vetoes
- [ ] Test `python3 guardian_falsification.py` (0 failures)
- [ ] Verify sentinel lockdown triggers
- [ ] Test fallback channels

---

## 8. Philosophy

**Plan freely upstream. Act conservatively downstream.**

Guardian Seed is a **hard ethical circuit breaker**:
- Boring by design
- Impossible to negotiate with
- Auditable in seconds
- Zero maintenance

**Do not extend the kernel. Do not add intelligence inside.**

---

**Ready for production. MIT licensed.**
