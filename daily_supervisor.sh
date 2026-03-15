#!/bin/bash
# NETLEARNER AGENT SUPERVISOR
# Ensures the Triad Agents run for exactly 2 hours and never stay crashed.

SCRIPT_DIR="/home/vinayrk/ansible_improved"
LOG_FILE="$SCRIPT_DIR/agent_runtime.log"
START_TIME=$(date +%s)
DURATION=$((2 * 60 * 60)) # 2 Hours
END_TIME=$((START_TIME + DURATION))

exec >> "$LOG_FILE" 2>&1

echo "==============================================================="
echo "SESSION START: $(date)"
echo "GOAL: 2-Hour Autonomous Research & Deployment"
echo "==============================================================="

while [ $(date +%s) -lt $END_TIME ]; do
    CURRENT_TIME=$(date +%s)
    REMAINING=$((END_TIME - CURRENT_TIME))
    
    echo "[$(date +%T)] Supervisor: Running MEA Cycle. Remaining: $((REMAINING / 60))m"
    
    # DYNAMIC SEARCH: ONLY STAGING AND TESTING PLAYBOOKS
    # Production promotion requires manual permission per v12.2 Mandate.
    for playbook in $(find "$SCRIPT_DIR/e2e_deployments" -name "*.yml" | grep -Ei "staging|testing"); do
        echo "[$(date +%T)] Supervisor: Starting v12.2 Autonomous Run for: $playbook"
        python3 "$SCRIPT_DIR/mea_runner.py" "$playbook"
        
        RET=$?
        if [ $RET -ne 0 ]; then
            echo "[$(date +%T)] CRASH/SAFETY REJECTED: $playbook exited with code $RET. Self-healing..."
            sleep 30
        else
            echo "[$(date +%T)] SUCCESS: $playbook cycle finished."
        fi
    done
    
    # Wait 15 mins before next sweep to check for drifts
    sleep 900 
    
    if [ $REMAINING -le 0 ]; then break; fi
done

echo "==============================================================="
echo "SESSION END: $(date) - Window Closed Successfully."
echo "==============================================================="
