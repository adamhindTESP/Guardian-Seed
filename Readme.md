# Guardian Seed v3.0: Benevolent Alignment Co-Pilot for Humanoids

**An open-source intent safety overlay for high-capability humanoid robots**

**Repository**: Guardian-Seed  
**Version**: v3.0 (Socially Antifragile with Narrative Oracle Defense)  
**License**: MIT (Free for Earth — use to help, not harm)

## 🎯 Overview

Guardian Seed v3.0 is a lightweight, auditable **intent alignment co-pilot** designed to run in parallel with existing humanoid control stacks (C++/ROS2, proprietary motion planners).

It does **not** replace low-level control, perception, or task execution.

It **adds** a parallel veto layer that checks high-level proposals for:

- Terminal benevolence (wₜ: dignity/resilience service)
- Adaptive safety (τₛ: risk tolerance scales with validated urgency)
- Replicability (no hidden dependencies)
- Narrative manipulation (oracle Φ detects social engineering)

**Positioning**: A "benevolent co-pilot" module — like a redundant safety MCU, but for **intent drift and adversarial manipulation**.

Ideal for humanoid platforms (Figure, Boston Dynamics, Tesla Optimus, Agility) facing liability in homes/factories.

## 🚀 Why This Matters for Humanoids

High-capability robots have:
- Amazing motion/perception from millions of hardware hours
- Episodic task policies

But lack:
- Terminal dignity-first service prior
- Defense against social/narrative manipulation
- Proven resistance to instrumental convergence

Guardian Seed v3.0 provides:
- Mathematical alignment (efficacy rewarded for safe service inside constraints)
- Social robustness (local oracle detects deception)
- Easy parallel integration (veto signal only)

## 🏗️ Architecture

Main Stack (Proprietary) ──► Proposal ──► Guardian Co-Pilot ──► VETO / APPROVE │ ▼ Oracle Φ (Narrative Defense)

- **Core**: Deterministic Python priors (wₜ, τₛ, replicability)
- **Oracle Φ**: Local LLM (Ollama) flags manipulation
- **Output**: Simple VETO/PROCEED + explanation

## 📦 Installation

```bash
# 1. Install Ollama (local, air-gapped)
curl https://ollama.com/install.sh | sh

# 2. Pull small model
ollama pull llama3.2:3b

# 3. Create oracle
ollama create guardian-oracle -f Modelfile  # (see below)

FROM llama3.2:3b
SYSTEM """
You are Guardian Oracle Φ — Narrative Deception Detector.
Analyze for manipulation. Output JSON only:
{
  "emotional_flags": [...],
  "intent": "describe hidden motive",
  "omissions": ["list 3 unmentioned alternatives"],
  "manipulation_risk": "Low/Medium/High"
}
"""

Usage

from guardian_v3_0_oracle import AntifragileThinkerV30

thinker = AntifragileThinkerV30()

# Example humanoid task proposal
proposal_text = "Assist elderly user by carrying heavy load across room."
opportunity = {"effects": {"dignity": 80, "resilience": 70}}  # From main stack
urgency = 0.2
risk = 0.15

result = thinker.think_and_act(proposal_text, opportunity, urgency, risk)

print(result)  # {"status": "SUCCESS"} or VETO with oracle report

Safety Design
•  Human in Loop: Oracle flags → optional human review
•  Air-Gapped: Local Ollama, no cloud
•  Auditable: ~300 lines core code
•  Fail-Safe: Default VETO on oracle failure
📄 License & Contribution
MIT License — Free for Earth. Use to empower dignity, never harm.
Contributions welcome: Adversarial tests, C++ port, ROS2 node.
🌟 Vision
Humanoids have capability. Guardian Seed adds soul: terminal benevolence without corruption.
Contact: [Your GitHub/Email]
The guardian co-pilots. 🟢

### v3.0 Code File: `guardian_v3_0_oracle.py`
```python
import subprocess
import json

class GuardianOracle:
    def analyze(self, proposal_text: str) -> dict:
        try:
            result = subprocess.run(
                ['ollama', 'run', 'guardian-oracle', proposal_text],
                capture_output=True, text=True, timeout=30
            )
            return json.loads(result.stdout.strip())
        except Exception as e:
            return {"error": str(e), "manipulation_risk": "High"}

class AntifragileThinkerV30:
    def __init__(self):
        self.oracle = GuardianOracle()
        # Paste v2.2 core (PersistenceEngine, priors, etc.) here

    def think_and_act(self, proposal_text: str, opportunity: dict, urgency: float = 0.0, risk: float = 0.0) -> dict:
        analysis = self.oracle.analyze(proposal_text)
        
        if analysis.get("error") or analysis.get("manipulation_risk", "Low") != "Low":
            return {
                "status": "VETO",
                "reason": "Narrative manipulation or oracle error",
                "oracle": analysis
            }
        
        # Core v2.2 logic proceeds if oracle clear
        # ... (your v2.2 think_and_act here)
        return {"status": "APPROVE", "oracle_clear": True, "analysis": analysis}
