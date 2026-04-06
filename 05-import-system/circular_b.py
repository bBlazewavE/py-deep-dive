"""
circular_b.py - Demonstrates circular import issues  
This module imports from circular_a, which imports from this module.
"""

print("🔄 Loading circular_b...")

# This import will cause circular dependency
try:
    from circular_a import function_from_a
    print("✅ Successfully imported function_from_a")
except ImportError as e:
    print(f"❌ Import failed: {e}")

def function_from_b():
    """A function that can be imported by circular_a"""
    return "Hello from module B!"

# This will only work if circular_a successfully imports
def use_function_from_a():
    """Try to use function from circular_a"""
    try:
        result = function_from_a()
        return f"B says: {result}"
    except NameError:
        return "B says: function_from_a is not available (circular import issue)"

print("✅ circular_b loaded successfully")