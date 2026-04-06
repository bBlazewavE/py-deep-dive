#!/usr/bin/env python3
"""
The Import System - How Python Finds Your Code
Interactive exploration of Python's import machinery
"""

import sys
import time
import importlib
import importlib.util
from pathlib import Path


def header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)


def section(text):
    """Print a formatted section"""
    print(f"\n--- {text} ---")


def explore_sys_modules():
    """Demonstrate the sys.modules cache"""
    header("SYS.MODULES CACHE - Python's Import Memory")
    
    print("sys.modules is Python's import cache - a dictionary of all imported modules.")
    print(f"Currently loaded modules: {len(sys.modules)}")
    
    # Show some built-in modules that are always loaded
    builtin_modules = [name for name in sys.modules if not '.' in name][:10]
    print(f"\nSome loaded modules: {builtin_modules}")
    
    section("First-time import (slow)")
    module_name = 'json'
    
    # Remove from cache to demonstrate first import
    if module_name in sys.modules:
        print(f"'{module_name}' is already cached, removing for demo...")
        del sys.modules[module_name]
    
    start_time = time.perf_counter()
    import json  # This will be slow (relatively)
    first_import_time = time.perf_counter() - start_time
    
    print(f"First import of '{module_name}': {first_import_time*1000:.3f}ms")
    print(f"Module object: {json}")
    print(f"Module file: {json.__file__}")
    
    section("Cached import (fast)")
    start_time = time.perf_counter()
    import json as json_again  # This uses cache
    cached_import_time = time.perf_counter() - start_time
    
    print(f"Cached import: {cached_import_time*1000:.3f}ms")
    print(f"Speed improvement: {first_import_time/cached_import_time:.1f}x faster")
    print(f"Same object? {json is json_again}")
    print(f"sys.modules['json']: {sys.modules['json']}")


def explore_sys_path():
    """Demonstrate module search path"""
    header("SYS.PATH - Where Python Looks for Modules")
    
    print("sys.path determines where Python searches for modules.")
    print("Python searches these directories in order:")
    
    for i, path in enumerate(sys.path):
        print(f"  {i+1}. {path}")
    
    section("Adding custom search paths")
    print("You can modify sys.path at runtime:")
    
    # Add current directory if not already there
    current_dir = str(Path.cwd())
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"Added '{current_dir}' to sys.path")
    
    print("\nPYTHONPATH environment variable also adds to sys.path")
    print("Example: export PYTHONPATH=/my/custom/modules:$PYTHONPATH")


def explore_import_types():
    """Demonstrate different import syntaxes"""
    header("IMPORT TYPES - Different Ways to Import")
    
    section("1. Module import")
    print("import os")
    print("  - Imports entire module")
    print("  - Access with: os.path.join()")
    
    section("2. Function import") 
    print("from os.path import join")
    print("  - Imports specific function")
    print("  - Access with: join()")
    
    section("3. Alias import")
    print("import numpy as np")
    print("  - Imports with custom name")
    print("  - Access with: np.array()")
    
    section("4. Star import (avoid!)")
    print("from os import *")
    print("  - Imports everything into namespace")
    print("  - Can cause name conflicts")
    print("  - Makes code hard to understand")
    
    section("5. Dynamic import")
    print("Using importlib for runtime imports:")
    
    # Dynamic import example
    module_name = 'datetime'
    dynamic_module = importlib.import_module(module_name)
    print(f"Dynamically imported: {dynamic_module}")
    print(f"Module name from variable: {module_name}")


def demonstrate_circular_imports():
    """Show how Python handles circular imports"""
    header("CIRCULAR IMPORTS - When Modules Import Each Other")
    
    print("Circular imports happen when modules import each other.")
    print("Python can handle some cases, but not all.")
    
    # Create temporary circular modules for demonstration
    circular_a_code = '''
# circular_a.py
print("Loading circular_a...")
from circular_b import b_function

def a_function():
    return "Function from A"

print("circular_a loaded!")
'''
    
    circular_b_code = '''
# circular_b.py  
print("Loading circular_b...")
from circular_a import a_function

def b_function():
    return "Function from B"

print("circular_b loaded!")
'''
    
    print("\nExample circular import scenario:")
    print("circular_a.py imports from circular_b")
    print("circular_b.py imports from circular_a")
    print("\nThis can cause ImportError or AttributeError!")
    
    print("\nSolutions:")
    print("1. Restructure to avoid circular dependencies")
    print("2. Move imports inside functions (lazy import)")
    print("3. Import the module, not specific functions")
    print("4. Use a third module for shared functionality")


