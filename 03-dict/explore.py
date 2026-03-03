#!/usr/bin/env python3
"""03 — How Dicts Actually Work: Explore Hash Tables"""

import sys

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# ── 1. hash() basics ────────────────────────────────────────
section("hash() — The Foundation of Dicts")

examples = [0, 1, 42, -1, -2, 256, 1000, 3.14, "hello", "world", (1, 2), True, False]
for val in examples:
    print(f"  hash({val!r:15s}) = {hash(val)}")

print(f"\n  🤯 Notice: hash(42) == 42, hash(True) == 1, hash(-1) == -2")
print(f"     Integers hash to themselves (except -1)!")

# ── 2. Hash collisions ──────────────────────────────────────
section("Hash Collisions (same slot, different keys)")

# Demonstrate that different objects can have the same slot
table_size = 8
keys = ["name", "age", "city", "email", "phone", "role", "team", "id"]
print(f"  Simulating a hash table with {table_size} slots:\n")
for key in keys:
    h = hash(key)
    slot = h % table_size
    print(f"  hash({key!r:10s}) % {table_size} = slot {slot}  (hash={h})")

print(f"\n  Any duplicated slot numbers = collision → Python probes for next open slot")

# ── 3. Dict memory growth ───────────────────────────────────
section("Dict Memory Growth (watch it resize!)")

d = {}
prev_size = sys.getsizeof(d)
print(f"  {'Items':>6s}  {'Size (bytes)':>14s}  {'Change':>10s}")
print(f"  {'─'*6}  {'─'*14}  {'─'*10}")
print(f"  {0:>6d}  {prev_size:>14d}  {'(empty)':>10s}")

for i in range(1, 30):
    d[f"key_{i}"] = i
    size = sys.getsizeof(d)
    change = size - prev_size
    marker = " ← RESIZE!" if change > 0 else ""
    print(f"  {i:>6d}  {size:>14d}  {change:>+10d}{marker}")
    prev_size = size

print(f"\n  Notice: size jumps happen at ~2/3 capacity (the load factor threshold)")

# ── 4. Insertion order preservation ──────────────────────────
section("Insertion Order (guaranteed since 3.7)")

d = {}
for fruit in ["banana", "apple", "cherry", "date", "elderberry"]:
    d[fruit] = len(fruit)

print(f"  Inserted: banana → apple → cherry → date → elderberry")
print(f"  Keys:     {list(d.keys())}")
print(f"  Order preserved ✅")

# ── 5. Key requirements ─────────────────────────────────────
section("What Can Be a Dict Key?")

print("  Keys must be hashable (immutable, typically):\n")
valid_keys = {
    42: "int",
    3.14: "float",
    "hello": "str",
    (1, 2): "tuple",
    True: "bool",
    None: "NoneType",
    frozenset({1,2}): "frozenset",
}
for k, v in valid_keys.items():
    print(f"  ✅ {v:12s} → {k!r}")

print(f"\n  ❌ Lists, dicts, sets → unhashable (mutable) → can't be keys")
try:
    {[1,2]: "nope"}
except TypeError as e:
    print(f"     {{[1,2]: 'nope'}} → TypeError: {e}")

# ── 6. hash(-1) quirk ───────────────────────────────────────
section("🤯 The hash(-1) == -2 Quirk")

print(f"  hash(-1) = {hash(-1)}")
print(f"  hash(-2) = {hash(-2)}")
print(f"\n  In CPython's C code, -1 signals an error.")
print(f"  So if a hash function returns -1, CPython replaces it with -2.")
print(f"  This means -1 and -2 collide more than you'd expect!")

# ── 7. Practical: dict vs alternatives ──────────────────────
section("Memory: dict vs __slots__ vs namedtuple")

from collections import namedtuple

class PointDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSlots:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

PointNT = namedtuple("PointNT", ["x", "y"])

pd = PointDict(1, 2)
ps = PointSlots(1, 2)
pn = PointNT(1, 2)

print(f"  Regular class:    {sys.getsizeof(pd)} + {sys.getsizeof(pd.__dict__)} (instance + __dict__) = {sys.getsizeof(pd) + sys.getsizeof(pd.__dict__)} bytes")
print(f"  __slots__ class:  {sys.getsizeof(ps)} bytes (no __dict__!)")
print(f"  namedtuple:       {sys.getsizeof(pn)} bytes")
print(f"\n  💡 For millions of small objects, __slots__ saves massive memory")

print(f"\n{'='*60}")
print("  ✅ Done! Now you know how Python dicts work under the hood.")
print(f"{'='*60}\n")
