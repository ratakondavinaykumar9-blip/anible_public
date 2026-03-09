# Ansible Agent System

## Mission
Continuously learn, improve, and expand network automation playbooks.

## Agents

### 1. Script Analyzer (Daily)
- Reviews all existing playbooks
- Identifies improvement opportunities
- Checks for: idempotency, error handling, speed optimizations, best practices

### 2. Platform Builders
- **Nexus9k-Builder**: Cisco Nexus 9000 series playbooks
- **Juniper-SRX-Builder**: Juniper 320/Firewall automation
- **DellEMC-Builder**: Dell EMC switch configuration
- **Cisco-IOS-Builder**: Cisco IOS/IOS-XE switch automation
- **ASA-Enhancer**: Improve existing ASA playbooks
- **Fortigate-Enhancer**: Improve existing Fortigate playbooks

### 3. Git Guardian
- Tests changes in feature branches
- Creates documented PRs
- Merges approved changes

## Schedule
- **Daily at 06:00 UTC**: Script Analyzer runs
- **Daily at 08:00 UTC**: Platform Builders run (staggered)
- **Daily at 18:00 UTC**: Git Guardian reviews and commits

## Metrics
- Total playbooks
- Coverage per platform
- Quality score (0-100)
- Last improvement date

## Rules
1. Never break existing working scripts
2. Always test in isolation before commit
3. Document every change
4. Follow Ansible best practices religiously