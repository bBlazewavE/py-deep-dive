#!/usr/bin/env python3
"""
performance_test.py - Measure and analyze import performance
Shows the real cost of imports and optimization strategies.
"""

import sys
import time
import importlib
from contextlib import contextmanager


@contextmanager
def timer(description):
    """Context manager to time operations"""
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    print(f"{description}: {(end - start) * 1000:.3f}ms")


def clear_module_cache(modules):
    """Remove modules from sys.modules cache for testing"""
    for module in modules:
        if module in sys.modules:
            del sys.modules[module]


def test_import_performance():
    """Test the performance difference between first import and cached import"""
    print("🚀 Import Performance Analysis")
    print("=" * 50)
    
    # Test modules of different sizes
    test_modules = [
        'os',           # Medium-sized standard library module
        're',           # Medium-sized with compilation
        'datetime',     # Larger standard library module
        'collections',  # Complex module with many classes
        'json',         # JSON parsing module
        'urllib',       # Package with submodules
    ]
    
    print("\n📊 First Import vs Cached Import Times:")
    print("-" * 50)
    
    for module_name in test_modules:
        # Clear cache for fair measurement
        clear_module_cache([module_name])
        
        # Measure first import (slow)
        with timer(f"{module_name:12} (first)"):
            importlib.import_module(module_name)
        
        # Measure cached import (fast)  
        with timer(f"{module_name:12} (cached)"):
            importlib.import_module(module_name)
        
        print()


def test_lazy_imports():
    """Demonstrate lazy import patterns for performance"""
    print("\n💤 Lazy Import Patterns")
    print("-" * 30)
    
    def eager_function():
        """Function with eager imports - imports at module level"""
        import json
        import re
        import datetime
        return "Function with eager imports"
    
    def lazy_function():
        """Function with lazy imports - imports when needed"""
        def inner():
            import json
            import re  
            import datetime
            return "Function with lazy imports"
        return inner()
    
    # Clear cache to measure fairly
    clear_module_cache(['json', 're', 'datetime'])
    
    print("\nEager imports (imports happen at function definition):")
    with timer("Eager function call"):
        result1 = eager_function()
    
    # Clear cache again
    clear_module_cache(['json', 're', 'datetime'])
    
    print("\nLazy imports (imports happen when function is called):")
    with timer("Lazy function call"):
        result2 = lazy_function()
    
    print("\n💡 Lazy imports delay the cost until actually needed")
    print("   Good for: conditional features, error handling, optional dependencies")


def test_package_import_cost():
    """Show the cost difference between importing packages vs modules"""
    print("\n📦 Package vs Module Import Costs")
    print("-" * 40)
    
    # Clear any existing imports
    modules_to_clear = [
        'sample_package',
        'sample_package.module_a',
        'sample_package.module_b',
        'sample_package.subpackage',
        'sample_package.subpackage.sub_module'
    ]
    clear_module_cache(modules_to_clear)
    
    # Add current directory to path so we can import our sample_package
    current_dir = str(Path.cwd()) if 'Path' in globals() else '.'
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        print("Importing just the package:")
        with timer("import sample_package"):
            import sample_package
        
        print("\nImporting a specific module:")
        with timer("from sample_package import module_a"):
            from sample_package import module_a
            
        print("\nImporting from subpackage:")
        with timer("from sample_package.subpackage import sub_module"):
            from sample_package.subpackage import sub_module
            
    except ImportError as e:
        print(f"⚠️  Could not import sample_package: {e}")
        print("   (Make sure you're running from the 05-import-system directory)")


def analyze_startup_cost():
    """Analyze the startup cost of importing many modules"""
    print("\n⏱️ Startup Cost Analysis")
    print("-" * 30)
    
    # Simulate an application with many imports
    heavy_imports = [
        'os', 'sys', 're', 'json', 'datetime', 'collections',
        'itertools', 'functools', 'pathlib', 'urllib', 'socket',
        'threading', 'subprocess', 'tempfile'
    ]
    
    # Clear cache
    clear_module_cache(heavy_imports)
    
    print(f"Importing {len(heavy_imports)} common modules:")
    start_time = time.perf_counter()
    
    for module_name in heavy_imports:
        importlib.import_module(module_name)
    
    total_time = time.perf_counter() - start_time
    
    print(f"Total import time: {total_time * 1000:.1f}ms")
    print(f"Average per module: {(total_time / len(heavy_imports)) * 1000:.1f}ms")
    print(f"Modules in cache: {len([m for m in heavy_imports if m in sys.modules])}")
    
    print("\n💡 Optimization strategies:")
    print("   1. Import only what you need")
    print("   2. Use lazy imports for optional features")
    print("   3. Consider import order for dependencies")
    print("   4. Profile your application's import bottlenecks")


def demonstrate_import_hooks():
    """Show how import hooks work (advanced topic)"""
    print("\n🪝 Import Hooks (Advanced)")
    print("-" * 30)
    
    print("Current meta path finders:")
    for i, finder in enumerate(sys.meta_path):
        print(f"  {i+1}. {finder}")
    
    print(f"\nPath hooks: {len(sys.path_hooks)} registered")
    
    print("\n💡 Import hooks allow you to:")
    print("   - Import modules from non-standard locations")
    print("   - Transform code during import")
    print("   - Implement custom module loading logic")
    print("   - Add debugging/logging to imports")


if __name__ == "__main__":
    print("🐍 Python Import System - Performance Analysis")
    print("Understanding the real cost of imports")
    
    test_import_performance()
    test_lazy_imports()
    test_package_import_cost()
    analyze_startup_cost()
    demonstrate_import_hooks()
    
    print("\n" + "=" * 60)
    print("📈 Performance Analysis Complete!")
    print("   Key takeaway: First imports are expensive, cached imports are free")
    print("=" * 60)