"""
sample_package.subpackage.sub_module - A module in a subpackage
Demonstrates deeply nested package structures.
"""

def sub_function():
    """A function in the subpackage"""
    return "Hello from subpackage.sub_module.sub_function()"

def call_parent_package():
    """Demonstrates importing from parent packages"""
    # Import from parent package (going up the hierarchy)
    from ...sample_package.module_a import function_a
    return f"sub_module calling parent: {function_a()}"

# This shows where we are in the package hierarchy
MODULE_PATH = "sample_package.subpackage.sub_module"

print("🔧 sub_module loaded")