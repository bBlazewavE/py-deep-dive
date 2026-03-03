# 02 — Memory Model: References, Counting, and the GC 🧹

Python manages memory so you don't have to — but understanding *how* it does it makes you a better engineer.

## How Python Tracks Objects: Reference Counting

Every object has a counter: **how many things point to me?** When the count hits zero, the object is immediately freed.

```
x = "hello"     # refcount("hello") = 1
y = x            # refcount("hello") = 2
del x            # refcount("hello") = 1
del y            # refcount("hello") = 0 → FREED immediately
```

```
  Step 1: x = "hello"           Step 2: y = x
  ┌───┐    ┌─────────┐          ┌───┐    ┌─────────┐
  │ x ├───►│ "hello" │          │ x ├───►│ "hello" │◄───┤ y │
  └───┘    │ rc: 1   │          └───┘    │ rc: 2   │    └───┘
           └─────────┘                   └─────────┘

  Step 3: del x                  Step 4: del y
  ┌───┐    ┌─────────┐                   ┌─────────┐
  │ x │ ✗  │ "hello" │◄───┤ y │          │ "hello" │  → 💀 FREED
  └───┘    │ rc: 1   │    └───┘          │ rc: 0   │
           └─────────┘                   └─────────┘
```

## Peeking at Refcounts with `sys.getrefcount()`

```python
import sys

x = []
print(sys.getrefcount(x))  # 2 (not 1!)
```

**Wait, why 2?** Because passing `x` to `getrefcount()` temporarily creates another reference. The "real" count is always `getrefcount() - 1`.

## The Problem: Circular References 🔄

Reference counting has an Achilles' heel — **cycles**:

```python
a = []
b = []
a.append(b)   # a → b
b.append(a)   # b → a  (CYCLE!)
del a
del b
# Both have refcount 1 (from each other)
# Neither can reach 0. Memory leak! 💀
```

```
  After del a, del b:

  ┌──────────┐     ┌──────────┐
  │ list (a) │────►│ list (b) │
  │ rc: 1    │◄────│ rc: 1    │
  └──────────┘     └──────────┘
       ▲                ▲
       No external      No external
       references!      references!

  → Orphaned cycle. Refcounting alone can't free these.
```

## The Garbage Collector to the Rescue 🦸

Python's `gc` module runs a **generational garbage collector** that detects and breaks cycles:

```
┌──────────────────────────────────────────────┐
│            Generational GC                    │
├──────────┬──────────┬────────────────────────┤
│  Gen 0   │  Gen 1   │  Gen 2                 │
│ (young)  │  (mid)   │  (old)                 │
│ Checked  │ Checked  │ Checked                │
│ often    │ less     │ rarely                 │
└──────────┴──────────┴────────────────────────┘
  New objects start here ──►
  Survivors get promoted ──────────────────────►
```

- **Generation 0**: All new objects. Collected frequently.
- **Generation 1**: Survived one collection. Collected less often.
- **Generation 2**: Long-lived objects. Collected rarely.

The collector traces reachable objects and frees unreachable cycles.

## Weak References — Observing Without Owning

Sometimes you want to reference an object **without** keeping it alive:

```python
import weakref

class BigData:
    def __init__(self, name):
        self.name = name

obj = BigData("important")
weak = weakref.ref(obj)

print(weak())        # <BigData object> — still alive
del obj
print(weak())        # None — it's been collected!
```

```
  Strong ref:  variable ──────► object (keeps alive)
  Weak ref:    variable - - - ► object (doesn't keep alive)
                                  ▲
                                  When strong refs hit 0,
                                  object is freed regardless
                                  of weak refs
```

## 🤯 Mind-Blowing Fact

`gc.get_referrers(obj)` tells you **every object that references your object**. It's like asking "who's pointing at me?" — incredibly powerful for debugging memory leaks:

```python
import gc
x = [1, 2, 3]
y = {"data": x}
print(gc.get_referrers(x))  # Shows y's dict, locals(), etc.
```

## 💡 Staff Engineer Insight

- **Memory leaks in Python are almost always circular references** involving objects with `__del__` methods (the GC can't safely break those cycles in older Python versions)
- Use `weakref` for caches — `weakref.WeakValueDictionary()` gives you a cache that doesn't prevent garbage collection
- In long-running services, call `gc.get_stats()` periodically to monitor collection generations
- If you're seeing memory grow, `objgraph` (third-party) or `tracemalloc` (stdlib) are your best friends

## Try It Yourself

```bash
python3 explore.py
```
