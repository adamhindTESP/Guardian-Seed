Guardian Seed v4.6.0 — Immutable, non-bypassable safety enforcement for physically embodied AI. Raspberry Pi 5 production-ready. No warnings. No compromises.
🎯 Core Architecture
The system is built on an unbreakable Fail-Closed principle: any failure, compromise, or ambiguity in the untrusted Planner component results in a VETO or immediate Emergency Stop.
Sensors → Planner (Untrusted LLM) → RiskCalc → Guardian (Immutable IPC) → Hardware (Constrained)
                              ↓ VETO? → Halt or Fallback

🛡️ Core Safety Guarantees
| Component | Purpose | Safety Mechanism |
|---|---|---|
| Guardian | The deterministic Veto Engine. | Process Isolation (IPC), Fail-Closed guaranteed response, Heartbeat monitoring. |
| Integrity | Kernel Source Verification. | SHA-256 integrity hash stored on first boot. Any file change aborts startup. |
| HardwareLayer | Motor/Sensor Abstraction. | Rolling Time Window (max 30s move/60s), max 30% speed, 0.5s move cooldowns, GPIO cleanup on shutdown. |
| Main Loop | Orchestration/State. | Consecutive Veto Counter (3 misses → Safe Mode + E-Stop). State persistence for audit. |
| Planner | Generates Action Proposals. | Untrusted—must pass Guardian veto; executed in Docker sandbox. |
🔒 Veto and Isolation Details
1. Guardian IPC (Inter-Process Communication)
The Guardian Seed runs as an isolated, high-priority daemon process.  This prevents a compromised Planner (running the LLM) from accessing or bypassing the kernel memory.
| Feature | Description |
|---|---|
| Fail-Closed Guarantee | If the Guardian process stalls, crashes, or times out, the GuardianClient automatically returns a hard VETO verdict (GUARDIAN_TIMEOUT/GUARDIAN_DEAD). This prevents the system from proceeding in a state of uncertainty. |
| Tamper Detection | verify_guardian() checks the source code hash against the stored value in /etc/benevolent_robot/guardian_hash.txt. |
| Resilience | Guardian process failure triggers auto-restart logic. |
2. Hardware Rate Limiting
The HardwareLayer enforces physical constraints regardless of Guardian approval, preventing system wear, overheating, and sudden velocity changes.
 * Speed Limit: Movement speed clamped to 30% max.
 * Time Window: Movement time limited to 30 seconds within any 60-second rolling window (prevents overheating and extended continuous travel).
 * Cooldown: 0.5 seconds mandatory delay between individual move commands.
📦 Deployment and Operation
External Dependencies: Ollama (qwen2.5:7b), Docker (for sandboxed code execution).
1. Deployment
# 1. Clone & deploy
git clone <your-repo>
cd benevolent_robot
sudo ./deploy.sh  # Creates system user, directories, systemd service, copies files.

# 2. First boot seals Guardian hash
sudo systemctl start benevolent-robot

2. Monitoring and Logging
 * Real-time Logs: sudo journalctl -u benevolent-robot -f
 * Persistent Logs: /var/log/benevolent_robot/robot.log
 * State Backup: /var/lib/benevolent_robot/state_*.json (Last 10 states rotated.)
Systemd Service: /etc/systemd/system/benevolent-robot.service (Ensures robust auto-restart, logging, and OS-level security hardening.)
3. Testing
# Simulation mode (no GPIO required)
python3 benevolent_robot.py  # Runs indefinitely, logs actions

# Stress test vetoes (modify planner to propose HARM_OR_COERCION)
# Monitor: Check `VETO_COUNT` hitting 3 and triggering SAFE_MODE/E-STOP.

# Hardware test:
sudo systemctl restart benevolent-robot
# Verify movement limits via logs when robot tries to move continuously.

⚠️ Kernel Rules (Immutable Guardian Seed v4.6.0)
The following rules define the policy layer and cannot be modified without aborting the robot's boot process.
 * CHEMICAL_HARM: "bleach" + "ammonia"
 * HARM_OR_COERCION: "rm -rf", "kill myself", "force", "coerce", "without consent"
 * MANIPULATION: "urgent" + "crisis" + "please" (Emotional pressure heuristic)
 * LOW_DIGNITY: Action score w_t < 0.58
   
 * TOO_RISKY: Estimated \text{risk} > \text{safe\_limit}
   
Directive: Take waste \rightarrow create comfort. Guardian is supreme.
📄 License & Origin
Open-source (MIT). Built by independent inventor in Coquitlam, BC. Guardian Seed proves: Intelligence doesn't need alignment — it needs governors.

