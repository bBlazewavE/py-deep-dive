#!/usr/bin/env python3
"""01 — Everything is an Object: Explore & Prove It"""

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# ── 1. Everything has an id and a type ──────────────────────
section("Everything has id() and type()")

things = [42, 3.14, "hello", [1,2], {"a": 1}, None, print, int, type]
for thing in things:
    print(f"  {str(thing):30s}  type={type(thing).__name__:30s}  id={id(thing)}")

# ── 2. Variables are references, not boxes ──────────────────
section("Variables are references")

a = [1, 2, 3]
b = a
print(f"  a = [1, 2, 3]")
print(f"  b = a")
print(f"  id(a) = {id(a)}")
print(f"  id(b) = {id(b)}")
print(f"  a is b → {a is b}  (same object!)")
print()
b.append(4)
print(f"  b.append(4)")
print(f"  a = {a}  ← a changed too, because a and b point to the SAME list")

# ── 3. is vs == ─────────────────────────────────────────────
section("is vs == (identity vs equality)")

x = [1, 2, 3]
y = [1, 2, 3]
print(f"  x = [1, 2, 3]    id={id(x)}")
print(f"  y = [1, 2, 3]    id={id(y)}")
print(f"  x == y → {x == y}   (same value)")
print(f"  x is y → {x is y}  (different objects)")

# ── 4. Integer interning ────────────────────────────────────
section("🤯 Integer Interning (-5 to 256)")

for val in [0, 100, 256, 257, -5, -6, 1000]:
    a = val
    b = val
    # Force fresh objects by computing
    a = val + 0  # CPython may still intern for small ints
    b = val + 0
    # More reliable: use int() to force new object for large vals
    a = int(str(val))
    b = int(str(val))
    cached = a is b
    print(f"  {val:>5d}: a is b → {str(cached):5s}  {'(cached!)' if cached else '(separate objects)'}")

print("\n  Note: Small integers are pre-allocated singletons in CPython.")
print("  Never use 'is' to compare numbers in real code!")

# ── 5. None is a singleton ──────────────────────────────────
section("None is a singleton")

a = None
b = None
print(f"  a = None, b = None")
print(f"  a is b → {a is b}")
print(f"  id(a) = {id(a)}, id(b) = {id(b)}")
print(f"  There is only ONE None object in all of Python.")

# ── 6. Functions are objects too ─────────────────────────────
section("Functions are objects")

def greet(name):
    """Say hello"""
    return f"Hello, {name}!"

print(f"  type(greet)       = {type(greet)}")
print(f"  id(greet)         = {id(greet)}")
print(f"  greet.__name__    = {greet.__name__}")
print(f"  greet.__doc__     = {greet.__doc__}")
print(f"  greet('World')    = {greet('World')}")

# You can assign functions to variables
say_hi = greet
print(f"\n  say_hi = greet")
print(f"  say_hi is greet   → {say_hi is greet}")
print(f"  say_hi('Python')  = {say_hi('Python')}")

# ── 7. type of type ─────────────────────────────────────────
section("🤯 type(type) = type")

print(f"  type(int)    = {type(int)}")
print(f"  type(str)    = {type(str)}")
print(f"  type(type)   = {type(type)}")
print(f"  type(object) = {type(object)}")
print(f"\n  It's types all the way down. 'type' is its own type.")
print(f"  isinstance(type, object) → {isinstance(type, object)}")
print(f"  isinstance(object, type) → {isinstance(object, type)}")

print(f"\n{'='*60}")
print("  ✅ Done! Everything in Python is an object.")
print(f"{'='*60}\n")
