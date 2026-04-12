# 🧠 Long-Term Memory: Network Automation Framework

## 🏗️ Core Architecture (Updated 2026-04-07)

### **Inventory Management: Dual-View Tree**
The framework has transitioned from legacy flat `.ini` files to a **Hierarchical YAML Tree** (`dc_inventory_tree.yaml`).
- **Geographic View:** Assets grouped by Site (AMS, YUL, SIN, GIG) and then by function (firewalls, switches, routers).
- **Functional View:** Global Platform Groups (e.g., `global_nexus_switches`) that span all sites. 
- **Variable Inheritance:** `ansible_network_os` and other platform-specific variables are defined at the Global group level.
- **Connection Strategy:** Uses `network_cli` as the default, but overrides to `ssh` for Fortinet devices to allow `ansible.builtin.raw` commands.

### **Asset Discovery Strategy**
We utilize specialized, high-efficiency playbooks for network investigation:
- **`find_mac.yaml`**: Fast MAC table lookup targeting only switches and ASA firewalls.
- **`find_ip.yaml`**: Comprehensive IP search targeting only Firewalls and Production Routers (excluding OBS). Shows full raw CLI output for Fortinet.

## 🛡️ Best Practices & Mandates
1.  **Always use `dc_inventory_tree.yaml`** for new playbooks to leverage functional grouping.
2.  **Explicit Exclusion:** When targeting global groups, always explicitly exclude `obs_routers` if the task involves production traffic pathing.
3.  **Idempotency & Validation:** Every playbook must include a verification step to confirm the desired state was reached.

## 🏛️ Project History & Milestones
- **2026-04-07:** Conversion to Hierarchical Inventory. Creation of MAC/IP locator playbooks. Implementation of the `ansible` Gemini Skill.
