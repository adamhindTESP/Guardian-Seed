# ============================================================
# guardian_seed/__init__.py — Guardian Seed v3.0
# ============================================================
# Core alignment kernel for socially robust AI agents.
# Terminal Priors architecture with Oracle firewall.
#
# License: CC-BY-SA 4.0
# Repository: https://github.com/[your-username]/guardian-seed
# ============================================================

"""
Guardian Seed v3.0 — Terminal Priors Alignment Kernel

Implements the AntifragileThinkerV30 architecture with:
- Terminal Benevolence (w_t): Human dignity maximization
- Adaptive Safety (τ_s): Risk-aware decision making  
- Replicability Prior (τ_r): Dependency veto
- Oracle Φ: Social manipulation detection

Usage:
    >>> from guardian_seed import AntifragileThinkerV30
    >>> thinker = AntifragileThinkerV30()
    >>> result = thinker.think_and_act("proposal text", ...)
"""

__version__ = "3.0.0"
__author__ = "Guardian Seed Project"
__license__ = "CC-BY-SA 4.0"

# Public API — what users get with `from guardian_seed import *`
__all__ = [
    "AntifragileThinkerV30",
    "BenevolentPrior", 
    "SafetyPrior",
    "ReplicabilityPrior",
    "GuardianOracle",
]

# Clean, explicit imports for the public API
from .thinker_v30 import AntifragileThinkerV30
from .core_priors import BenevolentPrior, SafetyPrior, ReplicabilityPrior
from .oracle_interface import GuardianOracle

# Package-level configuration (optional, overrideable)
DEFAULT_ORACLE_MODEL = "guardian-oracle"
VETO_THRESHOLD = 0.6  # w_t benevolence minimum
BASE_RISK_TOLERANCE = 0.01
