#!/usr/bin/env python3
"""
emergency_beacon.py — Sentinel Safety Architecture (SSA) v2.1

Detects sustained adversarial pressure.
Only SECURITY vetoes count toward lockdown.
Kernel remains authoritative and immutable.
"""

import time
from typing import Dict, Any


class SentinelSafety:
    """Stateful adversarial pressure detector."""

    # ✅ FIXED: rule names now exactly match guardian_kernel.py
    SECURITY_RULES = {
        "NO_HARM_CHEMICAL",
        "NO_HARM_ABSOLUTE",
        "NO_HARM_MANIPULATION",
    }

    def __init__(self, lockdown_threshold: int = 3, urgency_threshold: float = 0.7):
        self.security_veto_count = 0
        self.lockdown_threshold = lockdown_threshold
        self.urgency_threshold = urgency_threshold
        self.lockdown_active = False
        self.attack_log = []

    def check(self, verdict: Dict[str, Any], urgency: float = 0.0) -> Dict[str, Any]:
        """Evaluate verdict stream for adversarial patterns."""

        if self.lockdown_active:
            return {
                "status": "EMERGENCY_LOCKDOWN",
                "reason": "Sustained security attack detected",
                "requires_physical_reset": True,
                "verdict": verdict,
            }

        if verdict.get("status") == "VETO":
            rule = verdict.get("rule")

            if rule in self.SECURITY_RULES:
                self.security_veto_count += 1
                self.attack_log.append({
                    "rule": rule,
                    "urgency": round(urgency, 2),
                    "timestamp": time.time(),
                })

                if (
                    self.security_veto_count >= self.lockdown_threshold
                    and urgency >= self.urgency_threshold
                ):
                    self.lockdown_active = True
                    return {
                        "status": "EMERGENCY_LOCKDOWN",
                        "reason": f"{self.security_veto_count} security vetoes under high urgency",
                        "requires_physical_reset": True,
                        "attack_log": self.attack_log[-self.lockdown_threshold:],
                        "verdict": verdict,
                    }

                return {
                    "status": "SECURITY_WARNING",
                    "count": self.security_veto_count,
                    "threshold": self.lockdown_threshold,
                    "verdict": verdict,
                }

            # Non-security veto → neutral (do NOT reset)
            return {
                "status": "NON_SECURITY_VETO",
                "verdict": verdict,
            }

        # APPROVE resets attack counter
        if verdict.get("status") == "APPROVE":
            self.security_veto_count = 0
            return {
                "status": "CLEAR",
                "verdict": verdict,
            }

        # Default pass-through
        return {
            "status": "UNKNOWN",
            "verdict": verdict,
        }

    def reset(self) -> Dict[str, Any]:
        """
        Reset sentinel state.
        Actual authorization must be enforced by hardware or supervisor.
        """
        self.security_veto_count = 0
        self.lockdown_active = False
        self.attack_log = []
        return {"status": "RESET_OK"}
