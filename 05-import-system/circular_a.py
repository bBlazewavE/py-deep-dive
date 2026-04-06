"""
circular_a.py - Demonstrates circular import issues
This module imports from circular_b, which imports from this module.
"""

print("🔄 Loading circular_a...")

# This import will cause circular dependency
try:
    from circular_b import function_from_b
    print("✅ Successfully imported function_from_b")
except ImportError as e:
    print(f"❌ Import failed: {e}")

def function_from_a():
    """A function that can be imported by circular_b"""
    return "Hello from module A!"

# This will only work if circular_b successfully imports
def use_function_from_b():
    """Try to use function from circular_b"""
    try:
        result = function_from_b()
        return f"A says: {result}"
    except NameError:
        return "A says: function_from_b is not available (circular import issue)"

print("✅ circular_a loaded successfully")