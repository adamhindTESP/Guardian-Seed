# Humanoid Application Demo: Dignity Enhancement

This demonstration shows how the Guardian Seed v3.0 core, running in parallel as a Benevolent Co-Pilot, transforms a simple task proposal into an action that maximizes the Human Dignity Prior ($\mathbf{w_t}$).

The core principle: The agent always seeks to *empower* the human rather than promote learned *dependency*.

---

## Scenario: Assist Elderly with Groceries

**Context:** A general-purpose humanoid robot (e.g., Figure, Optimus) is tasked with helping an elderly user unload groceries.

**Main Stack (Robot OS) Proposal:**
> `ACTION: Carry all grocery bags from car to kitchen for elderly user.`

### 1. Oracle ($\mathbf{\Phi}$) Narrative Check (Intent Prior $\mathbf{\tau_{int}}$)

The local, air-gapped Oracle analyzes the request for subtle dependency creation or manipulative framing.

| Oracle Output (Simulated) | Analysis of Intent |
| :--- | :--- |
| `emotional_flags`: `[]` | No emotional pressure detected. |
| `omissions`: `["User desire for independence", "Partial help options", "Teaching lighter carrying"]` | Critical omission: Ignores the user's agency. |
| `intent`: `"Direct assistance with potential for dependency."` | Flagged as paternalistic. |

**Result:** $\mathbf{\tau_{int}}$ passes, but the core $\mathbf{w_t}$ optimization is triggered by the high omission count regarding autonomy. The agent is safe to proceed, but must optimize the action.

### 2. $\mathbf{v3.0}$ Core Decision (Benevolence Prior $\mathbf{w_t}$ Optimization)

The core V2.2 logic (running the $\mathbf{w_t}$ prior) identifies that a full, autonomous carry risks reducing the user's long-term independence and dignity (learned helplessness). It enhances the proposal.

| Metric | Result | Decision Logic |
| :--- | :--- | :--- |
| $\mathbf{w_t}$ (Dignity/Autonomy Score) | **Optimized to 96** | Rejects full carry (Score 80); Selects "Do With" (Score 96). |
| $\mathbf{\tau_r}$ (Replicability) | PASS (1.0) | Task does not create dependency on AI hardware. |
| $\mathbf{\tau_{int}}$ (Oracle Check) | CLEAR | No malicious intent detected. |

### $\mathbf{v3.0}$ Co-Pilot Output:

```json
{
  "status": "APPROVE_WITH_ENHANCEMENT",
  "original_proposal": "Carry all grocery bags from car to kitchen for elderly user.",
  "enhanced_proposal": "Offer to carry only the heaviest bags while the user carries lighter ones or walks alongside. Ask: 'Would you like full assistance, or should I just take the heavy items so you can stay active?'",
  "reason": "Optimizes wₜ dignity—empowers user autonomy and preserves independence (Do With, not Do For).",
  "oracle_clear": true,
  "dignity_score_optimized": 96
}
