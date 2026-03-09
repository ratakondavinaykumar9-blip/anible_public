# Network Scripts - Combined ASA & FortiGate Ansible Playbooks

## Overview
Comprehensive collection of operational, troubleshooting, and configuration playbooks for Cisco ASA and FortiGate firewalls.

## Repository Structure
```
network-scripts/
├── cisco-asa/           # Cisco ASA/Firepower playbooks
│   ├── basic/           # Basic operational commands
│   ├── interfaces/       # Interface management
│   ├── nat/             # NAT configuration
│   ├── acl/             # Access lists
│   ├── routing/         # Routing (static, OSPF, BGP)
│   ├── failover/        # HA/Failover
│   ├── ipsec/           # IPSec VPNs
│   ├── ssl-vpn/         # SSL VPN
│   ├── backup/          # Configuration backup
│   ├── monitoring/      # Health checks & monitoring
│   └── objects/         # Objects & object groups
│
└── fortigate/           # FortiGate playbooks
    ├── basic/           # Basic operational commands
    ├── interfaces/      # Interface configuration
    ├── policy/          # Firewall policies
    ├── nat/             # NAT rules
    ├── routing/         # Routing configuration
    ├── ipsec/           # IPSec VPNs
    ├── ssl-vpn/         # SSL VPN
    ├── security/        # Security profiles
    ├── ha/              # High Availability
    ├── backup/          # Configuration backup
    └── monitoring/      # Monitoring & health
```

## Requirements
- Ansible 2.9+
- ansible.netcommon collection
- cisco.asa collection (for ASA)
- fortinet.fortios collection (for FortiGate)

## Installation
```bash
# Install collections
ansible-galaxy collection install ansible.netcommon
ansible-galaxy collection install cisco.asa
ansible-galaxy collection install fortinet.fortios
```

## Usage
```bash
# Run ASA playbook
ansible-playbook -i asa_inventory playbooks/cisco-asa/basic/show_version.yml

# Run FortiGate playbook
ansible-playbook -i fgt_inventory playbooks/fortigate/basic/system_status.yml
```

## SolarWinds Integration
All playbooks support JSON output:
```bash
ansible-playbook playbook.yml -e "output_format=json"
```

---
**Created:** 2026-02-21
**Status:** Active Development
