# 01 — Everything is an Object 🧱

In Python, **everything** is an object. Numbers, strings, functions, classes, modules, even `None` — they're all objects sitting in memory with an identity, a type, and a value.

## What Does "Object" Actually Mean?

In CPython, every Python object is a C struct called `PyObject`. At minimum, it contains:

```
┌─────────────────────────────┐
│         PyObject            │
├─────────────────────────────┤
│  ob_refcnt   (reference count) │
│  ob_type     (pointer to type)  │
│  ... value data ...             │
└─────────────────────────────┘
```

That's it. Every single value in Python has at least these two fields.

## `id()` — The Memory Address

`id()` returns the identity of an object — in CPython, it's literally the memory address:

```python
x = [1, 2, 3]
print(id(x))    # → 140234866534720  (some memory address)
print(hex(id(x)))  # → 0x7f8b2c3a4e00
```

Two variables can point to the **same** object:

```
 Variable       Memory
┌───┐         ┌──────────┐
│ a ├────────►│ [1,2,3]  │  ◄── one object in memory
├───┤         │ id: 0x7f │
│ b ├────────►│          │
└───┘         └──────────┘
```

```python
a = [1, 2, 3]
b = a
print(a is b)       # True — same object!
print(id(a) == id(b))  # True
```

## `is` vs `==` — Identity vs Equality

This trips up everyone at some point:

| Operator | Checks | Question it answers |
|----------|--------|-------------------|
| `is`     | Identity (same object in memory) | "Are these the same box?" |
| `==`     | Equality (same value) | "Do these boxes contain the same thing?" |

```python
a = [1, 2, 3]
b = [1, 2, 3]

a == b   # True  — same contents
a is b   # False — different objects in memory!
```

```
 a ──► ┌─────────┐
       │ [1,2,3] │  id: 0x1001
       └─────────┘

 b ──► ┌─────────┐
       │ [1,2,3] │  id: 0x2002   ← different box!
       └─────────┘
```

## 🤯 Mind-Blowing Fact: Integer Interning

CPython pre-creates integers from **-5 to 256** and reuses them. So:

```python
a = 256
b = 256
a is b   # True! Same object — Python reuses small ints

a = 257
b = 257
a is b   # False! Different objects (outside the cache)
```

This is a CPython implementation detail — don't rely on it in production code.

```
Integer Cache (pre-allocated at startup):
┌────┬────┬────┬─────┬─────┬─────┬─────┐
│ -5 │ -4 │ -3 │ ... │ 255 │ 256 │     │
└────┴────┴────┴─────┴─────┴─────┴─────┘
  ▲                           ▲
  Always reused               Always reused
```

## `type()` — Everything Has a Type

```python
type(42)          # <class 'int'>
type("hello")     # <class 'str'>
type([1, 2])      # <class 'list'>
type(type)        # <class 'type'>  🤯
type(None)        # <class 'NoneType'>
type(print)       # <class 'builtin_function_or_method'>
```

Even `type` itself is an object of type `type`. It's types all the way down.

## 💡 Staff Engineer Insight

Understanding `is` vs `==` prevents subtle bugs in production:
- **Never** use `is` to compare values (except `None` — `x is None` is idiomatic)
- Integer interning means `is` "works" for small numbers in tests but breaks for large ones in prod
- When debugging memory issues, `id()` tells you if you have one object or two — crucial for understanding mutation vs copying

## Try It Yourself

```bash
python3 explore.py
```

The script demonstrates all of these concepts with live output from your Python interpreter.
