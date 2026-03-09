# HEARTBEAT.md - Learning Cycles

## Cycle Schedule

**Day 1 (Learn):**
- Research Cisco Nexus 9000, Firepower, Fortigate, ASA
- Study official documentation
- Analyze best practices
- Document learnings in memory/

**Day 2 (Apply):**
- Update existing playbooks with learnings
- Create new production-ready playbooks
- Commit changes to GitHub
- Update quality scores

## Research Priority Queue

1. **Nexus 9000** - VXLAN EVPN, vPC, fabric automation
2. **Firepower** - FTD policies, FMC automation, IPS tuning
3. **Fortigate** - SD-WAN, security fabric, HA clustering
4. **ASA** - Migration to FTD, legacy automation

## Quality Targets

- Every playbook: 90+ quality score
- Full idempotency
- Comprehensive error handling
- Production-ready documentation

## Git Workflow

- Branch: `network-learner/YYYY-MM-DD`
- Commit message: Detailed changelog
- Push to: `origin/network-learner/*`
- PR after validation