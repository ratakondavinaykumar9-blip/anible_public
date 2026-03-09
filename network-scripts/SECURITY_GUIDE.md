# Ansible Vault - Secure Credential Storage

## Why Use Ansible Vault?

✅ **Never store passwords in plain text**
✅ **Encrypt sensitive files**
✅ **Version control safe** (can commit encrypted files)
✅ **Industry standard practice**

---

## Quick Start

### 1. Create a Vault Password File
```bash
# Create a secure password file (600 permissions)
echo "your-strong-vault-password" > ~/.ansible_vault-pass
chmod 600 ~/.ansible_vault-pass
```

### 2. Create Encrypted Variables
```bash
# Create encrypted file for ASA credentials
ansible-vault create group_vars/asa_firepower.yml --vault-password-file ~/.ansible_vault-pass
```

Add your credentials:
```yaml
---
ansible_user: admin
ansible_password: "YourSecurePassword123!"
ansible_become_pass: "YourEnablePassword"
```

### 3. Create encrypted file for FortiGate
```bash
ansible-vault create group_vars/fortigate.yml --vault-password-file ~/.ansible_vault-pass
```

Add:
```yaml
---
ansible_user: admin
ansible_password: "YourSecurePassword123!"
```

### 4. Run Playbooks
```bash
# With vault password file
ansible-playbook -i inventory playbook.yml --vault-password-file ~/.ansible_vault-pass

# It will decrypt and use the credentials automatically!
```

---

## Alternative: Environment Variables (No Vault)

For quick testing without vault setup:

```bash
# Set environment variables (they're temporary - gone after terminal closes)
export ANSIBLE_NET_USERNAME=admin
export ANSIBLE_NET_PASSWORD=your_password

# Run playbook
ansible-playbook -i inventory playbook.yml
```

**Pros:** Quick, no setup
**Cons:** Need to set every session, not as secure

---

## Alternative: Prompt at Runtime

The scripts we created will always prompt for passwords:

```bash
# ASA - will ask for SSH password + enable password
./run_asa.sh basic/show_version

# FortiGate - will ask for password
./run_fgt.sh basic/system_status
```

**Pros:** Most secure - password never stored anywhere
**Cons:** Must enter password every time

---

## Comparison

| Method | Security | Convenience | Best For |
|--------|----------|-------------|----------|
| **Prompt (our default)** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Maximum security |
| **Environment Variables** | ⭐⭐⭐ | ⭐⭐⭐ | Quick testing |
| **Ansible Vault** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Production use |

---

## Our Scripts Use Prompt by Default

The `run_asa.sh` and `run_fgt.sh` scripts will ALWAYS prompt for credentials - they will NEVER store passwords. This is the most secure option.

If you want to use Ansible Vault, you can modify the scripts or run ansible-playbook directly with the vault password file.
