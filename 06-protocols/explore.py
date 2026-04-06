"""
06 — Protocols: Interfaces Without Inheritance (PEP 544)
Structural subtyping in Python 3.8+
"""

from typing import Protocol, runtime_checkable, TypeVar, get_type_hints


# ============================================================
# 1. The Old Way: ABCs force inheritance
# ============================================================
print("=" * 60)
print("1. ABC vs Protocol")
print("=" * 60)

from abc import ABC, abstractmethod


class DrawableABC(ABC):
    @abstractmethod
    def draw(self) -> None: ...


class CircleABC(DrawableABC):
    def draw(self) -> None:
        print("  [ABC] drawing circle")


# Must inherit — no choice
print(f"CircleABC bases: {CircleABC.__bases__}")
print(f"Is instance of DrawableABC? {isinstance(CircleABC(), DrawableABC)}")


# ============================================================
# 2. The Protocol Way: no inheritance needed
# ============================================================
print("\n" + "=" * 60)
print("2. Protocol — structural subtyping")
print("=" * 60)


class Drawable(Protocol):
    def draw(self) -> None: ...


class Circle:
    """No inheritance from Drawable!"""

    def draw(self) -> None:
        print("  [Protocol] drawing circle")


class Square:
    def draw(self) -> None:
        print("  [Protocol] drawing square")


class NotDrawable:
    def move(self) -> None: ...


def render(shape: Drawable) -> None:
    """Type checker knows Circle satisfies Drawable without inheritance."""
    shape.draw()


render(Circle())
render(Square())

print(f"\nCircle bases: {Circle.__bases__}  ← no Drawable!")
print(f"Square bases: {Square.__bases__}  ← no Drawable!")

# Type checker would flag this:
# render(NotDrawable())  # ❌ mypy error: missing draw()


# ============================================================
# 3. runtime_checkable — isinstance() with Protocols
# ============================================================
print("\n" + "=" * 60)
print("3. @runtime_checkable")
print("=" * 60)


@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


class MyResource:
    def close(self) -> None:
        print("  closing resource")


class NotCloseable:
    pass


import io

print(f"MyResource is Closeable?  {isinstance(MyResource(), Closeable)}")
print(f"StringIO is Closeable?    {isinstance(io.StringIO(), Closeable)}")
print(f"NotCloseable is Closeable? {isinstance(NotCloseable(), Closeable)}")

# ⚠️ Caveat: only checks method EXISTS, not signature
class BadClose:
    def close(self, x: int, y: int) -> str:  # wrong signature!
        return "nope"

print(f"\nBadClose is Closeable?    {isinstance(BadClose(), Closeable)}")
print("  ↑ True! runtime_checkable only checks name exists, not params")


# ============================================================
# 4. Protocols with attributes
# ============================================================
print("\n" + "=" * 60)
print("4. Protocol with attributes")
print("=" * 60)


class Named(Protocol):
    name: str


class User:
    def __init__(self, name: str):
        self.name = name


class Config:
    name = "default"


def greet(thing: Named) -> str:
    return f"Hello, {thing.name}"


print(greet(User("Dimple")))
print(greet(Config()))


# ============================================================
# 5. Combining Protocols
# ============================================================
print("\n" + "=" * 60)
print("5. Combining Protocols (intersection types)")
print("=" * 60)


class Readable(Protocol):
    def read(self) -> str: ...


class Writable(Protocol):
    def write(self, data: str) -> None: ...


class ReadWrite(Readable, Writable, Protocol):
    """Must satisfy both Readable AND Writable."""
    ...


class Filelike:
    def read(self) -> str:
        return "data"

    def write(self, data: str) -> None:
        pass


@runtime_checkable
class ReadWriteCheck(Readable, Writable, Protocol):
    ...


print(f"Filelike satisfies ReadWrite? {isinstance(Filelike(), ReadWriteCheck)}")
print(f"StringIO satisfies ReadWrite? {isinstance(io.StringIO(), ReadWriteCheck)}")


# ============================================================
# 6. Real-world: testing without inheritance
# ============================================================
print("\n" + "=" * 60)
print("6. Real-world: easy mocking for tests")
print("=" * 60)

import json


class HTTPClient(Protocol):
    def get(self, url: str) -> bytes: ...


# Production client would use requests/httpx
# But for testing, just match the shape:
class FakeClient:
    def get(self, url: str) -> bytes:
        return b'{"status": "ok", "data": [1, 2, 3]}'


def fetch_data(client: HTTPClient) -> dict:
    return json.loads(client.get("https://api.example.com"))


result = fetch_data(FakeClient())
print(f"  fetch_data result: {result}")
print(f"  FakeClient bases: {FakeClient.__bases__}  ← no HTTPClient!")


# ============================================================
# 7. Key takeaway
# ============================================================
print("\n" + "=" * 60)
print("KEY TAKEAWAY")
print("=" * 60)
print("""
  ABCs  = "You MUST inherit from me" (nominal)
  Protocol = "Just have the right methods" (structural)

  Protocol matches Python's duck typing philosophy:
  If it looks like a duck and quacks like a duck... ✅

  Use Protocol when:
  • You want interfaces without forcing inheritance
  • Third-party classes need to satisfy your interface
  • Testing: mock objects without inheriting from anything
  • Plugin systems: don't constrain plugin authors
""")
