# Cisco ASA/Firepower Ansible Playbooks

Collection of operational playbooks for managing Cisco ASA running on Firepower chassis.

## Structure

```
.
├── playbooks/
│   ├── basic/           # Quick operational checks
│   ├── health/          # Health monitoring
│   ├── ipsec/           # VPN tunnel management
│   └── backup/          # Backup/restore
├── host_vars/           # Device-specific vars
├── group_vars/          # Group variables
└── docs/                # Documentation
```

## Usage

```bash
# Run a single playbook
ansible-playbook -i inventory playbooks/basic/show_version.yml

# Run with custom variables
ansible-playbook -i inventory playbooks/basic/show_interfaces.yml -e "device=asa01"

# Check mode (dry run)
ansible-playbook -i inventory playbook.yml --check
```

## Inventory

Edit `inventory` file to add your ASA devices:

```ini
[asa_firepower]
asa01 ansible_host=10.1.1.1
asa02 ansible_host=10.1.1.2

[asa_firepower:vars]
ansible_user=admin
ansible_password=YOUR_PASSWORD
ansible_connection=network_cli
ansible_network_os=cisco.asa.asa
```

## Output Format

All playbooks support JSON output for SolarWinds integration. Use `-e "output_format=json"` for JSON output.

## Requirements

- `cisco.asa` collection: `ansible-galaxy collection install cisco.asa`
- `ansible.netcommon` collection: `ansible-galaxy collection install ansible.netcommon`

---

See `docs/` folder for detailed documentation on each playbook.
