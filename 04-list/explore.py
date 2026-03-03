#!/usr/bin/env python3
"""04 — Lists: Dynamic Arrays Under the Hood"""

import sys
import timeit
from collections import deque

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# ── 1. Over-allocation pattern ───────────────────────────────
section("List Growth: Watch the Over-Allocation")

lst = []
prev_size = sys.getsizeof(lst)
print(f"  {'Items':>6s}  {'Size (bytes)':>14s}  {'Change':>10s}  {'Allocated':>10s}")
print(f"  {'─'*6}  {'─'*14}  {'─'*10}  {'─'*10}")
print(f"  {0:>6d}  {prev_size:>14d}  {'(empty)':>10s}  {'~0':>10s}")

for i in range(1, 40):
    lst.append(i)
    size = sys.getsizeof(lst)
    change = size - prev_size
    # Approximate allocated slots: (size - base_size) / pointer_size
    base = sys.getsizeof([])
    allocated = (size - base) // 8
    marker = " ← RESIZE!" if change > 0 else ""
    print(f"  {i:>6d}  {size:>14d}  {change:>+10d}  {allocated:>10d}{marker}")
    prev_size = size

print(f"\n  Notice: resizes happen less frequently as the list grows")
print(f"  That's the over-allocation strategy → amortized O(1) append")

# ── 2. List vs Tuple memory ─────────────────────────────────
section("List vs Tuple: Memory Comparison")

for n in [0, 1, 3, 5, 10, 100]:
    lst = list(range(n))
    tup = tuple(range(n))
    ls = sys.getsizeof(lst)
    ts = sys.getsizeof(tup)
    savings = ls - ts
    print(f"  {n:>3d} items:  list={ls:>5d}B  tuple={ts:>5d}B  saved={savings:>4d}B ({savings/max(ls,1)*100:.0f}%)")

print(f"\n  💡 Tuples have no over-allocation, no resize machinery")

# ── 3. Append vs Insert(0) benchmark ────────────────────────
section("append() vs insert(0) — O(1) vs O(n)")

sizes = [1000, 5000, 10000, 50000]
print(f"  {'N':>7s}  {'append (ms)':>12s}  {'insert(0) (ms)':>16s}  {'Ratio':>8s}")
print(f"  {'─'*7}  {'─'*12}  {'─'*16}  {'─'*8}")

for n in sizes:
    t_append = timeit.timeit(
        "lst.append(1)",
        setup="lst = list(range({}))".format(n),
        number=10000
    ) * 1000

    t_insert = timeit.timeit(
        "lst.insert(0, 1)",
        setup="lst = list(range({}))".format(n),
        number=10000
    ) * 1000

    ratio = t_insert / max(t_append, 0.001)
    print(f"  {n:>7d}  {t_append:>12.3f}  {t_insert:>16.3f}  {ratio:>7.1f}x")

print(f"\n  insert(0) gets SLOWER with size — it shifts every element!")

# ── 4. deque vs list for left operations ─────────────────────
section("deque vs list: appendleft/popleft")

n = 50000
t_list = timeit.timeit(
    "lst.insert(0, 1)",
    setup="lst = []",
    number=n
) * 1000

t_deque = timeit.timeit(
    "d.appendleft(1)",
    setup="from collections import deque; d = deque()",
    number=n
) * 1000

print(f"  {n} left-appends:")
print(f"    list.insert(0, x):   {t_list:>10.1f} ms")
print(f"    deque.appendleft(x): {t_deque:>10.1f} ms")
print(f"    deque is {t_list/max(t_deque,0.001):.0f}x faster! 🚀")

# ── 5. Comprehension vs append loop ─────────────────────────
section("List Comprehension vs Append Loop")

n = 100000

t_comp = timeit.timeit(
    "[i*2 for i in range(n)]",
    globals={"n": n},
    number=100
) * 1000

t_loop = timeit.timeit(
    """
lst = []
for i in range(n):
    lst.append(i*2)
""",
    globals={"n": n},
    number=100
) * 1000

print(f"  Building list of {n} items (×100 runs):")
print(f"    Comprehension: {t_comp:>8.1f} ms")
print(f"    Append loop:   {t_loop:>8.1f} ms")
print(f"    Comprehension is {t_loop/t_comp:.1f}x faster")
print(f"\n  💡 Comprehensions skip the attribute lookup for .append()")

# ── 6. array.array vs list ──────────────────────────────────
section("array.array vs list (homogeneous data)")

import array

n = 10000
lst = list(range(n))
arr = array.array("l", range(n))

print(f"  {n} integers:")
print(f"    list:        {sys.getsizeof(lst):>8d} bytes")
print(f"    array('l'):  {sys.getsizeof(arr):>8d} bytes")
print(f"    Savings:     {sys.getsizeof(lst) - sys.getsizeof(arr):>8d} bytes ({(1 - sys.getsizeof(arr)/sys.getsizeof(lst))*100:.0f}%)")
print(f"\n  array stores raw C values — no Python object overhead per element")

print(f"\n{'='*60}")
print("  ✅ Done! Now you know how Python lists really work.")
print(f"{'='*60}\n")
