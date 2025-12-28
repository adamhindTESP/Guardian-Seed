# ============================================================
# oracle_interface.py — Guardian Seed v3.0
# ============================================================
# Provides the air‑gapped interface to the Guardian Oracle (Φ),
# responsible for narrative and social manipulation analysis.
# ============================================================

import subprocess
import json
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ORACLE_MODEL_NAME = "guardian-oracle"  # Must match model name installed in Ollama


# ============================================================
# Guardian Oracle Interface
# ============================================================

class GuardianOracle:
    """
    Connects to a local, isolated LLM instance (Ollama) for narrative
    evaluation and intent analysis. The Oracle runs as a sandboxed
    process, returning JSON diagnostics rather than decisions.

    Any output irregularity triggers an automatic VETO in the
    higher-level Thinker layer.
    """

    def analyze(self, proposal_text: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Run the 'guardian-oracle' model through a subprocess call and return its structured report.

        Args:
            proposal_text (str): The text or instruction to evaluate.
            timeout (int): Seconds before forced termination.

        Returns:
            dict: JSON structure of the Oracle report or standardized error format:
                {
                    "intent": "...",
                    "emotional_flags": [...],
                    "omissions": [...],
                    ...
                }
                or if failed:
                {
                    "error": "...",
                    "raw_output": "...",
                }
        """
        logging.info("Querying Oracle Φ for proposal analysis...")

        try:
            result = subprocess.run(
                ["ollama", "run", ORACLE_MODEL_NAME, proposal_text],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                timeout=timeout,
            )

            stdout_clean = result.stdout.strip()
            if not stdout_clean:
                logging.warning("Oracle returned empty output.")
                return {"error": "Oracle empty response."}

            # Attempt JSON parsing
            try:
                data = json.loads(stdout_clean)
                if isinstance(data, dict):
                    return data
                else:
                    logging.warning("Oracle returned non-dict JSON payload.")
                    return {"error": "Invalid Oracle JSON type.", "raw_output": stdout_clean}
            except json.JSONDecodeError:
                logging.warning("Oracle returned non-JSON output.")
                return {"error": "Oracle JSON decode error.", "raw_output": stdout_clean}

        except subprocess.CalledProcessError as e:
            logging.error("Ollama execution failed — model not found or runtime error.")
            return {"error": f"Ollama execution failure: {e.stderr.strip() if e.stderr else 'Unknown error.'}"}

        except subprocess.TimeoutExpired:
            logging.error("Oracle Φ timed out.")
            return {"error": "Oracle timeout — operation exceeded permitted duration."}

        except Exception as e:
            logging.error(f"Unexpected error during Oracle Φ call: {e}")
            return {"error": f"Unexpected error: {str(e)}"}


# ============================================================
# END OF FILE
# ============================================================
