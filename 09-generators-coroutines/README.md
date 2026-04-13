# 09 — Generators & Coroutines

> **`yield`** · Generator objects · `send()` · `yield from` · `async`/`await` internals

## What Is a Generator?

A generator is a function that **pauses and resumes**. Instead of computing everything at once and returning a list, it produces values one at a time:

```python
def count_up(n):
    i = 0
    while i < n:
        yield i    # pause here, produce a value
        i += 1     # resume here on next()

gen = count_up(3)
print(next(gen))   # 0
print(next(gen))   # 1
print(next(gen))   # 2
print(next(gen))   # StopIteration!
```

## Under the Hood: Generator Objects

When you call a generator function, **nothing executes**. Python creates a generator object that's frozen at the start:

```python
def my_gen():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = my_gen()     # nothing prints!
print(type(g))   # <class 'generator'>
```

A generator object holds:
- **`gi_frame`** — the suspended frame (same frame objects from Topic 07!)
- **`gi_code`** — the code object
- **`gi_yieldfrom`** — sub-generator if using `yield from`

```python
g = my_gen()
print(g.gi_frame)          # <frame object> — frozen at line 1
print(g.gi_frame.f_lineno) # points to first line

next(g)                    # prints "start", yields 1
print(g.gi_frame.f_lineno) # now points to yield line
```

When the generator is exhausted, `gi_frame` becomes `None` — the frame is gone.

## Generators vs Lists: Memory

The whole point — generators are **lazy**:

```python
import sys

# List: all values in memory at once
big_list = [i for i in range(1_000_000)]
print(sys.getsizeof(big_list))  # ~8 MB

# Generator: one value at a time
big_gen = (i for i in range(1_000_000))
print(sys.getsizeof(big_gen))   # ~200 bytes (always!)
```

| | List | Generator |
|---|---|---|
| Memory | O(n) | O(1) |
| Speed (first item) | Must compute all | Instant |
| Reusable | Yes | No — single pass |
| Indexable | Yes (`lst[5]`) | No |

## `send()`: Two-Way Communication

Generators aren't just producers — they can **receive values**:

```python
def accumulator():
    total = 0
    while True:
        value = yield total   # yield current total, receive next value
        total += value

acc = accumulator()
next(acc)          # prime the generator (advances to first yield)
print(acc.send(10))  # 10
print(acc.send(20))  # 30
print(acc.send(5))   # 35
```

`yield` is an **expression**, not just a statement. `send(value)` resumes the generator and makes `yield` evaluate to `value`.

```
next(acc)     →  runs to yield, produces 0, pauses
send(10)      →  yield evaluates to 10, total=10, loops to yield, produces 10, pauses
send(20)      →  yield evaluates to 20, total=30, loops to yield, produces 30, pauses
```

## `throw()` and `close()`

You can inject exceptions and shut down generators:

```python
def careful():
    try:
        while True:
            try:
                value = yield
                print(f"  Got: {value}")
            except ValueError:
                print("  Caught ValueError inside generator!")
    finally:
        print("  Cleanup in finally block")

g = careful()
next(g)
g.send("hello")       # Got: hello
g.throw(ValueError)   # Caught ValueError inside generator!
g.close()             # Cleanup in finally block (throws GeneratorExit)
```

## `yield from`: Delegation

`yield from` delegates to a sub-generator, transparently forwarding `next()`, `send()`, `throw()`, and `close()`:

```python
def inner():
    yield 1
    yield 2
    return "done"  # return value is captured by yield from

def outer():
    result = yield from inner()
    print(f"  inner returned: {result}")
    yield 3

print(list(outer()))  # inner returned: done → [1, 2, 3]
```

Without `yield from`, you'd need a manual loop:

```python
# Equivalent without yield from (much more code):
def outer_manual():
    gen = inner()
    try:
        while True:
            yield next(gen)
    except StopIteration as e:
        result = e.value
    print(f"  inner returned: {result}")
    yield 3
```

### Flattening nested structures

```python
def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, [3, 4], 5], [6, 7]]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7]
```

## Generator Pipelines

Chain generators for memory-efficient data processing:

