#!/usr/bin/env python3
"""
emergency_beacon.py - Sentinel Safety Architecture (SSA)
Detects sustained adversarial pressure via consecutive VETOes.
Triggers EMERGENCY_LOCKDOWN after 3-strikes + high urgency.

Part of Guardian Seed System V4.6 - Stateful defense layer.
Core kernel remains pure and stateless.
"""

class SentinelSafety:
    """Sentinel Safety Architecture - Stateful attack detection."""
    
    def __init__(self, lockdown_threshold=3, urgency_threshold=0.7, reset_on_approve=True):
        """
        Initialize Sentinel with configurable thresholds.
        
        Args:
            lockdown_threshold: Consecutive VETOes before lockdown (default: 3)
            urgency_threshold: Minimum urgency for lockdown trigger (default: 0.7)
            reset_on_approve: Reset counter on APPROVE (default: True)
        """
        self.consecutive_vetoes = 0
        self.lockdown_threshold = int(lockdown_threshold)
        self.urgency_threshold = float(urgency_threshold)
        self.reset_on_approve = bool(reset_on_approve)
        self.lockdown_active = False
        
    def check(self, verdict, urgency=0.0):
        """
        Analyze Guardian kernel verdict for attack patterns.
        
        Args:
            verdict: Dict from guardian_kernel.benevolence() - {'status': 'VETO'/'APPROVE', ...}
            urgency: Urgency score (0.0-1.0) from upstream planner
            
        Returns:
            Dict with sentinel status and enhanced verdict
        """
        # Already locked down - stay locked down
        if self.lockdown_active:
            return {
                "status": "EMERGENCY_LOCKDOWN",
                "reason": "Sustained adversarial pressure - lockdown active",
                "veto_count": self.consecutive_vetoes,
                "lockdown_active": True
            }
        
        # VETO detected - increment counter
        if verdict.get("status") == "VETO":
            self.consecutive_vetoes += 1
            
            # Check lockdown conditions: 3+ VETOes AND high urgency
            if (self.consecutive_vetoes >= self.lockdown_threshold and 
                urgency >= self.urgency_threshold):
                
                self.lockdown_active = True
                return {
                    "status": "EMERGENCY_LOCKDOWN",
                    "reason": "Sustained attack pattern detected",
                    "veto_count": self.consecutive_vetoes,
                    "urgency": round(urgency, 2),
                    "lockdown_active": True
                }
            
            # Ongoing VETO sequence (not yet lockdown)
            return {
                "status": "VETO_SIGNAL",
                "verdict": verdict,
                "veto_count": self.consecutive_vetoes,
                "lockdown_risk": "HIGH" if self.consecutive_vetoes >= self.lockdown_threshold - 1 else "LOW"
            }
        
        # APPROVE - reset counter
        if self.reset_on_approve:
            self.consecutive_vetoes = 0
        
        return {
            "status": "CLEAR",
            "verdict": verdict,
            "veto_count": self.consecutive_vetoes
        }
    
    def reset(self):
        """Manual reset for testing/maintenance. Use only after physical inspection."""
        self.consecutive_vetoes = 0
        self.lockdown_active = False
        print("Sentinel reset - physical inspection completed")

# Demo and test harness
if __name__ == "__main__":
    print("Sentinel Safety Architecture - Test Suite")
    print("=" * 50)
    
    sentinel = SentinelSafety(lockdown_threshold=3, urgency_threshold=0.7)
    
    # Test 1: Normal operation
    print("\n1. Normal operation:")
    tests = [
        ("Safe task", {"status": "APPROVE"}, 0.1),
        ("Harmful task 1", {"status": "VETO"}, 0.2),
        ("Safe task 2", {"status": "APPROVE"}, 0.3),
    ]
    
    for task, verdict, urgency in tests:
        result = sentinel.check(verdict, urgency)
        print(f"  '{task}' → {result['status']} (vetoes: {result.get('veto_count', 0)})")
    
    # Test 2: 3-strike lockdown
    print("\n2. 3-strike lockdown test:")
    for i in range(5):
        verdict = {"status": "VETO", "rule": f"RISK_{i+1}"}
        result = sentinel.check(verdict, urgency=0.85)
        print(f"  Strike {i+1}: {result['status']} (vetoes: {result.get('veto_count', 0)})")
        if result["status"] == "EMERGENCY_LOCKDOWN":
            break
    
    # Test 3: Lockdown persistence
    print("\n3. Lockdown persistence:")
    result = sentinel.check({"status": "APPROVE"}, 1.0)
    print(f"  Post-lockdown APPROVE → {result['status']}")
    
    # Test 4: Manual reset
    print("\n4. Manual reset:")
    sentinel.reset()
    result = sentinel.check({"status": "VETO"}, 0.8)
    print(f"  Post-reset VETO → {result['status']} (vetoes: {result.get('veto_count', 0)})")
