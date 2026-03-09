# Research Phase: Network Automation Platforms
**Date:** 2026-03-03
**Focus:** Cisco Firepower, Nexus 9000, Fortigate, ASA
**Cycle:** Research → Apply (Next: Apply)

---

## 1. Cisco Nexus 9000 - VXLAN EVPN Automation

### Key Ansible Modules Discovered

#### EVPN Global Module (`cisco.nxos.nxos_evpn_global`)
- Enables EVPN control plane for VXLAN
- Simple parameter: `nv_overlay_evpn: true`
- **Note:** Not supported on Nexus 3000 series

#### EVPN VNI Module (`cisco.nxos.nxos_evpn_vni`)
- Manages VXLAN Network Identifier configurations
- Key parameters:
  - `vni`: The EVPN VNI (required)
  - `route_distinguisher`: VPN RD (format: "auto", "default", or "X:Y")
  - `route_target_import`: List of import route targets
  - `route_target_export`: List of export route targets
  - `route_target_both`: Deprecated - use explicit import/export instead

### Best Practices from Backup Playbook (backup_config.yml)
```yaml
# Pattern: Comprehensive backup with validation
- Validation of configuration size before backup
- Configuration drift detection (running vs startup)
- Metadata generation for audit trails
- Retention management with auto-cleanup
- Rescue blocks for error handling
- Multiple configuration sources (running, startup, VLAN DB)
```

### Recommended VXLAN EVPN Playbook Structure
```
cisco-nexus9k/vxlan/
├── vxlan_bgp.yml          # BGP underlay configuration
├── vxlan_evpn.yml         # EVPN control plane
├── nve.yml                # NVE interface configuration
├── vni_l2.yml             # Layer 2 VNI configurations
└── vni_l3.yml             # Layer 3 VNI (anycast gateway)
```

---

## 2. Fortinet FortiOS - SD-WAN & Security

### SD-WAN Module (`fortinet.fortios.fortios_system_sdwan`)

Comprehensive SD-WAN configuration with:

#### Health Check Parameters
- Protocol options: ping, tcp-echo, udp-echo, http, https, twamp, dns, tcp-connect, ftp
- SLA definitions with thresholds:
  - `latency_threshold`: ms
  - `jitter_threshold`: ms
  - `packetloss_threshold`: percentage
  - `mos_threshold`: Mean Opinion Score for voice quality

#### Load Balance Modes
- `source-ip-based`
- `weight-based`
- `usage-based`
- `source-dest-ip-based`
- `measured-volume-based`

#### Member Configuration
- `gateway`: ISP default gateway
- `priority`: Interface priority for rules
- `cost`: Cost for SLA mode services
- `spillover_threshold`: Traffic volume threshold
- `volume_ratio`: Weighted load balancing

### Router Policy Module (`fortinet.fortios.fortios_router_policy`)
- Policy-based routing configuration
- Supports: src/dst address, protocol, ports, gateway
- Internet service matching (FortiGuard and custom)
- User/group-based routing

### VDOM Support
All FortiOS modules support `vdom` parameter for virtual domain isolation.

### Security Features Catalog (from existing playbooks)
```
fortigate/security/
├── appctrl_profile.yml    # Application control
├── av_profile.yml         # Antivirus
├── content_armor.yml      # Content disarm
├── dnsfilter_profile.yml  # DNS filtering
├── emailfilter.yml        # Email security
├── filepattern.yml        # File pattern matching
├── ips_global.yml         # Global IPS settings
├── ips_profile.yml        # IPS profiles
├── ips_signatures.yml     # Custom signatures
├── utm_stats.yml          # UTM statistics
├── waf_profile.yml        # Web app firewall
└── webfilter_profile.yml  # Web filtering
```

---

## 3. Cisco ASA - VPN & ACL Management

### Existing Playbook Patterns Observed

#### IPSec Tunnel Status (`tunnel_status.yml`)
- Multi-protocol support: IKEv1 and IKEv2
- Multiple data sources:
  - `show vpn-sessiondb l2l`
  - `show crypto ipsec sa`
  - `show crypto isakmp sa`
  - `show crypto ikev2 sa`