```python
def read_lines(text):
    for line in text.strip().split("\n"):
        yield line

def parse_ints(lines):
    for line in lines:
        yield int(line)

def filter_positive(numbers):
    for n in numbers:
        if n > 0:
            yield n

data = "10\n-3\n7\n-1\n42"

# Nothing executes until we consume
pipeline = filter_positive(parse_ints(read_lines(data)))

# Each value flows through the entire chain one at a time
print(list(pipeline))  # [10, 7, 42]
```

Each item flows through the entire pipeline before the next item starts — like a factory assembly line. Memory usage: O(1) regardless of data size.

## From Generators to Coroutines

Generators laid the groundwork for Python's async model. The evolution:

```
Python 2.2  →  Simple generators (yield produces values)
Python 2.5  →  Generator-based coroutines (send/throw)
Python 3.3  →  yield from (delegation)
Python 3.4  →  asyncio + @asyncio.coroutine
Python 3.5  →  async/await syntax (native coroutines)
```

### The connection

```python
# Generator-based coroutine (old style)
import asyncio

@asyncio.coroutine
def old_style():
    yield from asyncio.sleep(1)
    return "done"

# Native coroutine (modern)
async def new_style():
    await asyncio.sleep(1)
    return "done"
```

Under the hood, `await` is essentially `yield from` for coroutine objects. The event loop calls `send(None)` to advance coroutines, just like generators.

## `async`/`await` Internals

A coroutine object is structurally similar to a generator:

```python
async def fetch():
    await asyncio.sleep(0)
    return 42

coro = fetch()
print(type(coro))    # <class 'coroutine'>
print(coro.cr_frame) # <frame object> — same as gi_frame!
print(coro.cr_code)  # code object
```

| Generator | Coroutine |
|---|---|
| `gi_frame` | `cr_frame` |
| `gi_code` | `cr_code` |
| `gi_yieldfrom` | `cr_await` |
| `next()`/`send()` | Event loop drives via `send()` |
| `yield` pauses | `await` pauses |

### How the event loop works (simplified)

```python
# Pseudocode — what asyncio.run() does internally
def run(coro):
    task_queue = [coro]
    while task_queue:
        task = task_queue.pop(0)
        try:
            result = task.send(None)  # advance to next await
            # result tells the loop what to wait for (I/O, timer, etc.)
            task_queue.append(task)   # re-queue for later
        except StopIteration as e:
            print(f"Task finished: {e.value}")
```

The event loop is just a `while` loop calling `send(None)` on coroutines. When a coroutine hits `await`, it yields control back to the loop, which can run other coroutines.

## `async for` and `async with`

### Async iterators

```python
class AsyncCounter:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.i += 1
        return self.i

# async for val in AsyncCounter(3):
#     print(val)  # 1, 2, 3 (with 0.1s delay each)
```

### Async generators (Python 3.6+)

Much simpler:

```python
async def async_count(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i
```

### Async context managers

```python
class AsyncDB:
    async def __aenter__(self):
        print("  connecting...")
        await asyncio.sleep(0)
        return self

    async def __aexit__(self, *args):
        print("  disconnecting...")
        await asyncio.sleep(0)

# async with AsyncDB() as db:
#     ...
```

## Common Pitfalls

### 1. Generators are single-use

```python
gen = (i for i in range(3))
print(list(gen))  # [0, 1, 2]
print(list(gen))  # [] — exhausted!
```

### 2. Forgetting to prime coroutines

```python
def coro():
    value = yield
    print(value)

c = coro()
# c.send("hello")  # TypeError! Must call next() first
next(c)             # prime it
c.send("hello")     # now it works
```

### 3. Not awaiting coroutines

```python
async def compute():
    return 42

# result = compute()    # RuntimeWarning! This is a coroutine object, not 42
# result = await compute()  # ✅
```

## When to Use What

| Need | Use |
|---|---|
| Lazy sequence of values | Generator function |
| One-off lazy expression | Generator expression `(x for x in ...)` |
| Two-way communication | `send()` / coroutine |
| Delegate to sub-generator | `yield from` |
| I/O concurrency | `async`/`await` + `asyncio` |
| Memory-efficient pipeline | Chained generators |
| Infinite sequence | Generator with `while True: yield` |

## Run It

```bash
python3 09-generators-coroutines/explore.py
```
