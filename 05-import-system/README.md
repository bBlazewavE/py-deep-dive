# 05: The Import System - How Python Finds Your Code

**Ever wondered what happens when you write `import numpy`? How does Python find it among thousands of packages?**

This deep dive explains Python's import machinery — the hidden system that makes `import` statements work.

## 🎯 What You'll Learn

- **Module Resolution**: How Python searches for and finds modules
- **sys.modules Cache**: Why imports are lightning-fast after the first time  
- **Circular Imports**: How Python handles mutual dependencies
- **Package vs Module**: The difference and why it matters
- **Import Hooks**: How to customize the import process
- **Performance**: Why imports can be slow and how to optimize
- **Debugging**: Tools and techniques for import issues

## 🚀 Run the Examples

```bash
python3 05-import-system/explore.py
```

## 📊 The Import Process (Simplified)

```
import mymodule
     ⬇
1. Check sys.modules cache
     ⬇ (if not cached)
2. Search sys.path directories
     ⬇ (when found)
3. Create module object
     ⬇
4. Execute module code
     ⬇
5. Add to sys.modules
     ⬇
6. Bind to local namespace
```

## 🔍 Key Concepts

### Module Cache (sys.modules)
- **First import**: Module is loaded and executed
- **Subsequent imports**: Retrieved from cache (O(1) lookup)
- **Memory sharing**: Same module object across all imports

### Module Search Path (sys.path)
```python
import sys
print(sys.path)
# ['/current/directory', '/usr/lib/python3.9', '/usr/lib/python3.9/site-packages', ...]
```

### Import Types
- **Absolute**: `import package.module`
- **Relative**: `from .sibling import something` 
- **Dynamic**: `importlib.import_module('module_name')`

## ⚡ Performance Implications

- **First import**: File I/O + compilation + execution
- **Cached import**: Dictionary lookup only
- **Circular imports**: Can cause startup delays
- **Large modules**: Consider lazy loading

## 🐛 Common Issues

1. **ModuleNotFoundError**: Check sys.path and PYTHONPATH
2. **Circular imports**: Restructure or use lazy imports
3. **Import order**: Dependencies must be imported first
4. **Package structure**: Missing `__init__.py` files

## 🧪 Experiments in This Directory

- `explore.py` - Interactive import system exploration
- `circular_a.py`, `circular_b.py` - Circular import demonstration  
- `sample_package/` - Package structure examples
- `performance_test.py` - Import timing measurements

## 💡 Why This Knowledge Matters

Understanding the import system helps with:
- **Architecture decisions** (avoiding circular dependencies)
- **Performance optimization** (lazy loading strategies)
- **Debugging complex codebases** (import resolution issues)
- **Package design** (clean module boundaries)
- **Deployment issues** (PYTHONPATH configuration)
- **Interview preparation** (deep technical questions)

**This knowledge transforms you from someone who "imports and hopes" to someone who understands and controls the process.**