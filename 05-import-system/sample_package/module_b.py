"""
sample_package.module_b - Another module inside the package
Shows different import patterns within packages.
"""

def function_b():
    """A simple function in module_b"""
    return "Hello from module_b.function_b()"

def call_subpackage():
    """Demonstrates importing from subpackages"""
    # Import from subpackage
    from .subpackage.sub_module import sub_function
    return f"module_b calling subpackage: {sub_function()}"

class ClassB:
    """A simple class in module_b"""
    
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"ClassB says: Hello, {self.name}!"

# Module-level variable
MODULE_B_DATA = {"type": "demo", "version": 2}

print("⚙️ module_b loaded")