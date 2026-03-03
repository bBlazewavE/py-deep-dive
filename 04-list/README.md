# 04 — Lists: Dynamic Arrays Under the Hood 📦

Python lists look simple, but they're backed by a carefully engineered **dynamic array** with a clever growth strategy.

## What's Inside a List?

A Python list is NOT a linked list. It's a **contiguous array of pointers**:

```
  my_list = ["a", "b", "c"]

  list object:
  ┌────────────────────────┐
  │ ob_refcnt: 1           │
  │ ob_type: <list>        │
  │ ob_size: 3  (length)   │
  │ allocated: 4  (capacity)│
  │ ob_item ──────────────────► ┌─────┬─────┬─────┬─────┐
  └────────────────────────┘    │ ptr │ ptr │ ptr │ --- │
                                │  │  │  │  │  │  │empty│
                                └──┼──┴──┼──┴──┼──┴─────┘
                                   ▼     ▼     ▼
                                 "a"   "b"   "c"
```

Key distinction: the list stores **pointers** to objects, not the objects themselves. That's why a list can hold mixed types.

## The Over-Allocation Strategy

When you `append()` to a full list, Python doesn't grow by just 1 — it **over-allocates** to make future appends cheap:

```
  Growth pattern (CPython):
  new_size = old_size + (old_size >> 3) + (6 if old_size >= 9 else 3)

  Size 0  → allocate 4
  Size 4  → allocate 8
  Size 8  → allocate 16
  Size 16 → allocate 25
  Size 25 → allocate 35
  ...grows by ~12.5% each time
```

This gives **amortized O(1)** append time. Most appends just write to pre-allocated space. Occasionally one triggers a resize (O(n) copy), but spread across all appends, the average cost is O(1).

```
  Append #1-4:   Write to slot, no resize        O(1)
  Append #5:     RESIZE (copy 4 items to new array of 8) + write  O(n)
  Append #6-8:   Write to slot, no resize        O(1)
  Append #9:     RESIZE again                    O(n)

  Average across all appends: O(1) ← amortized!
```

## List vs Tuple: Memory

Tuples are immutable, so Python optimizes them differently:

```
  list  = pointer array + over-allocation + size tracking
  tuple = pointer array + NOTHING ELSE (exact size, no slack)

  [1, 2, 3]  → ~120 bytes (list overhead + slack space)
  (1, 2, 3)  →  ~72 bytes (minimal, exact-fit)
```

Also: Python **caches** small tuples. Creating an empty tuple `()` always returns the same object. Tuples of length 1-20 are recycled from a free list.

## Operations & Their True Cost

| Operation | Average | Why |
|-----------|---------|-----|
| `lst[i]` | O(1) | Direct pointer lookup (base + offset) |
| `lst.append(x)` | O(1)* | Amortized — usually writes to slack space |
| `lst.insert(0, x)` | O(n) | Must shift every element right |
| `lst.pop()` | O(1) | Remove last element, no shifting |
| `lst.pop(0)` | O(n) | Must shift every element left |
| `x in lst` | O(n) | Linear scan, no hash table |
| `lst.sort()` | O(n log n) | Timsort — hybrid merge/insertion sort |

## 🤯 Mind-Blowing Fact

`collections.deque` uses a **doubly-linked list of fixed-size blocks** — making both `appendleft()` and `append()` true O(1). If you're doing `lst.insert(0, x)` or `lst.pop(0)` in a loop, switch to deque immediately:

```python
from collections import deque
d = deque()
d.appendleft("fast!")  # O(1), not O(n)
```

## 💡 Staff Engineer Insight

- **Pre-allocate when you know the size**: `[None] * n` is faster than appending n times — avoids all the resizes
- **List comprehensions are faster than append loops** — CPython optimizes the bytecode for comprehensions (uses `LIST_APPEND` opcode, skips attribute lookup)
- **`extend()` > loop of `append()`** — one resize check instead of n
- In memory-critical code, `array.array` stores actual C values instead of Python object pointers — massive savings for homogeneous numeric data
- Empty list `[]` costs 56 bytes on 64-bit Python. Each item adds 8 bytes (one pointer). Account for this when storing millions of small lists.

## Try It Yourself

```bash
python3 explore.py
```
