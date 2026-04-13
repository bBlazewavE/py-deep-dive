# 08 — Classes & Metaclasses

> **`__new__` vs `__init__`** · MRO · Descriptors · `type()` · Custom metaclasses

## What Happens When You Write `class Foo`?

```python
class Foo:
    x = 10
    def hello(self):
        return "hi"
```

Python doesn't just "register" a class. It **executes** the class body and calls `type()` to build the class object:

```python
# The above is roughly equivalent to:
body = {}
exec("x = 10\ndef hello(self): return 'hi'", body)
Foo = type("Foo", (object,), body)
```

`type` is the **metaclass** — the class of classes.

```python
print(type(42))        # <class 'int'>
print(type(int))       # <class 'type'>
print(type(type))      # <class 'type'> — it's turtles all the way down
```

```
instance  →  class  →  metaclass
  42     →   int   →    type
  Foo()  →   Foo   →    type
```

## `__new__` vs `__init__`

Most people only know `__init__`. But object creation is a **two-step process**:

```python
class Point:
    def __new__(cls, x, y):
        print(f"__new__: creating instance of {cls.__name__}")
        instance = super().__new__(cls)  # actually allocates the object
        return instance

    def __init__(self, x, y):
        print(f"__init__: initializing with ({x}, {y})")
        self.x = x
        self.y = y

p = Point(1, 2)
# __new__: creating instance of Point
# __init__: initializing with (1, 2)
```

| | `__new__` | `__init__` |
|---|---|---|
| **Purpose** | Create the instance | Initialize the instance |
| **First arg** | `cls` (the class) | `self` (the instance) |
| **Returns** | The new instance | `None` |
| **When to override** | Immutable types, singletons, caching | Almost always (normal setup) |
| **Called** | Before `__init__` | After `__new__` |

### When `__new__` matters: Immutable types

You can't modify an `int` after creation, so you **must** use `__new__`:

```python
class EvenInt(int):
    def __new__(cls, value):
        return super().__new__(cls, value - value % 2)

print(EvenInt(7))   # 6
print(EvenInt(4))   # 4
```

### Singleton pattern with `__new__`

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)  # True
```

## Method Resolution Order (MRO)

When a class inherits from multiple parents, Python needs to decide which method to call. It uses the **C3 linearization algorithm**:

```python
class A:
    def who(self): return "A"

class B(A):
    def who(self): return "B"

class C(A):
    def who(self): return "C"

class D(B, C):
    pass

print(D().who())  # "B"
print(D.__mro__)
# (D, B, C, A, object)
```

```
      A
     / \
    B   C
     \ /
      D

MRO: D → B → C → A → object
```

### MRO rules

1. **Children before parents** — `D` comes before `B` and `C`
2. **Left before right** — `B` (listed first) comes before `C`
3. **Preserve order** — if `B` inherits from `A`, `B` always comes before `A`

### `super()` follows MRO, not parent

This is the key insight most people miss:

```python
class A:
    def greet(self):
        print("A")

class B(A):
    def greet(self):
        print("B")
        super().greet()  # calls C.greet(), NOT A.greet()!

class C(A):
    def greet(self):
        print("C")
        super().greet()

class D(B, C):
    def greet(self):
        print("D")
        super().greet()

D().greet()
# D → B → C → A (follows MRO exactly)
```

## Descriptors: The Protocol Behind Everything

Descriptors power `@property`, `@classmethod`, `@staticmethod`, slots, and more. A descriptor is any object with `__get__`, `__set__`, or `__delete__`:

```python
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
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        setattr(obj, f"_{self.name}", value)

class Config:
    timeout = Validated(1, 60)
    retries = Validated(0, 10)

c = Config()
c.timeout = 30   # ✅
c.retries = 3    # ✅
# c.timeout = 100  # ValueError!
```

### How `@property` works (it's a descriptor)

```python
class property:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)
```

### Descriptor lookup order

When you access `obj.attr`, Python searches:

1. **Data descriptor** on the class (`__get__` + `__set__`) — wins over instance dict
2. **Instance `__dict__`**
3. **Non-data descriptor** on the class (`__get__` only)
4. **`__getattr__`** (fallback)

This is why `@property` (a data descriptor) can intercept attribute access even if the instance has the same key in `__dict__`.

## Metaclasses: Classes That Build Classes

A metaclass controls how a class is created. The default metaclass is `type`.

```python
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class: {name}")
        # You can modify the class before it's created
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

class MyClass(metaclass=Meta):
    pass
# Creating class: MyClass
```

### Real-world metaclass: Auto-registry

```python
class PluginMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:  # don't register the base class itself
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class JSONPlugin(Plugin):
    pass

class XMLPlugin(Plugin):
    pass

print(PluginMeta.registry)
# {'JSONPlugin': <class 'JSONPlugin'>, 'XMLPlugin': <class 'XMLPlugin'>}
```

### `__init_subclass__`: The modern alternative

Python 3.6+ added `__init_subclass__` which covers most metaclass use cases without the complexity:

```python
class Plugin:
    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry[cls.__name__] = cls

class JSONPlugin(Plugin):
    pass

class XMLPlugin(Plugin):
    pass

print(Plugin.registry)
# {'JSONPlugin': <class 'JSONPlugin'>, 'XMLPlugin': <class 'XMLPlugin'>}
```

**Rule of thumb:** Use `__init_subclass__` unless you need to modify the class namespace *before* the class is created.

## Class Creation: The Full Picture

```
1. Python encounters `class Foo(Base, metaclass=Meta):`
2. Executes the class body → collects into a namespace dict
3. Calls Meta("Foo", (Base,), namespace)
   a. Meta.__new__(Meta, "Foo", (Base,), namespace) → creates the class
   b. Meta.__init__(cls, "Foo", (Base,), namespace) → initializes it
4. Assigns result to name `Foo`
```

## `__slots__`: Ditching the Instance Dict

By default, instances store attributes in a `__dict__`. With `__slots__`, Python uses a compact struct instead:

```python
class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
a = WithDict(1, 2)
b = WithSlots(1, 2)
print(f"With __dict__:  {sys.getsizeof(a) + sys.getsizeof(a.__dict__)} bytes")
print(f"With __slots__: {sys.getsizeof(b)} bytes")
```

| | `__dict__` | `__slots__` |
|---|---|---|
| Memory | ~100+ bytes | ~56 bytes |
| Dynamic attrs | ✅ `obj.anything = 1` | ❌ Only declared attrs |
| Speed | Slower (dict lookup) | Faster (struct offset) |
| Inheritance | Just works | Must declare in each subclass |

## When to Use What

| Want to... | Use |
|---|---|
| Normal class setup | `__init__` |
| Customize immutable types | `__new__` |
| Register subclasses | `__init_subclass__` |
| Control class creation deeply | Metaclass |
| Validate/transform attributes | Descriptors |
| Save memory on many instances | `__slots__` |
| Understand `super()` calls | Check `__mro__` |

## Run It

```bash
python3 08-classes-metaclasses/explore.py
```
