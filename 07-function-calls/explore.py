"""
07 — Function Calls & the Call Stack
Run: python3 07-function-calls/explore.py
"""

import dis
import sys
import timeit


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────
# 1. Frame Objects
# ─────────────────────────────────────────────
section("1. Frame Objects — The Execution Context")

def inner():
    frame = sys._getframe()
    print(f"  Current function:  {frame.f_code.co_name}")
    print(f"  Current line:      {frame.f_lineno}")
    print(f"  Caller function:   {frame.f_back.f_code.co_name}")
    print(f"  Caller's caller:   {frame.f_back.f_back.f_code.co_name}")

def outer():
    x = 42
    inner()

outer()


# ─────────────────────────────────────────────
# 2. Bytecode Disassembly
# ─────────────────────────────────────────────
section("2. Bytecode — What Actually Runs")

def add(a, b):
    return a + b

print("  Bytecode for add(a, b):")
dis.dis(add)

print("\n  The code object:")
code = add.__code__
print(f"    co_name:      {code.co_name}")
print(f"    co_varnames:  {code.co_varnames}")
print(f"    co_argcount:  {code.co_argcount}")
print(f"    co_consts:    {code.co_consts}")
print(f"    co_stacksize: {code.co_stacksize}")


# ─────────────────────────────────────────────
# 3. LOAD_FAST vs LOAD_GLOBAL
# ─────────────────────────────────────────────
section("3. Local vs Global — Speed Difference")

GLOBAL_VAR = "I'm global"

def scope_demo():
    local_var = "I'm local"
    _ = GLOBAL_VAR   # LOAD_GLOBAL
    _ = local_var     # LOAD_FAST

print("  Bytecode for scope_demo():")
dis.dis(scope_demo)
print()
print("  Notice: LOAD_FAST (index lookup) vs LOAD_GLOBAL (dict lookup)")

# Benchmark
def use_global():
    for _ in range(1000):
        x = GLOBAL_VAR

def use_local():
    val = GLOBAL_VAR
    for _ in range(1000):
        x = val

t_global = timeit.timeit(use_global, number=1000)
t_local = timeit.timeit(use_local, number=1000)
print(f"\n  Global access (1M reads): {t_global:.4f}s")
print(f"  Local access  (1M reads): {t_local:.4f}s")
print(f"  Local is {t_global/t_local:.1f}x faster")


# ─────────────────────────────────────────────
# 4. Closures
# ─────────────────────────────────────────────
section("4. Closures — Functions That Remember")

def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
print(f"  counter() = {counter()}")  # 1
print(f"  counter() = {counter()}")  # 2
print(f"  counter() = {counter()}")  # 3

print(f"\n  Closure cells: {counter.__closure__}")
print(f"  Cell contents: {counter.__closure__[0].cell_contents}")


# ─────────────────────────────────────────────
# 5. The Classic Loop Trap
# ─────────────────────────────────────────────
section("5. The Loop Trap — Closures Share Cells")

# Bug
funcs_bad = []
for i in range(3):
    funcs_bad.append(lambda: i)

print(f"  Bug:  {[f() for f in funcs_bad]}")  # [2, 2, 2]

# Fix
funcs_good = []
for i in range(3):
    funcs_good.append(lambda i=i: i)

print(f"  Fix:  {[f() for f in funcs_good]}")  # [0, 1, 2]


# ─────────────────────────────────────────────
# 6. Recursion Limit
# ─────────────────────────────────────────────
section("6. Recursion Limit")

print(f"  Default recursion limit: {sys.getrecursionlimit()}")

def count_depth(n=0):
    try:
        return count_depth(n + 1)
    except RecursionError:
        return n

max_depth = count_depth()
print(f"  Actual max depth reached: {max_depth}")


# ─────────────────────────────────────────────
# 7. Function Call Overhead
# ─────────────────────────────────────────────
section("7. Function Call Overhead")

def add_func(a, b):
    return a + b

t_call = timeit.timeit("add_func(1, 2)", globals={"add_func": add_func}, number=1_000_000)
t_inline = timeit.timeit("1 + 2", number=1_000_000)

print(f"  Function call (1M): {t_call:.4f}s")
print(f"  Inline (1M):        {t_inline:.4f}s")
print(f"  Overhead:           {t_call/t_inline:.1f}x slower")


# ─────────────────────────────────────────────
# 8. Walking the Stack
# ─────────────────────────────────────────────
section("8. Walking the Call Stack")

def level_3():
    frame = sys._getframe()
    print("  Call stack (bottom to top):")
    stack = []
    while frame:
        stack.append(f"    {frame.f_code.co_name}() at line {frame.f_lineno}")
        frame = frame.f_back
    for line in reversed(stack):
        print(line)

def level_2():
    level_3()

def level_1():
    level_2()

level_1()


print(f"\n{'='*60}")
print("  Done! Read 07-function-calls/README.md for the full deep dive.")
print(f"{'='*60}")
