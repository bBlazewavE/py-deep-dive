"""
sample_package.module_a - A module inside a package
Demonstrates module imports within packages.
"""

def function_a():
    """A simple function in module_a"""
    return "Hello from module_a.function_a()"

def call_module_b():
    """Demonstrates importing sibling modules"""
    # Relative import from sibling module
    from .module_b import function_b
    return f"module_a calling module_b: {function_b()}"

# Module-level variable
MODULE_A_CONSTANT = "I'm a constant in module_a"

print("🔧 module_a loaded")