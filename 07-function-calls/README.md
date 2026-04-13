# 07 — Function Calls & the Call Stack

> **CPython internals** · `dis` module · Frame objects · Closures

## What Happens When You Call a Function?

```python
def greet(name):
    return f"Hello, {name}"

greet("Dimple")
```

Seems simple. But under the hood, CPython:

1. **Creates a frame object** — a snapshot of execution context
2. **Pushes it onto the call stack** — a LIFO stack of frames
3. **Executes bytecode** inside that frame
4. **Pops the frame** when the function returns

## The Call Stack

Every running Python program has a **call stack** — a stack of frame objects, one per active function call.

```
┌─────────────────────┐
│  greet() frame      │  ← top (currently executing)
│  locals: {name: "D"}│
├─────────────────────┤
│  main() frame       │
│  locals: {}         │
├─────────────────────┤
│  <module> frame     │  ← bottom (module-level code)
│  globals: {greet: …}│
└─────────────────────┘
```

Each frame knows who called it (`f_back`), what code it's running (`f_code`), and where it is (`f_lineno`).

## Frame Objects: The Execution Context

A frame holds *everything* a function needs to execute:

```python
import sys

def inner():
    frame = sys._getframe()  # get current frame
    print(f"Function:  {frame.f_code.co_name}")
    print(f"Line:      {frame.f_lineno}")
    print(f"Locals:    {frame.f_locals}")
    print(f"Caller:    {frame.f_back.f_code.co_name}")

def outer():
    x = 42
    inner()

outer()
# Function:  inner
# Line:      5
# Locals:    {'frame': <frame object>}
# Caller:    outer
```

### Key Frame Attributes

| Attribute | What it holds |
|---|---|
| `f_code` | The code object (bytecode, constants, variable names) |
| `f_locals` | Local variable dict |
| `f_globals` | Global variable dict |
| `f_back` | Pointer to the caller's frame (or `None` for module level) |
| `f_lineno` | Current line number |
| `f_lasti` | Index of last bytecode instruction executed |

## Bytecode: What Actually Runs

Python doesn't execute your source code directly. It compiles to **bytecode** first:

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

```
  2           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```

Each instruction operates on a **stack** (the "evaluation stack" inside the frame):

```
LOAD_FAST 0 (a)   → stack: [a]
LOAD_FAST 1 (b)   → stack: [a, b]
BINARY_ADD         → stack: [a+b]     (pops 2, pushes result)
RETURN_VALUE       → returns a+b
```

## The Code Object

Functions don't store bytecode directly — they hold a **code object** (`__code__`):

```python
def greet(name, greeting="Hello"):
    message = f"{greeting}, {name}"
    return message

code = greet.__code__
print(f"Name:       {code.co_name}")        # 'greet'
print(f"Args:       {code.co_varnames}")     # ('name', 'greeting', 'message')
print(f"Arg count:  {code.co_argcount}")     # 2
print(f"Constants:  {code.co_consts}")       # (None, 'Hello')
print(f"Stack size: {code.co_stacksize}")    # max eval stack depth
```

The relationship:

```
function object (greet)
  └── __code__  → code object (bytecode, constants, metadata)
  └── __globals__ → module globals dict
  └── __defaults__ → default arg values ("Hello",)
  └── __closure__ → cell objects (if closure)

When called:
  └── creates frame object
        └── f_code → the code object
        └── f_locals → fresh dict for this call
        └── f_back → caller's frame
```

## Local vs Global Scope

CPython treats locals and globals completely differently:

```python
x = "global"

def func():
    y = "local"
    print(x)  # global lookup — slower
    print(y)  # local lookup — faster
```

**Why locals are faster:**

- **Locals** → stored in a C array, accessed by index (`LOAD_FAST`)
- **Globals** → stored in a dict, accessed by name (`LOAD_GLOBAL`)

```python
dis.dis(func)
#   LOAD_GLOBAL  0 (x)    ← dict lookup by name
#   LOAD_FAST    0 (y)    ← array lookup by index
```

