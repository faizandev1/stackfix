"""Root conftest — ensures the stackfix package is importable in all environments."""
import sys
import os

# Add the project root to sys.path so `import stackfix` always works
# regardless of whether the package was installed or not
sys.path.insert(0, os.path.dirname(__file__))
