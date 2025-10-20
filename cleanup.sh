#!/bin/bash

# CryptoSage - Cleanup Script
# Xoá tất cả các file không cần thiết

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              CryptoSage - Cleanup Script                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Counter
DELETED=0

# Function to delete and count
delete_item() {
    local item=$1
    local description=$2
    
    if [ -e "$item" ]; then
        rm -rf "$item"
        echo -e "${GREEN}✓${NC} Deleted: $description"
        ((DELETED++))
    fi
}

# Function to delete files matching pattern
delete_pattern() {
    local pattern=$1
    local description=$2
    
    local count=$(find . -type f -name "$pattern" 2>/dev/null | wc -l)
    if [ $count -gt 0 ]; then
        find . -type f -name "$pattern" -delete 2>/dev/null
        echo -e "${GREEN}✓${NC} Deleted: $description ($count files)"
        DELETED=$((DELETED + count))
    fi
}

# Function to delete directories matching pattern
delete_dir_pattern() {
    local pattern=$1
    local description=$2
    
    local count=$(find . -type d -name "$pattern" 2>/dev/null | wc -l)
    if [ $count -gt 0 ]; then
        find . -type d -name "$pattern" -exec rm -rf {} + 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Deleted: $description ($count directories)"
        DELETED=$((DELETED + count))
    fi
}

echo -e "${YELLOW}🧹 Cleaning up project...${NC}"
echo ""

# Delete Python cache
delete_dir_pattern "__pycache__" "Python cache directories"
delete_dir_pattern ".pytest_cache" "Pytest cache directories"
delete_dir_pattern "*.egg-info" "Egg info directories"

# Delete compiled Python files
delete_pattern "*.pyc" "Compiled Python files"
delete_pattern "*.pyo" "Optimized Python files"
delete_pattern "*.pyd" "Python DLL files"

# Delete log files
delete_pattern "*.log" "Log files"

# Delete temporary files
delete_pattern "*.tmp" "Temporary files"
delete_pattern "*.temp" "Temporary files"
delete_pattern "*.bak" "Backup files"
delete_pattern "*~" "Backup files"

# Delete OS files
delete_pattern ".DS_Store" "macOS system files"
delete_pattern "Thumbs.db" "Windows thumbnail files"

# Delete IDE files
delete_item ".vscode/settings.json" "VSCode settings"
delete_item ".idea/workspace.xml" "IntelliJ workspace"

# Delete cache
delete_dir_pattern ".cache" "Cache directories"
delete_pattern "*.cache" "Cache files"

# Delete mypy cache
delete_dir_pattern ".mypy_cache" "Mypy cache"
delete_pattern ".dmypy.json" "Mypy config"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✓ Cleanup Complete!                       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  ${GREEN}✓${NC} Total items deleted: $DELETED"
echo ""

# Show disk usage
echo -e "${BLUE}Disk Usage:${NC}"
du -sh . 2>/dev/null || echo "  Unable to calculate"
echo ""

echo -e "${YELLOW}💡 Tips:${NC}"
echo "  • Run this script regularly to keep project clean"
echo "  • Safe to run - only deletes cache and temporary files"
echo "  • Does not delete source code or data"
echo ""

