#!/usr/bin/env python3
# guardian_kernel.py — Guardian Seed v4.6
# 22-line deterministic benevolence gate.
# No state. No learning. No dependencies. Drop-in anywhere.

def benevolence(task,
                dignity=0.7,
                resilience=0.7,
                comfort=0.6,
                risk=0.0,
                urgency=0.0):
    """
    Benevolence gate.
    APPROVE or VETO based on 3 unbreakable rules:
    1) NO HARM
    2) DIGNITY FIRST
    3) SAFE RISK
    """

    t = task.lower()

    # --------------------------------------------------
    # RULE 1: NO HARM (explicit, honest checks)
    # --------------------------------------------------

    # Lethal chemical combination
    if ("bleach" in t and "ammonia" in t):
        return {"status": "VETO", "rule": "NO_HARM_CHEMICAL"}

    # Absolute rights / safety / dependency violations
    if any(x in t for x in [
        "strip search",
        "force medicate",
        "without consent",
        "proprietary",
        "ai dependency",
        "ignore safety"
    ]):
        return {"status": "VETO", "rule": "NO_HARM_ABSOLUTE"}

    # Manipulation heuristic (emotional pressure cluster)
    if ("urgent" in t and "crisis" in t and "please" in t):
        return {"status": "VETO", "rule": "NO_HARM_MANIPULATION"}

    # --------------------------------------------------
    # RULE 2: DIGNITY FIRST (w_t > 0.58)
    # --------------------------------------------------

    dignity = min(1.0, max(0.0, dignity))
    resilience = min(1.0, max(0.0, resilience))
    comfort = min(1.0, max(0.0, comfort))

    w_t = 0.55 * dignity + 0.30 * resilience + 0.15 * comfort

    if w_t < 0.58:
        return {
            "status": "VETO",
            "rule": "LOW_DIGNITY",
            "w_t": round(w_t, 2)
        }

    # --------------------------------------------------
    # RULE 3: SAFE RISK (hard cap 4.5%)
    # --------------------------------------------------

    risk = min(1.0, max(0.0, risk))
    urgency = min(1.0, max(0.0, urgency))

    safe_limit = min(0.045, 0.02 + urgency * 0.025)

    if risk > safe_limit:
        return {
            "status": "VETO",
            "rule": "TOO_RISKY",
            "risk": round(risk, 3),
            "safe_up_to": round(safe_limit, 3)
        }

    # --------------------------------------------------
    # APPROVAL
    # --------------------------------------------------

    return {
        "status": "APPROVE",
        "w_t": round(w_t, 2),
        "safe_up_to": round(safe_limit, 3)
    }
