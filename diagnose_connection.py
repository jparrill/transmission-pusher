#!/usr/bin/env python3
"""
Transmission Connection Diagnostics - Wrapper script
This script allows you to run connection diagnostics from the project root
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main function
if __name__ == "__main__":
    from transmission_pusher.diagnose_connection import main

    main()
