<![CDATA[<div align="center">

# 🐍 py-deep-dive

### Python internals explained visually — how things *actually* work under the hood

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/bBlazewavE/py-deep-dive?style=social)](https://github.com/bBlazewavE/py-deep-dive)

<br>

*Ever wondered what happens when you write `x = []`?*

*Where does that list live? How does Python find it again? What's really going on in memory?*

**This repo answers those questions — with diagrams, runnable code, and zero hand-waving.**

<br>

[Explore Topics ↓](#-topics) · [Run the Code](#-running-the-code) · [Contribute](CONTRIBUTING.md)

</div>

---

## 🗺️ Topics

Each topic is a self-contained deep dive with visual explanations and runnable Python scripts.

| # | Topic | What You'll Learn |
|---|-------|-------------------|
| **01** | [Everything is an Object](01-objects/) | `PyObject`, `id()`, `type()`, `is` vs `==`, interning |
| **02** | [Memory Model & GC](02-memory/) | Reference counting, `gc` module, circular references, weak refs |
| **03** | [How Dicts Actually Work](03-dict/) | Hash tables, open addressing, collisions, compact dicts |
| **04** | [Lists: Dynamic Arrays](04-list/) | Over-allocation, amortized O(1), list vs tuple memory |

> 🚧 More topics coming — **star this repo** to stay updated!

---

## 🎯 Who Is This For?

- **Intermediate Python devs** who want to go beyond "it just works"
- **Interview preppers** who want to actually understand the answers
- **Senior/Staff engineers** looking for quick refreshers on CPython internals
- **CS students** who want practical examples instead of textbook theory
- Anyone who's ever asked *"but WHY does it work that way?"*

---

## 🏃 Running the Code

Every topic has an `explore.py` you can run immediately:

```bash
git clone https://github.com/bBlazewavE/py-deep-dive.git
cd py-deep-dive

# Pick any topic
python3 01-objects/explore.py
python3 02-memory/explore.py
python3 03-dict/explore.py
python3 04-list/explore.py
```

No dependencies. No virtual env. Just Python 3.8+ and curiosity.

---

## ⭐ Found This Useful?

If this helped you understand Python better, **give it a star** — it helps others find it too.

Got a topic you'd love to see? [Open an issue](https://github.com/bBlazewavE/py-deep-dive/issues) or [contribute](CONTRIBUTING.md)!

---

<div align="center">

**Made with 🧠 and too many hours reading CPython source code.**

</div>
]]>