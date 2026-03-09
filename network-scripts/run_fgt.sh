#!/bin/bash
# Secure FortiGate Ansible Runner - Prompts for credentials
# Usage: ./run_fgt.sh <playbook> [extra-options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/fortigate"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  🔐 Secure FortiGate Playbook Runner${NC}"
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
    echo "  $0 basic/system_status"
    echo "  $0 ipsec/ipsec_status"
    echo "  $0 monitoring/monitor_traffic"
    exit 0
fi

PLAYBOOK="$1"
shift

if [ ! -f "../playbooks/${PLAYBOOK}.yml" ]; then
    echo -e "${RED}Error: Playbook not found: ../playbooks/${PLAYBOOK}.yml${NC}"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🔐 Running FortiGate Playbook: ${PLAYBOOK}${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Prompt for username
if [ -z "$ANSIBLE_NET_USERNAME" ]; then
    echo -e "${YELLOW}Enter FortiGate username (default: admin): ${NC}"
    read -r ANSIBLE_NET_USERNAME
    ANSIBLE_NET_USERNAME=${ANSIBLE_NET_USERNAME:-admin}
fi

export ANSIBLE_NET_USERNAME

echo ""
echo -e "${GREEN}Running playbook...${NC}"
echo ""

# Run with prompts - NO PASSWORD STORED
ansible-playbook \
    -i inventory \
    "../playbooks/${PLAYBOOK}.yml" \
    --ask-pass \
    "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Playbook completed successfully!${NC}"
else
    echo -e "${RED}❌ Playbook failed with exit code: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
