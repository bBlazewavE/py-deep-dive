"""
09 — Generators & Coroutines
Run: python3 09-generators-coroutines/explore.py
"""

import sys
import asyncio


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────
# 1. Generator Basics
# ─────────────────────────────────────────────
section("1. Generator Basics — Lazy Evaluation")

def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

gen = count_up(5)
print(f"  type(gen): {type(gen)}")
print(f"  Values: {list(gen)}")

# Nothing executes until consumed
def verbose_gen():
    print("    → producing 1")
    yield 1
    print("    → producing 2")
    yield 2
    print("    → done")

print("\n  Step-by-step execution:")
g = verbose_gen()
print(f"  next(g) = {next(g)}")
print(f"  next(g) = {next(g)}")
try:
    next(g)
except StopIteration:
    print("  StopIteration raised")


# ─────────────────────────────────────────────
# 2. Generator Internals
# ─────────────────────────────────────────────
section("2. Generator Internals — Frame Objects")

def my_gen():
    x = 10
    yield x
    x = 20
    yield x

g = my_gen()
print(f"  Before first next():")
print(f"    gi_frame: {g.gi_frame}")
print(f"    gi_code:  {g.gi_code.co_name}")

next(g)
print(f"\n  After first next():")
print(f"    gi_frame.f_locals: {g.gi_frame.f_locals}")
print(f"    gi_frame.f_lineno: {g.gi_frame.f_lineno}")

next(g)
print(f"\n  After second next():")
print(f"    gi_frame.f_locals: {g.gi_frame.f_locals}")

try:
    next(g)
except StopIteration:
    pass
print(f"\n  After exhaustion:")
print(f"    gi_frame: {g.gi_frame}  ← frame is gone!")


# ─────────────────────────────────────────────
# 3. Memory: Generator vs List
# ─────────────────────────────────────────────
section("3. Memory — Generators Are Constant Size")

sizes = [100, 10_000, 1_000_000]
for n in sizes:
    lst = [i for i in range(n)]
    gen = (i for i in range(n))
    print(f"  n={n:>10,}  list={sys.getsizeof(lst):>10,} bytes  gen={sys.getsizeof(gen)} bytes")


# ─────────────────────────────────────────────
# 4. send() — Two-Way Communication
# ─────────────────────────────────────────────
section("4. send() — Two-Way Communication")

def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)               # prime
print(f"  send(10) → {acc.send(10)}")
print(f"  send(20) → {acc.send(20)}")
print(f"  send(5)  → {acc.send(5)}")


# ─────────────────────────────────────────────
# 5. throw() and close()
# ─────────────────────────────────────────────
section("5. throw() and close()")

def robust():
    try:
        while True:
            try:
                value = yield
                print(f"    Got: {value}")
            except ValueError:
                print("    Caught ValueError — recovering")
    finally:
        print("    Finally block (cleanup)")

g = robust()
next(g)
g.send("hello")
g.throw(ValueError)
g.send("still alive")
g.close()


# ─────────────────────────────────────────────
# 6. yield from
# ─────────────────────────────────────────────
section("6. yield from — Delegation")

def inner():
    yield "a"
    yield "b"
    return "inner_result"

def outer():
    result = yield from inner()
    print(f"    inner returned: '{result}'")
    yield "c"

print(f"  Values: {list(outer())}")

# Flattening
print()

def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, [3, 4], 5], [6, 7]]
print(f"  flatten({nested})")
print(f"  → {list(flatten(nested))}")


# ─────────────────────────────────────────────
# 7. Generator Pipelines
# ─────────────────────────────────────────────
section("7. Generator Pipelines — Assembly Line")

def read_lines(text):
    for line in text.strip().split("\n"):
        yield line.strip()

def parse_numbers(lines):
    for line in lines:
        try:
            yield int(line)
        except ValueError:
            continue

def square(numbers):
    for n in numbers:
        yield n ** 2

def above_threshold(numbers, threshold):
    for n in numbers:
        if n > threshold:
            yield n

data = """
10
-3
7
abc
-1
42
0
"""

pipeline = above_threshold(square(parse_numbers(read_lines(data))), 10)
print(f"  Data → parse → square → filter(>10)")
print(f"  Result: {list(pipeline)}")
print(f"  Memory: O(1) regardless of data size!")


# ─────────────────────────────────────────────
# 8. Single-Use Gotcha
# ─────────────────────────────────────────────
section("8. Common Pitfall — Single Use")

gen = (x**2 for x in range(5))
first = list(gen)
second = list(gen)
print(f"  First consumption:  {first}")
print(f"  Second consumption: {second}  ← empty!")


# ─────────────────────────────────────────────
# 9. Async/Await Basics
# ─────────────────────────────────────────────
section("9. async/await — Coroutine Objects")

async def fetch(name, delay):
    print(f"    {name}: starting")
    await asyncio.sleep(delay)
    print(f"    {name}: done after {delay}s")
    return f"{name}_result"

# Show coroutine object structure
coro = fetch("test", 0)
print(f"  type:     {type(coro)}")
print(f"  cr_frame: {coro.cr_frame}")
print(f"  cr_code:  {coro.cr_code.co_name}")
coro.close()  # cleanup

# Run concurrent coroutines
async def demo_concurrent():
    print("\n  Running 3 coroutines concurrently:")
    results = await asyncio.gather(
        fetch("A", 0.3),
        fetch("B", 0.1),
        fetch("C", 0.2),
    )
    print(f"    Results: {results}")
    print("    (Notice: B finishes first despite starting second!)")

asyncio.run(demo_concurrent())


# ─────────────────────────────────────────────
# 10. Async Generator
# ─────────────────────────────────────────────
section("10. Async Generators (Python 3.6+)")

async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.05)
        yield i

async def demo_async_gen():
    values = []
    async for val in async_range(5):
        values.append(val)
    print(f"  async for values: {values}")

asyncio.run(demo_async_gen())


print(f"\n{'='*60}")
print("  Done! Read 09-generators-coroutines/README.md for the full deep dive.")
print(f"{'='*60}")
