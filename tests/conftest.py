import os
import sys
from pathlib import Path

# Get the absolute path to the project root directory
root_dir = Path(__file__).parent.parent

# Add the src directory to the Python path
sys.path.append(str(root_dir / "src")) 