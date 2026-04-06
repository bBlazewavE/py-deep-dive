"""
sample_package.subpackage - A subpackage demonstration
Shows how packages can be nested.
"""

print("📦 Initializing subpackage...")

# Import from sub_module and make it available at subpackage level
from .sub_module import sub_function

subpackage_info = {
    "name": "subpackage",
    "level": "nested",
    "parent": "sample_package"
}

print("✅ subpackage initialized")