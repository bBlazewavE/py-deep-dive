# 03 — How Dicts Actually Work 📖

Python dicts are one of the most optimized data structures in any language runtime. They power **everything** — namespaces, object attributes, keyword arguments, module globals. Understanding them is understanding Python.

## Hash Tables: The Core Idea

A dict is a **hash table**. When you write `d["name"] = "Alice"`:

1. Python calls `hash("name")` → gets a big integer
2. Uses that integer to compute a **slot index** in an internal array
3. Stores the key-value pair at that slot

```
d["name"] = "Alice"

  hash("name") → 2345678901
  slot = 2345678901 % table_size → 5

  Hash Table (simplified):
  ┌───┬───┬───┬───┬───┬──────────────────┬───┬───┐
  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5: ("name","Alice")│ 6 │ 7 │
  └───┴───┴───┴───┴───┴──────────────────┴───┴───┘
```

Lookup is the same process in reverse: hash the key, jump to the slot, return the value. **O(1) average time.**

## Hash Collisions & Open Addressing

What if two keys hash to the same slot? That's a **collision**. Python uses **open addressing** with probing:

```
hash("name") % 8 → slot 5
hash("edad") % 8 → slot 5  💥 collision!

Python probes for the next open slot:
  Slot 5: occupied → try slot = (5 * 5 + 5 + 1) % 8 → slot 7

  ┌───┬───┬───┬───┬───┬────────────┬───┬────────────┐
  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5: "name"  │ 6 │ 7: "edad"  │
  └───┴───┴───┴───┴───┴────────────┴───┴────────────┘
```

The probing isn't linear (slot+1, slot+2...) — CPython uses a **perturbation** scheme that mixes in higher bits of the hash to spread things out.

## The Compact Dict (Python 3.6+)

Before 3.6, dicts used a single sparse array — lots of wasted memory from empty slots. The modern layout splits storage into two arrays:

```
  OLD (pre-3.6): Sparse array, many empty slots
  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │      │k1,v1 │      │      │k2,v2 │      │k3,v3 │      │
  └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
  Wasted space! Each empty slot = 3 pointers of nothing

  NEW (3.6+): Indices array + dense entries
  Indices: ┌───┬───┬───┬───┬───┬───┬───┬───┐
           │   │ 0 │   │   │ 1 │   │ 2 │   │  (1-byte each!)
           └───┴───┴───┴───┴───┴───┴───┴───┘
                 │           │       │
                 ▼           ▼       ▼
  Entries: ┌──────────┬──────────┬──────────┐
           │ k1, v1   │ k2, v2   │ k3, v3   │  (dense, no gaps)
           └──────────┴──────────┴──────────┘
```

**Result:** 20-25% less memory AND dicts preserve insertion order (which became guaranteed in Python 3.7).

## Dict Resizing

When a dict gets ~2/3 full, Python **resizes** — allocates a new, bigger table and re-inserts everything:

```
Load factor > 2/3 → resize!

  Size 8 (5 items, 62% full) → nearing limit
  Size 8 (6 items, 75% full) → RESIZE to 16

  Growth: 8 → 16 → 32 → 64 → ...  (doubles, roughly)
```

This is why `sys.getsizeof()` jumps in chunks — you can watch it happen.

## 🤯 Mind-Blowing Fact

The hash of an integer in Python **is the integer itself** (for values that fit in a C long):

```python
hash(42)     # → 42
hash(1000)   # → 1000
hash(-1)     # → -2  (because -1 is reserved as an error code in C!)
```

That `hash(-1) == -2` quirk has existed since the earliest days of Python and can never be changed without breaking things.

## 💡 Staff Engineer Insight

- **Dict key lookup is O(1) average, O(n) worst case** — but worst case basically never happens with good hash functions
- **Dict creation is expensive** — if you're creating millions of small dicts (like ORM rows), consider `__slots__` or `namedtuple` instead
- **Key sharing dicts (PEP 412)**: Instances of the same class share their key arrays, saving significant memory. This is why `__init__` should always set the same attributes in the same order
- `dict.fromkeys()` and `{**d1, **d2}` are faster than building dicts incrementally
- In hot paths, local variable lookup (`LOAD_FAST`) beats dict-based global/attribute lookup — that's why `local_var = self.attr` before a loop is a real optimization

## Try It Yourself

```bash
python3 explore.py
```
