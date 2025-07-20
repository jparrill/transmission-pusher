#!/usr/bin/env python3
"""
Transmission Client - Wrapper script
This script allows you to run the transmission client from the project root
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main function
if __name__ == "__main__":
    from transmission_pusher.transmission_client import main

    exit(main())
