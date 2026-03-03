#!/usr/bin/env python3
"""02 — Memory Model: References, Counting, and the GC"""

import sys
import gc
import weakref

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# ── 1. Reference counting ───────────────────────────────────
section("Reference Counting with sys.getrefcount()")

x = [1, 2, 3]
print(f"  x = [1, 2, 3]")
print(f"  sys.getrefcount(x) = {sys.getrefcount(x)}  (includes the arg to getrefcount)")

y = x
print(f"  y = x")
print(f"  sys.getrefcount(x) = {sys.getrefcount(x)}  (one more reference)")

z = [x, x, x]
print(f"  z = [x, x, x]")
print(f"  sys.getrefcount(x) = {sys.getrefcount(x)}  (three more references from z)")

del y
del z
print(f"  del y; del z")
print(f"  sys.getrefcount(x) = {sys.getrefcount(x)}  (back to baseline)")

# ── 2. Circular references ──────────────────────────────────
section("Circular References (the refcount killer)")

gc.collect()  # Clean slate
gc.set_debug(0)

# Create a cycle
a = {"name": "a"}
b = {"name": "b"}
a["partner"] = b
b["partner"] = a

id_a, id_b = id(a), id(b)
print(f"  a['partner'] = b, b['partner'] = a  (cycle created)")
print(f"  id(a) = {id_a}")
print(f"  id(b) = {id_b}")

del a
del b
print(f"\n  del a; del b — but the cycle keeps them alive!")

# Before GC
unreachable_before = gc.collect()
print(f"  gc.collect() freed {unreachable_before} unreachable objects")
print(f"  The garbage collector detected and broke the cycle! 🧹")

# ── 3. GC generations ───────────────────────────────────────
section("Generational GC Stats")

stats = gc.get_stats()
for i, gen in enumerate(stats):
    print(f"  Generation {i}: {gen}")

thresholds = gc.get_threshold()
print(f"\n  Collection thresholds: {thresholds}")
print(f"  (Gen0 collects every ~{thresholds[0]} allocations,")
print(f"   Gen1 every ~{thresholds[1]} Gen0 collections,")
print(f"   Gen2 every ~{thresholds[2]} Gen1 collections)")

# ── 4. Weak references ──────────────────────────────────────
section("Weak References")

class HeavyObject:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"HeavyObject({self.name!r})"

obj = HeavyObject("big-data")
weak = weakref.ref(obj)

print(f"  obj = HeavyObject('big-data')")
print(f"  weak = weakref.ref(obj)")
print(f"  weak()        = {weak()}")
print(f"  weak() is obj = {weak() is obj}")
print(f"  sys.getrefcount(obj) = {sys.getrefcount(obj)}")
print(f"  (weak ref does NOT increase refcount!)")

del obj
print(f"\n  del obj")
print(f"  weak() = {weak()}  ← object was collected!")

# ── 5. WeakValueDictionary (smart cache) ────────────────────
section("WeakValueDictionary — A Cache That Doesn't Leak")

cache = weakref.WeakValueDictionary()

def load_data(key):
    """Simulate loading heavy data"""
    data = HeavyObject(key)
    cache[key] = data
    return data

result = load_data("users")
print(f"  Loaded: cache['users'] = {cache.get('users')}")
print(f"  Cache size: {len(cache)}")

del result
gc.collect()
print(f"\n  del result; gc.collect()")
print(f"  cache.get('users') = {cache.get('users')}  ← auto-evicted!")
print(f"  Cache size: {len(cache)}")
print(f"\n  💡 WeakValueDictionary = cache that cleans itself up")

# ── 6. tracemalloc ───────────────────────────────────────────
section("Bonus: tracemalloc (memory profiling)")

import tracemalloc
tracemalloc.start()

# Do some allocations
data = [list(range(1000)) for _ in range(100)]

snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")[:3]

print("  Top 3 memory allocations:")
for stat in top:
    print(f"    {stat}")

tracemalloc.stop()

print(f"\n{'='*60}")
print("  ✅ Done! Now you know how Python manages memory.")
print(f"{'='*60}\n")
