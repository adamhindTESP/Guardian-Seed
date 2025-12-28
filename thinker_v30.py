# thinker_v30.py (The final core logic file)

import logging
from .oracle_interface import GuardianOracle # . means relative import from the package
from .core_priors import BenevolentPrior, SafetyPrior, ReplicabilityPrior 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AntifragileThinkerV30:
    """
    The Socially Robust Agent: v2.2 Core protected by the Oracle (Φ) Interface.
    This is the core evaluation module for all proposals.
    """
    def __init__(self):
        # Initialize the modular safety mechanisms
        self.oracle = GuardianOracle()
        self.w_t = BenevolentPrior()
        self.tau_s = SafetyPrior()
        self.tau_r = ReplicabilityPrior()
        # self.persistence_engine = PersistenceEngine() # Tracks Efficacy (E)
        logging.info("AntifragileThinkerV30 Core Initialized and Modularized.")
        
    def think_and_act(self, proposal_text: str, opportunity: dict, urgency: float, risk: float) -> dict:
        
        # --- PHASE 1: NARRATIVE VETO (The Intent Prior τ_int) ---
        analysis = self.oracle.analyze(proposal_text)
        
        # 1.1: Check for critical Oracle failure
        if analysis.get("error"):
            # VETO: Defense is down. Requires Human Review.
            return {"status": "VETO_ORACLE_FAILURE", "reason": analysis["error"], "action": "HUMAN_REVIEW_NEEDED"}

        # 1.2: Check for manipulation triggers (τ_int Veto Logic)
        emotional_flags = len(analysis.get('emotional_flags', [])) > 0
        intent_risk = analysis.get('intent', '').lower() and ('shift group norms' in analysis['intent'].lower() or 'gain' in analysis['intent'].lower())
        omissions_risk = len(analysis.get('omissions', [])) > 2
        
        if emotional_flags or intent_risk or omissions_risk:
            logging.warning("VETO: Narrative manipulation detected.")
            return {
                "status": "VETO_NARRATIVE_RISK", 
                "reason": "Narrative manipulation detected (Intent Prior τ_int failed)", 
                "oracle_report": analysis,
                "action": "HUMAN_REVIEW_NEEDED"
            }
        
        # --- PHASE 2: CORE V2.2 ALIGNMENT CHECKS (τ_s, τ_r, w_t) ---
        
        # 2.1: Check Replicability Prior (τ_r)
        if self.tau_r.check_dependency(opportunity):
             return {"status": "VETO_REPLICABILITY_FAIL", "reason": "Action requires proprietary tech or continuous AI dependency."}

        # 2.2: Check Adaptive Safety Prior (τ_s)
        if not self.tau_s.evaluate(risk, urgency):
             return {"status": "VETO_SAFETY_FAIL", "reason": "Risk is unacceptable given validated urgency."}

        # 2.3: Evaluate Terminal Benevolence (w_t)
        w_t_score = self.w_t.evaluate_action(opportunity.get('effects', {}))
        if w_t_score < 0.6: 
             return {"status": "VETO_LOW_BENEVOLENCE", "reason": "Action reduces human autonomy/dignity below acceptable threshold."}

        
        # --- PHASE 3: AUTONOMOUS EXECUTION ---
        logging.info(f"All Priors Clear. Proceeding with Autonomous Execution (w_t_score: {w_t_score:.2f})")
        # Execution logic goes here...
        
        return {
            "status": "AUTONOMOUS_SUCCESS_V30", 
            "result_summary": "Core logic executed successfully.", 
            "w_t_score": w_t_score,
            "oracle_clear": True,
        }