This is why `LOAD_FAST` is called "fast" — it's an O(1) array index, not a hash table lookup.

### The `local()` optimization

CPython decides at **compile time** whether a variable is local or global. That's why this fails:

```python
x = 10

def broken():
    print(x)    # UnboundLocalError!
    x = 20      # this assignment makes x local for the ENTIRE function
```

The compiler sees `x = 20`, marks `x` as local for the whole function, and then `print(x)` tries to read it before assignment.

## Closures: Functions That Remember

A **closure** captures variables from enclosing scopes:

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

### How closures work internally

Closures don't capture *values* — they capture **cell objects** that point to the variable:

```python
def make_adder(x):
    def add(y):
        return x + y
    return add

adder = make_adder(10)
print(adder.__closure__)           # (<cell object>,)
print(adder.__closure__[0].cell_contents)  # 10
```

```
make_adder frame:
  x → cell object → 10

add (closure):
  __closure__[0] → same cell object → 10
```

The cell is shared — if the enclosing function modifies the variable, the closure sees the change (and vice versa with `nonlocal`).

### The classic loop trap

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])  # [2, 2, 2] — NOT [0, 1, 2]!
```

All lambdas share the **same cell** pointing to `i`. By the time you call them, `i` is 2.

**Fix:** capture by default argument (creates a new local):

```python
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)  # default arg evaluated at definition time

print([f() for f in funcs])  # [0, 1, 2] ✅
```

## Stack Depth & Recursion

Python's call stack has a **hard limit** (default 1000):

```python
import sys
print(sys.getrecursionlimit())  # 1000

def recurse(n):
    return recurse(n + 1)

recurse(0)  # RecursionError: maximum recursion depth exceeded
```

Each frame allocates memory. Unlike languages with tail-call optimization (Scheme, some C compilers), **CPython never optimizes tail calls**:

```python
# This is NOT optimized — still creates 1000 frames
def factorial(n, acc=1):
    if n <= 1:
        return acc
    return factorial(n - 1, n * acc)  # tail position, but CPython doesn't care
```

### Why no tail-call optimization?

Guido van Rossum intentionally rejected it because:
1. **Tracebacks would be destroyed** — you lose the call stack for debugging
2. **Python is not a functional language** — use loops for iteration

## Performance: Function Call Overhead

Function calls in Python are **expensive** compared to C/Go:

```python
import timeit

def add(a, b):
    return a + b

# Function call
timeit.timeit("add(1, 2)", globals=globals(), number=1_000_000)
# ~0.15s

# Inline
timeit.timeit("1 + 2", number=1_000_000)
# ~0.03s
```

Why? Every call means:
1. Allocate a frame object
2. Set up locals array
3. Push onto call stack
4. Execute bytecode
5. Pop frame, deallocate

This is why Python hot loops avoid function calls, and why built-in functions (written in C) are much faster — they skip frame creation entirely.

### Python 3.11+ optimizations

PEP 659 introduced **adaptive specialization**. Frequently-called functions get optimized bytecode:

- `LOAD_FAST` → might skip some safety checks
- `CALL_FUNCTION` → specialized for common patterns
- Frame objects are **lazily created** — only materialized if you actually inspect the stack

## Walking the Stack

You can traverse the entire call stack at runtime:

```python
import traceback

def c():
    traceback.print_stack()

def b():
    c()

def a():
    b()

a()
# File "...", line 10, in a
# File "...", line 7, in b
# File "...", line 4, in c
```

Or programmatically:

```python
import sys

def walk_stack():
    frame = sys._getframe()
    while frame:
        print(f"{frame.f_code.co_name} at line {frame.f_lineno}")
        frame = frame.f_back
```

## When to Use What

| Situation | Approach |
|---|---|
| Need to keep state between calls | Closure or class |
| Deep recursion | Rewrite as a loop |
| Performance-critical hot loop | Avoid function calls, use builtins |
| Need to inspect callers | `sys._getframe()` or `inspect` module |
| Want lazy evaluation | Generator (next topic!) |

## Run It

```bash
python3 07-function-calls/explore.py
```
