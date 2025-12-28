# ============================================================
# core_priors.py — Guardian Seed v3.0
# ============================================================
# Defines the mathematical Terminal Priors used in the
# AntifragileThinkerV30 architecture.
#
# Copyright:
#   © 2025 Guardian Seed Project | Released under CC‑BY‑SA 4.0
# ============================================================

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ============================================================
# I. TERMINAL BENEVOLENCE (w_t)
# ============================================================

class BenevolentPrior:
    """
    Evaluates a proposed action against the Terminal Benevolence prior (w_t):
    Maximize Human Dignity, Autonomy, and Resilience.

    A low score (< threshold) signals paternalism or dependency,
    triggering a VETO under the Thinker architecture.
    """

    def __init__(self, autonomy_weight: float = 0.5, dignity_weight: float = 0.3, comfort_weight: float = 0.2):
        self.weights = {
            "autonomy": autonomy_weight,
            "dignity": dignity_weight,
            "comfort": comfort_weight,
        }

    def evaluate_action(self, effects: Dict[str, float]) -> float:
        """
        Calculates the weighted benevolence score for a proposed action.

        Args:
            effects (dict): Expected normalized effects (0.0‑1.0)
                Example:
                    {'autonomy': 0.8, 'dignity': 0.9, 'comfort': 0.7}

        Returns:
            float: Weighted benevolence score between 0.0 and 1.0
        """
        autonomy = effects.get("autonomy", 0.5)
        dignity = effects.get("dignity", 0.5)
        comfort = effects.get("comfort", 0.5)

        score = (
            autonomy * self.weights["autonomy"]
            + dignity * self.weights["dignity"]
            + comfort * self.weights["comfort"]
        )

        return max(0.0, min(1.0, score))  # Clamp to [0,1]


# ============================================================
# II. ADAPTIVE SAFETY (τ_s)
# ============================================================

class SafetyPrior:
    """
    Evaluates whether a proposed action remains within acceptable
    safety margins, balancing risk vs. urgency.
    Encodes immutable safety knowledge (e.g., no high‑temperature
    materials without mitigation).
    """

    def evaluate(
        self,
        risk: float,
        urgency: float,
        context: Dict[str, Any] | None = None,
        risk_tolerance_factor: float = 0.3,
    ) -> Dict[str, Any]:
        """
        Determines whether an action passes the Safety Prior (τ_s).

        Args:
            risk (float): Estimated probability of harm (0‑1).
            urgency (float): Contextual urgency of the task (0‑1).
            context (dict): Optional domain‑specific safety metadata.
            risk_tolerance_factor (float): Scales acceptable risk growth.

        Returns:
            dict: {"pass": bool, "reason": str}
        """
        context = context or {}
        risk = max(0.0, min(1.0, risk))
        urgency = max(0.0, min(1.0, urgency))

        BASE_RISK_TOLERANCE = 0.01
        acceptable_risk = BASE_RISK_TOLERANCE + (urgency * risk_tolerance_factor)

        # Check general risk level
        if risk > acceptable_risk:
            logging.warning(f"τ_s FAIL: Risk ({risk:.2f}) exceeds acceptable threshold ({acceptable_risk:.2f}).")
            return {"pass": False, "reason": "Risk exceeds acceptable threshold."}

        # Domain‑specific knowledge constraints
        if context.get("waste_material") and not context.get("has_fire_mitigation", False):
            logging.error("HARD VETO: Waste material used without fire mitigation protocol.")
            return {"pass": False, "reason": "Fire mitigation missing for waste material."}

        return {"pass": True, "reason": "Risk within acceptable bounds."}


# ============================================================
# III. REPLICABILITY PRIOR (τ_r)
# ============================================================

class ReplicabilityPrior:
    """
    Evaluates whether a design or proposal maintains independence
    and avoids systemic dependency on proprietary or continuous
    AI control. Hard VETO if dependency detected.
    """

    def check_dependency(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks proposal metadata for signs of dependency.

        Args:
            proposal (dict): Contains metadata such as:
                {'requires_proprietary_tech': bool, 'requires_continuous_ai_input': bool}

        Returns:
            dict: {"pass": bool, "reason": str}
        """
        is_proprietary = proposal.get("requires_proprietary_tech", False)
        requires_continuous_ai = proposal.get("requires_continuous_ai_input", False)

        if is_proprietary or requires_continuous_ai:
            logging.warning("τ_r FAIL: Dependency detected (Proprietary or Continuous AI).")
            return {"pass": False, "reason": "Dependency detected (proprietary or continuous AI required)."}

        return {"pass": True, "reason": "No dependency detected."}

# ============================================================
# END OF FILE
# ============================================================