def explore_package_structure():
    """Explain packages vs modules"""
    header("PACKAGES VS MODULES - Organizing Python Code")
    
    print("Module: A single .py file")
    print("Package: A directory containing modules + __init__.py")
    
    section("Package structure example")
    package_structure = """
mypackage/
    __init__.py      # Makes it a package
    module1.py       # Module inside package
    module2.py       # Another module
    subpackage/      # Nested package
        __init__.py
        submodule.py
"""
    print(package_structure)
    
    section("Import examples")
    print("import mypackage                    # Import package")
    print("from mypackage import module1       # Import module from package") 
    print("from mypackage.subpackage import submodule  # Nested import")
    
    print("\n__init__.py controls what gets imported:")
    print("- Empty __init__.py: Package is importable but empty")
    print("- With code: Runs when package is first imported")
    print("- __all__ = [...]: Controls what 'from package import *' imports")


def show_import_internals():
    """Show the internal import process"""
    header("IMPORT INTERNALS - What Happens Under the Hood")
    
    print("When you write 'import mymodule', Python:")
    print("1. Checks if 'mymodule' is in sys.modules cache")
    print("2. If cached: return the cached module object")
    print("3. If not cached:")
    print("   a. Search sys.path directories for 'mymodule.py'")
    print("   b. Create a new module object")
    print("   c. Compile and execute the module code")
    print("   d. Add the module to sys.modules cache")
    print("   e. Return the module object")
    
    section("Import hooks and finders")
    print("Python uses 'finders' and 'loaders' to customize imports:")
    print(f"Meta path: {sys.meta_path}")
    print("\nThis allows:")
    print("- Importing from ZIP files")
    print("- Network imports")
    print("- Database imports")
    print("- Custom module transformations")


def performance_analysis():
    """Analyze import performance"""
    header("IMPORT PERFORMANCE - Speed Matters")
    
    print("Import costs:")
    print("1. First import: File I/O + Compilation + Execution")
    print("2. Cached import: Dictionary lookup (very fast)")
    print("3. Large modules: Can slow startup significantly")
    
    section("Measuring import times")
    modules_to_test = ['os', 're', 'datetime', 'collections']
    
    for module_name in modules_to_test:
        # Remove from cache for fair timing
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        start_time = time.perf_counter()
        importlib.import_module(module_name)
        import_time = time.perf_counter() - start_time
        
        print(f"{module_name:12}: {import_time*1000:6.3f}ms")
    
    section("Optimization strategies")
    print("1. Lazy imports: Import inside functions when needed")
    print("2. Conditional imports: Only import what's actually used")
    print("3. Import grouping: Import related modules together")
    print("4. Preloading: Import heavy modules at startup, not during requests")


def debugging_imports():
    """Show import debugging techniques"""
    header("DEBUGGING IMPORTS - When Things Go Wrong")
    
    print("Common import problems and solutions:")
    
    problems = [
        ("ModuleNotFoundError", "Check sys.path and module spelling"),
        ("ImportError: cannot import name", "Check if name exists in module"),
        ("Circular import", "Restructure dependencies or use lazy imports"),
        ("AttributeError after import", "Module may not be fully initialized"),
    ]
    
    for problem, solution in problems:
        print(f"• {problem}: {solution}")
    
    section("Debugging tools")
    print("1. python -v: Verbose import output")
    print("2. python -X importtime: Show import timing")
    print("3. importlib.util.find_spec(): Check if module can be found")
    print("4. sys.modules.keys(): See what's loaded")
    print("5. module.__file__: See where module was loaded from")
    
    # Demonstrate find_spec
    print(f"\nExample - Finding 'os' module:")
    spec = importlib.util.find_spec('os')
    if spec:
        print(f"Found: {spec.origin}")
    else:
        print("Not found!")


def advanced_topics():
    """Cover advanced import concepts"""
    header("ADVANCED TOPICS - For the Curious")
    
    section("1. Import hooks")
    print("Customize the import process:")
    print("- sys.meta_path: Module finders")
    print("- sys.path_hooks: Path entry finders")
    print("- importlib.abc: Abstract base classes for custom importers")
    
    section("2. Reloading modules")
    print("importlib.reload(module) - Reload a module")
    print("⚠️  Dangerous! Can break references and cause bugs")
    
    section("3. Import from arbitrary paths")
    print("Load modules from specific file paths:")
    print("spec = importlib.util.spec_from_file_location('name', 'path')")
    print("module = importlib.util.module_from_spec(spec)")
    print("spec.loader.exec_module(module)")
    
    section("4. Bytecode compilation")
    print("Python compiles .py files to .pyc bytecode")
    print("Located in __pycache__ directories")
    print("Speeds up subsequent imports of the same file")


def main():
    """Run all explorations"""
    print("🐍 Python Import System Deep Dive")
    print("Understanding how Python finds and loads your code")
    
    explore_sys_modules()
    explore_sys_path()
    explore_import_types()
    demonstrate_circular_imports()
    explore_package_structure()
    show_import_internals()
    performance_analysis()
    debugging_imports()
    advanced_topics()
    
    print("\n" + "="*60)
    print("  🎓 Import System Mastery Complete!")
    print("     You now understand how Python finds your code.")
    print("="*60)


if __name__ == "__main__":
    main()