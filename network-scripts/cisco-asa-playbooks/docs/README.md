# Cisco ASA Playbooks - Documentation

## Quick Start

### 1. Install Requirements
```bash
# Install Ansible collections
ansible-galaxy collection install -r requirements.yml

# Or individually:
ansible-galaxy collection install cisco.asa
ansible-galaxy collection install ansible.netcommon
```

### 2. Configure Inventory
Edit the `inventory` file and add your ASA devices:
```ini
[asa_firepower]
asa01 ansible_host=10.1.1.1
asa02 ansible_host=10.1.1.2
```

Set your credentials in `group_vars/asa_firepower.yml` or directly in inventory (less secure).

### 3. Test Connectivity
```bash
ansible all -i inventory -m ping
```

### 4. Run a Playbook
```bash
# Using the runner script
./run.sh basic/show_version

# Or directly
ansible-playbook -i inventory playbooks/basic/show_version.yml
```

## Playbook Categories

### Basic Operational (playbooks/basic/)
| Playbook | Description | Use Case |
|----------|-------------|----------|
| `show_version.yml` | Get ASA version, model, serial | Quick device info |
| `show_interfaces.yml` | Interface status, IP addresses | Check interface health |
| `show_failover.yml` | Failover status | Verify HA pair status |
| `show_nat.yml` | NAT rules table | Review NAT config |
| `show_acls.yml` | Access lists | Audit security rules |
| `show_routes.yml` | Routing table | Check routes |

### Health Monitoring (playbooks/health/)
| Playbook | Description | Use Case |
|----------|-------------|----------|
| `health_check.yml` | CPU, Memory, Connections | Daily health check |

### IPSec VPN (playbooks/ipsec/)
| Playbook | Description | Use Case |
|----------|-------------|----------|
| `tunnel_status.yml` | All tunnel summary | Quick tunnel overview |
| `tunnel_detail.yml` | Detailed tunnel info | Deep dive on specific tunnel |
| `troubleshoot_tunnel.yml` | Full troubleshooting | When tunnel is down |

### Backup (playbooks/backup/)
| Playbook | Description | Use Case |
|----------|-------------|----------|
| `backup_config.yml` | Backup running/startup config | Regular backups |

## SolarWinds Integration

### JSON Output
All playbooks support JSON output for SolarWinds:
```bash
# Run with JSON output
ansible-playbook -i inventory playbooks/health/health_check.yml -e "output_format=json"

# Output saved to /tmp/
```

### Custom Monitoring
The JSON files contain:
- Device name
- Timestamp
- All command outputs
- Ready for SolarWinds API ingestion

## Examples

### Quick Health Check
```bash
./run.sh health/health_check -e "output_format=json"
```

### Check Specific Tunnel
```bash
./run.sh ipsec/tunnel_detail -e "tunnel_peer=203.0.113.1"
```

### Troubleshoot Down Tunnel
```bash
./run.sh ipsec/troubleshoot_tunnel -e "tunnel_peer=203.0.113.1"
```

### Backup All Devices
```bash
ansible-playbook -i inventory playbooks/backup/backup_config.yml
```

## Troubleshooting

### Connection Issues
```bash
# Test connectivity
ansible all -i inventory -m ansible.netcommon.cli_ping

# Debug mode
ansible-playbook -i inventory playbooks/basic/show_version.yml -vvv
```

### Credential Issues
- Ensure `ansible_become_pass` is set for enable mode
- Check SSH connectivity to ASA
- Verify device is reachable from Ansible host

### Module Errors
- Ensure cisco.asa collection is installed: `ansible-galaxy collection list`
- Check Ansible version: `ansible --version` (need 2.9+)
