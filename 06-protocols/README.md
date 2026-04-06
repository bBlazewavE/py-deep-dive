# 06 — Protocols: Interfaces Without Inheritance

> **PEP 544** · Python 3.8+ · `typing.Protocol`

## The Problem

Traditional interfaces in Python use ABCs (Abstract Base Classes):

```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None: ...

class Circle(Drawable):  # forced to inherit
    def draw(self) -> None:
        print("drawing circle")
```

This is **nominal subtyping** — the class must explicitly declare "I am a `Drawable`" by inheriting from it. But Python is a duck-typed language. If it quacks like a duck...

## The Solution: Protocols

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("drawing circle")

def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # ✅ No inheritance needed!
```

This is **structural subtyping** — the type checker looks at the *shape* of the object, not its inheritance tree.

## Nominal vs Structural Subtyping

| | Nominal (ABC) | Structural (Protocol) |
|---|---|---|
| **Requires inheritance?** | Yes | No |
| **Type checking** | `isinstance()` built-in | Type checker infers compatibility |
| **Duck typing friendly?** | No — forces coupling | Yes — matches Python's philosophy |
| **Third-party classes** | Must wrap or monkey-patch | Just work if they match |
| **Runtime cost** | MRO lookup | Zero (checked at type-check time) |

## Key Concepts

### 1. Basic Protocol

```python
from typing import Protocol

class Closeable(Protocol):
    def close(self) -> None: ...

# Any class with a close() method satisfies this
import io
def cleanup(resource: Closeable) -> None:
    resource.close()

cleanup(io.StringIO())  # ✅ StringIO has close()
```

### 2. Protocol with Attributes

```python
class Named(Protocol):
    name: str

class User:
    def __init__(self, name: str):
        self.name = name

def greet(thing: Named) -> str:
    return f"Hello, {thing.name}"

greet(User("Dimple"))  # ✅
```

### 3. Runtime Checkable

By default, Protocols are type-check-time only. Add `@runtime_checkable` for `isinstance()` support:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None: ...

print(isinstance(Circle(), Drawable))  # True
```

⚠️ **Caveat:** `runtime_checkable` only checks method/attribute *existence*, not signatures. It won't catch wrong parameter types.

### 4. Generic Protocols

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Container(Protocol[T]):
    def get(self) -> T: ...
    def set(self, value: T) -> None: ...
```

### 5. Combining Protocols (Intersection)

```python
class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

class ReadWrite(Readable, Writable, Protocol):
    ...
```

## Under the Hood

### How does the type checker know?

The type checker (mypy, pyright) compares the **method resolution order (MRO)** and **attribute signatures** of the target class against the Protocol definition. It's purely static analysis — no runtime metaclass magic like ABCs use.

### ABC vs Protocol internals

```
ABC path:     class → ABCMeta.__init__ → registers abstract methods
              isinstance() → ABCMeta.__instancecheck__ → checks __abstractmethods__

Protocol path: class → _ProtocolMeta (3.8-3.11) / normal type (3.12+)
               Type checker → structural comparison at analysis time
               @runtime_checkable → adds __instancecheck__ that checks attrs exist
```

### Python 3.12+ improvement

PEP 544 originally used a custom metaclass. Python 3.12 simplified this — `Protocol` no longer needs special metaclass machinery, making it lighter and more compatible with other metaclasses.

## When to Use What

| Use Case | Use |
|---|---|
| You own all the classes | Either works — Protocol is cleaner |
| Third-party classes must conform | Protocol (can't change their inheritance) |
| Need runtime `isinstance()` checks | ABC or `@runtime_checkable` Protocol |
| Defining a plugin interface | Protocol — don't force inheritance on plugins |
| Need default method implementations | ABC — Protocols can't have method bodies |

## Real-World Example: Testing

Protocols shine in testing — define what you need, mock freely:

```python
class HTTPClient(Protocol):
    def get(self, url: str) -> bytes: ...

class FakeClient:
    def get(self, url: str) -> bytes:
        return b'{"ok": true}'

def fetch_data(client: HTTPClient) -> dict:
    return json.loads(client.get("https://api.example.com"))

# In tests — no need to inherit from HTTPClient
fetch_data(FakeClient())  # ✅
```

## Run It

```bash
python3 06-protocols/explore.py
```
