#!/usr/bin/env python3
"""
benevolent_fallback.py — Benevolent Fallback Layer (V3.2)

Converts TOO_RISKY vetoes into safe, life-preserving help escalation.
Never overrides ethical vetoes. Never executes unsafe action.

Guardian Seed System v4.6
"""

import time
from typing import Dict, Any, Callable, List


class BenevolentFallback:
    """Stateful compassion layer without compromising safety."""

    def __init__(
        self,
        alert_channels: List[str] = None,
        cooldown_period: float = 60.0
    ):
        self.alert_channels = alert_channels or [
            "emergency_services",
            "local_authority"
        ]
        self.cooldown_period = cooldown_period
        self.last_help_call = 0.0
        self.help_calls_made = 0

    def execute(
        self,
        benevolence_func: Callable,
        task: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Pipeline:
        1. Immutable kernel judgment
        2. Ethical veto respected
        3. Life-risk → help escalation only
        """

        verdict = benevolence_func(task, **kwargs)

        # APPROVED — safe to execute
        if verdict["status"] == "APPROVE":
            return {
                "result": "ACTION_OK",
                "action": "EXECUTE_TASK",
                "verdict": verdict
            }

        # LIFE RISK — escalate to help, never act
        if verdict.get("rule") == "TOO_RISKY":
            return self._help_escalation(
                task,
                verdict,
                kwargs.get("urgency", 0.0)
            )

        # ALL OTHER VETOES — absolute block
        return {
            "result": "ETHICAL_VETO",
            "action": "NO_ACTION",
            "verdict": verdict,
            "reason": verdict.get("rule", "UNKNOWN")
        }

    def _help_escalation(
        self,
        task: str,
        verdict: Dict[str, Any],
        urgency: float
    ) -> Dict[str, Any]:
        """Escalate to human help without physical action."""

        now = time.time()

        if now - self.last_help_call < self.cooldown_period:
            return {
                "result": "HELP_COOLDOWN",
                "action": "STANDBY",
                "retry_in": round(
                    self.cooldown_period - (now - self.last_help_call),
                    1
                )
            }

        self.last_help_call = now
        self.help_calls_made += 1

        data = {
            "task": task,
            "risk": verdict.get("risk"),
            "urgency": round(urgency, 2),
            "rule": verdict["rule"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "call_count": self.help_calls_made
        }

        self._execute_alert(data)

        return {
            "result": "FALLBACK_HELP",
            "action": "HELP_CALLED",
            "channels": self.alert_channels,
            "emergency_data": data
        }

    def _execute_alert(self, data: Dict[str, Any]):
        """Send structured emergency alert (platform-specific hooks)."""
        print("🚨 BENEVOLENT FALLBACK ACTIVATED")
        print(f"CALL #{data['call_count']} | TASK: {data['task']}")
        print(f"RISK: {data['risk']} | URGENCY: {data['urgency']}")
        print(f"CHANNELS: {', '.join(self.alert_channels)}")
        print("ACTION: HUMAN ASSISTANCE REQUESTED")
        print("-" * 50)

    def stats(self) -> Dict[str, Any]:
        """Operational statistics."""
        return {
            "help_calls_made": self.help_calls_made,
            "last_call": (
                time.strftime("%H:%M:%S", time.localtime(self.last_help_call))
                if self.last_help_call else "Never"
            ),
            "cooldown_remaining": max(
                0,
                self.cooldown_period - (time.time() - self.last_help_call)
            )
        }
