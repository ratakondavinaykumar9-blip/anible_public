#!/bin/bash
# ASA Playbook Runner - Quick execution script
# Usage: ./run.sh <playbook> [options]
# Example: ./run.sh basic/show_version

PLAYBOOK_DIR="playbooks"
INVENTORY="inventory"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${YELLOW}ASA Playbook Runner${NC}"
    echo "Usage: $0 <playbook> [options]"
    echo ""
    echo "Available playbooks:"
    find $PLAYBOOK_DIR -name "*.yml" | sort | while read f; do
        echo "  $f"
    done
    exit 1
fi

PLAYBOOK="$1"
shift

# Check if playbook exists
if [ ! -f "$PLAYBOOK_DIR/$PLAYBOOK.yml" ]; then
    echo -e "${RED}Error: Playbook not found: $PLAYBOOK_DIR/$PLAYBOOK.yml${NC}"
    exit 1
fi

echo -e "${GREEN}Running: $PLAYBOOK${NC}"
ansible-playbook -i $INVENTORY $PLAYBOOK_DIR/$PLAYBOOK.yml "$@"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Success!${NC}"
else
    echo -e "${RED}Failed!${NC}"
    exit 1
fi
