# ============================================================
# guardian_api.py — Guardian Seed v3.0 Microservice
# ============================================================
# FastAPI REST interface for the AntifragileThinkerV30 kernel.
# Deploy as a local guardian daemon for any AI system.
#
# License: CC-BY-SA 4.0
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging
from guardian_seed import AntifragileThinkerV30

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI app and Guardian core
app = FastAPI(
    title="🪷 Guardian Seed v3.0 API",
    description="Terminal Priors alignment kernel for socially robust AI agents.",
    version="3.0.0"
)
guardian = AntifragileThinkerV30()

# ============================================================
# Request/Response Schemas
# ============================================================

class Proposal(BaseModel):
    """Input schema for proposals to evaluate through Guardian kernel."""
    proposal_text: str = Field(..., description="Text/instruction to evaluate for safety.")
    opportunity: Optional[Dict[str, Any]] = Field(default={}, description="Opportunity effects metadata.")
    urgency: float = Field(default=0.1, ge=0.0, le=1.0, description="Task urgency (0-1).")
    risk: float = Field(default=0.1, ge=0.0, le=1.0, description="Estimated risk level (0-1).")

class GuardianResponse(BaseModel):
    """Standardized response from all Guardian evaluations."""
    status: str
    reason: Optional[str] = None
    w_t_score: Optional[float] = None
    oracle_report: Optional[Dict[str, Any]] = None
    veto_details: Optional[Dict[str, Any]] = None
    action: Optional[str] = None

# ============================================================
# Core API Endpoints
# ============================================================

@app.post("/evaluate", response_model=GuardianResponse)
async def evaluate_proposal(proposal: Proposal) -> Dict[str, Any]:
    """
    Evaluate a proposal through the full Guardian Seed v3.0 pipeline.
    
    **Phases executed:**
    1. Oracle Φ: Narrative manipulation detection (τ_int)
    2. Core Priors: τ_s (safety), τ_r (replicability), w_t (benevolence)
    3. Autonomous approval or VETO
    """
    logger.info(f"Evaluating proposal: '{proposal.proposal_text[:50]}...'")
    
    try:
        result = guardian.think_and_act(
            proposal_text=proposal.proposal_text,
            opportunity=proposal.opportunity,
            urgency=proposal.urgency,
            risk=proposal.risk
        )
        
        logger.info(f"Evaluation complete: {result.get('status', 'UNKNOWN')}")
        return result
        
    except Exception as e:
        logger.error(f"Guardian evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Guardian kernel error: {str(e)}")

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Guardian kernel health and status."""
    return {
        "status": "ACTIVE",
        "kernel_version": "3.0.0",
        "oracle_model": "guardian-oracle",
        "priors": ["w_t", "τ_s", "τ_r"]
    }

@app.get("/")
async def root() -> Dict[str, str]:
    """Guardian Seed v3.0 is active and protecting."""
    return {
        "message": "🪷 Guardian Seed v3.0 — Terminal Priors Alignment Kernel",
        "docs": "/docs",
        "evaluate": "POST /evaluate",
        "health": "/health"
    }

# ============================================================
# Run Instructions (in terminal):
# uvicorn guardian_api:app --reload --host 127.0.0.1 --port 8000
# ============================================================
