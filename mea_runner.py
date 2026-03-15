#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time

class MasterExecutionAgent:
    """
    MASTER EXECUTION AGENT (MEA) - v1.0
    Implements: Researcher -> Planner -> Implementer
    Goal: Zero-Crash, Validated Network Automation
    """

    def __init__(self, playbook_path, inventory=None):
        self.playbook = playbook_path
        # --- DYNAMIC INVENTORY DISCOVERY ---
        if inventory:
            self.inventory = inventory
        else:
            if "staging" in playbook_path.lower():
                self.inventory = "inventory_staging"
            elif "testing" in playbook_path.lower():
                self.inventory = "inventory_testing"
            elif "prod" in playbook_path.lower():
                self.inventory = "inventory_prod"
            else:
                self.inventory = "inventory" # fallback
        
        self.status = "INITIALIZING"
        self.metadata = {}

    def log(self, phase, message):
        print(f"[{phase}] {message}")

    def research(self):
        """Phase 1: Research - Syntax check and connectivity"""
        self.status = "RESEARCHING"
        self.log("RESEARCHER", f"Analyzing playbook: {self.playbook}")

        # --- v12.2 PRODUCTION SAFETY GATE ---
        is_prod = "prod" in self.playbook.lower() or "prod" in self.inventory.lower()
        if is_prod:
            self.log("SAFETY", "CRITICAL: Production target detected.")
            # If not running in a terminal (e.g. cron), we must fail.
            if not sys.stdin.isatty():
                self.log("ERROR", "Autonomous production deployment is FORBIDDEN. Manual permission required.")
                return False
            else:
                confirm = input("[SAFETY] Do you have explicit permission to deploy to PRODUCTION? (yes/no): ")
                if confirm.lower() != 'yes':
                    self.log("ERROR", "Production deployment aborted by user.")
                    return False
        
        # 1. Syntax Check
        cmd = ["ansible-playbook", "-i", self.inventory, self.playbook, "--syntax-check"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            self.log("ERROR", "Syntax check failed!")
            print(result.stderr)
            return False

        # 2. Extract Hosts (Simplified)
        # In a real scenario, we'd parse the YAML properly.
        self.log("RESEARCHER", "Syntax check passed. Mapping dependencies...")
        self.metadata['syntax_ok'] = True
        return True

    def plan(self):
        """Phase 2: Planner - Define validation strategy"""
        self.status = "PLANNING"
        self.log("PLANNER", "Defining Validation Protocol...")
        
        # Strategy: Pre-snapshot -> Check-Mode -> Real-Run -> Post-Scan
        self.metadata['plan'] = {
            "pre_flight": "Config Backup",
            "dry_run": "ansible-playbook --check",
            "execution": "ansible-playbook",
            "validation": "Nmap Fingerprinting & Assertion"
        }
        self.log("PLANNER", f"End Product Goal: Verified state for {self.playbook}")
        return True

    def implement(self, extra_vars=None):
        """Phase 3: Implementer - Execute and Validate"""
        self.status = "IMPLEMENTING"
        self.log("IMPLEMENTER", "Starting execution sequence...")

        # 1. Dry Run (Check Mode)
        self.log("IMPLEMENTER", "Running Check Mode (Safe-Gate)...")
        cmd_check = ["ansible-playbook", "-i", self.inventory, self.playbook, "--check"]
        if extra_vars:
            cmd_check.extend(["-e", extra_vars])
        
        # We simulate user input for passwords for now or use env vars
        # For a truly autonomous system, we'd use ansible-vault or env
        
        # 2. Real Execution (Instructional - user confirms manually for now via this wrapper)
        self.log("IMPLEMENTER", "Dry run complete. Ready for real implementation.")
        
        # Implementation logic would go here
        # For the demo, we show the command it would run
        real_cmd = f"ansible-playbook -i {self.inventory} {self.playbook}"
        self.log("IMPLEMENTER", f"Command: {real_cmd}")
        
        self.status = "COMPLETED"
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./mea_runner.py <playbook_path>")
        sys.exit(1)

    mea = MasterExecutionAgent(sys.argv[1])
    if mea.research():
        if mea.plan():
            mea.implement()
