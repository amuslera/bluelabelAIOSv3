#!/usr/bin/env python3
"""
Run the AIOSv3 Control Center
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from control_center.main import main

if __name__ == "__main__":
    # Set environment variables if not set
    if not os.getenv("MONITORING_URL"):
        os.environ["MONITORING_URL"] = "ws://localhost:8765"
    if not os.getenv("REDIS_URL"):
        os.environ["REDIS_URL"] = "redis://localhost:6379"
        
    main()