- JSON output option for integration with monitoring tools

#### ACL Management
- `acl_aces_per_acl.yml`: Count access control entries
- `acl_expanded.yml`: View expanded ACL details
- `acl_hits.yml`: ACL hit counters for optimization
- `acl_log.yml`: ACL logging configuration
- `acl_remarks.yml`: ACL documentation/remarks

### ASA Collection Note
⚠️ `cisco.asa` collection removed from Ansible 12
- Must install manually: `ansible-galaxy collection install cisco.asa`

---

## 4. Juniper SRX 300 Series

### Structure (from README.md)
```
juniper-srx/
├── basic/           # hostname, dns, ntp, snmp, users, ssh
├── interfaces/      # physical, vlan, aggregate, tunnel
├── routing/         # ospf, bgp, static, routing-instances
├── security/        # zones, policies, address-book, screens
├── nat/             # source-nat, destination-nat, static-nat
├── vpn/             # site-to-site, remote-access
├── ips/             # idp-policies
├── monitoring/      # jflow, logging, snmp-traps
├── ha/              # chassis-cluster
└── backup/          # backup-config
```

### Requirements
- Collection: `junipernetworks.junos`
- Python: `junos-eznc`

### Best Practices
- Configuration rollback on failure
- Diff display before commit
- Structured validation

---

## 5. Cisco Firepower - Research Gaps

### Documentation Access Issues
- Cisco DevNet Firepower pages returning 403/404 errors
- Ansible `cisco.ftd` collection documentation minimal on Galaxy

### Known Approaches for FTD/ASA Automation
1. **CLI via SSH**: Use `ansible.netcommon.cli_command` for show commands
2. **FMC API**: REST API for policy management (requires separate documentation)
3. **Firepower Management Center**: Central policy deployment

### FTD vs ASA Mode Considerations
- FTD uses unified threat policies (not traditional ACLs)
- ASA mode maintains traditional ACL/NAT structure
- Migration path: ASA → FTD requires policy conversion

---

## 6. Playbook Quality Patterns Observed

### Common Headers
```yaml
# ==============================================================================
# Playbook: [Name]
# ==============================================================================
# Author: [Name]
# Version: [X.Y.Z]
# Last Updated: [Date]
# Description: [What this does]
#
# Platforms: [Supported devices]
# Requirements: [Collections needed]
# ==============================================================================
```

### Error Handling Pattern (Rescue Blocks)
```yaml
- name: Task block
  block:
    - name: Main task
      # ...
  rescue:
    - name: Log failure
      ansible.builtin.debug:
        msg: "ERROR: {{ ansible_failed_result.msg }}"
    - name: Create failure marker
      # ...
```

### Idempotency Pattern
```yaml
- name: Task with idempotency
  cisco.nxos.nxos_command:
    commands: show running-config
  register: result
  changed_when: false
  failed_when:
    - result is failed
    - result.stdout is not defined
```

---

## 7. Key Findings Summary

| Platform | Primary Collection | Automation Readiness | Gaps |
|----------|-------------------|---------------------|------|
| Nexus 9000 | cisco.nxos | ✅ Excellent | VXLAN vNI playbooks |
| Fortigate | fortinet.fortios | ✅ Excellent | SD-WAN service rules |
| ASA | cisco.asa | ⚠️ Good (manual install) | VPN automation |
| Firepower FTD | cisco.ftd | ⚠️ Limited | FMC API integration |
| Juniper SRX | junipernetworks.junos | ✅ Good | Security policies |

---

## 8. Next Cycle: Apply

**Priority Tasks:**
1. Create VXLAN EVPN playbooks for Nexus 9000
2. Build SD-WAN health-check and service rule playbooks for Fortigate
3. Enhance ASA VPN troubleshooting playbooks
4. Research FMC REST API for Firepower automation

---

*Research completed by Network Automation Framework (OpenClaw)*