"""
sample_package - Demonstrates Python package structure
This __init__.py makes the directory a package.
"""

print("📦 Initializing sample_package...")

# This code runs when the package is first imported
package_version = "1.0.0"

# Control what gets imported with "from sample_package import *"
__all__ = ['module_a', 'important_function']

def important_function():
    """A function defined in the package's __init__.py"""
    return "This function is defined in __init__.py"

# You can also import and re-export items from submodules
from .module_a import function_a

print(f"✅ sample_package v{package_version} initialized")