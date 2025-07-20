#!/bin/bash

# Installation script for transmission-cli
# Copies the CLI script to ~/bin for global access

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Installing transmission-pusher to ~/bin...${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create ~/bin if it doesn't exist
if [ ! -d "$HOME/bin" ]; then
    echo -e "${YELLOW}Creating ~/bin directory...${NC}"
    mkdir -p "$HOME/bin"
fi

# Copy the CLI script
CLI_SOURCE="$SCRIPT_DIR/transmission-cli"
CLI_DEST="$HOME/bin/transmission-pusher"

if [ -f "$CLI_SOURCE" ]; then
    cp "$CLI_SOURCE" "$CLI_DEST"
    chmod +x "$CLI_DEST"
    echo -e "${GREEN}✅ transmission-pusher installed successfully to $CLI_DEST${NC}"
else
    echo -e "${RED}❌ Error: transmission-pusher script not found at $CLI_SOURCE${NC}"
    exit 1
fi

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo -e "${YELLOW}⚠️  Warning: ~/bin is not in your PATH${NC}"
    echo -e "${YELLOW}   Add this line to your shell profile (.bashrc, .zshrc, etc.):${NC}"
    echo -e "${YELLOW}   export PATH=\"\$HOME/bin:\$PATH\"${NC}"
else
    echo -e "${GREEN}✅ ~/bin is already in your PATH${NC}"
fi

echo -e "${GREEN}🎉 Installation complete!${NC}"
echo -e "${YELLOW}Usage examples:${NC}"
echo -e "  transmission-pusher --help"
echo -e "  transmission-pusher --list"
echo -e "  transmission-pusher /path/to/file.torrent"