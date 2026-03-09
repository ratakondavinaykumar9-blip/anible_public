#!/bin/bash
# Secure Ansible Runner - Prompts for credentials, doesn't store them
# Usage: ./run_asa.sh <playbook> [extra-options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/cisco-asa"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if playbook provided
if [ -z "$1" ]; then
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  🔐 Secure ASA Playbook Runner${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Usage: $0 <playbook> [options]"
    echo ""
    echo -e "${GREEN}Available playbooks:${NC}"
    echo ""
    find ../playbooks -name "*.yml" -type f | sort | while read f; do
        playbook_name=$(echo "$f" | sed 's|../playbooks/||' | sed 's/\.yml$//')
        echo "  📄 $playbook_name"
    done
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 basic/show_version"
    echo "  $0 basic/show_version -e 'output_format=json'"
    echo "  $0 ipsec/tunnel_status"
    echo "  $0 ipsec/troubleshoot_tunnel -e 'tunnel_peer=1.2.3.4'"
    exit 0
fi

PLAYBOOK="$1"
shift

# Validate playbook exists
if [ ! -f "../playbooks/${PLAYBOOK}.yml" ]; then
    echo -e "${RED}Error: Playbook not found: ../playbooks/${PLAYBOOK}.yml${NC}"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🔐 Running ASA Playbook: ${PLAYBOOK}${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if credentials are set via environment
if [ -z "$ANSIBLE_NET_USERNAME" ]; then
    echo -e "${YELLOW}Enter Ansible username: ${NC}"
    read -r ANSIBLE_NET_USERNAME
fi

# Don't use stored password - always prompt
# This ensures security - no passwords saved anywhere
export ANSIBLE_NET_USERNAME

echo ""
echo -e "${GREEN}Running playbook...${NC}"
echo ""

# Run playbook with prompt for password
# --ask-pass = SSH password
# --ask-become-pass = Enable password
ansible-playbook \
    -i inventory \
    "../playbooks/${PLAYBOOK}.yml" \
    --ask-pass \
    --ask-become-pass \
    "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Playbook completed successfully!${NC}"
else
    echo -e "${RED}❌ Playbook failed with exit code: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
