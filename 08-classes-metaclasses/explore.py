"""
08 — Classes & Metaclasses
Run: python3 08-classes-metaclasses/explore.py
"""

import sys


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────
# 1. type() — The Metaclass
# ─────────────────────────────────────────────
section("1. type() — The Class of Classes")

print(f"  type(42):       {type(42)}")
print(f"  type(int):      {type(int)}")
print(f"  type(type):     {type(type)}")

# Creating a class dynamically with type()
DynamicClass = type("DynamicClass", (object,), {"x": 10, "greet": lambda self: "hi"})
obj = DynamicClass()
print(f"\n  Dynamic class: {DynamicClass}")
print(f"  obj.x = {obj.x}")
print(f"  obj.greet() = {obj.greet()}")


# ─────────────────────────────────────────────
# 2. __new__ vs __init__
# ─────────────────────────────────────────────
section("2. __new__ vs __init__")

class Point:
    def __new__(cls, x, y):
        print(f"  __new__:  allocating {cls.__name__}")
        instance = super().__new__(cls)
        return instance

    def __init__(self, x, y):
        print(f"  __init__: setting x={x}, y={y}")
        self.x = x
        self.y = y

p = Point(3, 4)

# Immutable type customization
print()

class EvenInt(int):
    def __new__(cls, value):
        return super().__new__(cls, value - value % 2)

print(f"  EvenInt(7) = {EvenInt(7)}")
print(f"  EvenInt(4) = {EvenInt(4)}")

# Singleton
print()

class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a, b = Singleton(), Singleton()
print(f"  Singleton: a is b = {a is b}")


# ─────────────────────────────────────────────
# 3. Method Resolution Order (MRO)
# ─────────────────────────────────────────────
section("3. MRO — Method Resolution Order")

class A:
    def who(self): return "A"

class B(A):
    def who(self): return "B"

class C(A):
    def who(self): return "C"

class D(B, C):
    pass

print(f"  D().who() = '{D().who()}'")
print(f"  D.__mro__ =")
for cls in D.__mro__:
    print(f"    → {cls.__name__}")

# super() follows MRO
print()

class X:
    def greet(self):
        print("    X.greet")

class Y(X):
    def greet(self):
        print("    Y.greet")
        super().greet()

class Z(X):
    def greet(self):
        print("    Z.greet")
        super().greet()

class W(Y, Z):
    def greet(self):
        print("    W.greet")
        super().greet()

print("  super() follows MRO chain:")
W().greet()
print(f"  MRO: {' → '.join(c.__name__ for c in W.__mro__)}")


# ─────────────────────────────────────────────
# 4. Descriptors
# ─────────────────────────────────────────────
section("4. Descriptors — The Protocol Behind @property")

class Validated:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value):
        if not self.min_val <= value <= self.max_val:
            raise ValueError(f"{self.name} must be between {self.min_val}-{self.max_val}")
        setattr(obj, f"_{self.name}", value)

class Config:
    timeout = Validated(1, 60)
    retries = Validated(0, 10)

c = Config()
c.timeout = 30
c.retries = 3
print(f"  c.timeout = {c.timeout}")
print(f"  c.retries = {c.retries}")

try:
    c.timeout = 100
except ValueError as e:
    print(f"  c.timeout = 100 → {e}")


# ─────────────────────────────────────────────
# 5. Metaclasses
# ─────────────────────────────────────────────
section("5. Metaclasses — Classes That Build Classes")

class PluginMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class JSONPlugin(Plugin):
    pass

class XMLPlugin(Plugin):
    pass

class CSVPlugin(Plugin):
    pass

print(f"  Registered plugins: {list(PluginMeta.registry.keys())}")


# ─────────────────────────────────────────────
# 6. __init_subclass__ (Modern Alternative)
# ─────────────────────────────────────────────
section("6. __init_subclass__ — The Modern Way")

class Handler:
    handlers = {}

    def __init_subclass__(cls, route=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if route:
            Handler.handlers[route] = cls

class HomeHandler(Handler, route="/"):
    pass

class APIHandler(Handler, route="/api"):
    pass

print(f"  Route registry: {Handler.handlers}")


# ─────────────────────────────────────────────
# 7. __slots__
# ─────────────────────────────────────────────
section("7. __slots__ — Memory Optimization")

class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

a = WithDict(1, 2)
b = WithSlots(1, 2)

size_dict = sys.getsizeof(a) + sys.getsizeof(a.__dict__)
size_slots = sys.getsizeof(b)

print(f"  With __dict__:  {size_dict} bytes")
print(f"  With __slots__: {size_slots} bytes")
print(f"  Savings:        {size_dict - size_slots} bytes per instance")

# Show that slots blocks dynamic attrs
try:
    b.z = 99
except AttributeError as e:
    print(f"  Dynamic attr on slots → {e}")

# Scale it up
import timeit
def create_dict():
    for _ in range(10000):
        WithDict(1, 2)

def create_slots():
    for _ in range(10000):
        WithSlots(1, 2)

t_dict = timeit.timeit(create_dict, number=100)
t_slots = timeit.timeit(create_slots, number=100)
print(f"\n  Create 1M instances:")
print(f"    __dict__:  {t_dict:.3f}s")
print(f"    __slots__: {t_slots:.3f}s")
print(f"    Slots is {t_dict/t_slots:.1f}x faster")


print(f"\n{'='*60}")
print("  Done! Read 08-classes-metaclasses/README.md for the full deep dive.")
print(f"{'='*60}")
