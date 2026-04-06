# 🐍 py-deep-dive

**Python internals explained visually — how things _actually_ work under the hood**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/bBlazewavE/py-deep-dive?style=social)](https://github.com/bBlazewavE/py-deep-dive)

---

## 🤔 The Questions This Repo Answers

**Ever wondered what happens when you write `x = []`?**

- Where does that list live in memory?
- How does Python find it again?
- Why is `a is b` different from `a == b`?
- How do dictionaries achieve O(1) lookup?
- What's actually happening during garbage collection?

**This repo answers those questions — with diagrams, runnable code, and zero hand-waving.**

---

## 🗺️ Topics

Each topic is a self-contained deep dive with visual explanations and runnable Python scripts.

| Topic | What You'll Learn | Status |
|-------|-------------------|---------|
| **[01: Everything is an Object](01-objects/)** | `PyObject` structure, `id()`, `type()`, `is` vs `==`, integer interning | ✅ Complete |
| **[02: Memory Model & GC](02-memory/)** | Reference counting, `gc` module, circular references, weak refs | ✅ Complete |
| **[03: How Dicts Actually Work](03-dict/)** | Hash tables, open addressing, collisions, compact dicts (Python 3.6+) | ✅ Complete |
| **[04: Lists: Dynamic Arrays](04-list/)** | Over-allocation strategy, amortized O(1), list vs tuple memory layout | ✅ Complete |
| **05: Function Calls & Stack** | Call stack, frames, local vs global scope, closures | 🚧 Coming Soon |
| **06: Classes & Metaclasses** | `__new__` vs `__init__`, method resolution order (MRO) | 🚧 Coming Soon |
| **07: Generators & Coroutines** | Generator objects, `yield`, async/await internals | 🚧 Coming Soon |

> 💡 **Tip:** Start with Topic 01 if you're new to Python internals!

---

## 🎯 Who Is This For?

- **📚 Intermediate Python developers** who want to go beyond "it just works"
- **💼 Interview candidates** who need to understand the "why" behind the answers  
- **🚀 Senior/Staff engineers** looking for quick refreshers on CPython internals
- **🎓 CS students** who want practical examples instead of pure theory
- **🔍 Curious minds** who've ever asked *"but WHY does it work that way?"*

**Not for:** Complete beginners to Python (learn the basics first!)

---

## 🏃‍♂️ Quick Start

Every topic has an `explore.py` file you can run immediately:

```bash
# Clone the repo
git clone https://github.com/bBlazewavE/py-deep-dive.git
cd py-deep-dive

# Run any topic (no setup required!)
python3 01-objects/explore.py
python3 02-memory/explore.py  
python3 03-dict/explore.py
python3 04-list/explore.py
```

**Requirements:** Just Python 3.8+ — no virtual env, no dependencies, no hassle.

---

## 🧠 What Makes This Different?

### ❌ Most Python "internals" content:
- Shows you the **what** but not the **why**
- Abstract explanations without runnable examples  
- Assumes you already know C and CPython source code

### ✅ This repo:
- **Visual diagrams** that show memory layouts and data flows
- **Runnable scripts** you can modify and experiment with
- **Real-world examples** that connect to everyday Python coding
- **Interview-ready explanations** you can actually remember and use

---

## 📖 Learning Path

### 🥉 **Beginner Track** (New to internals)
1. [Everything is an Object](01-objects/) — Foundation concepts
2. [Memory Model & GC](02-memory/) — How Python manages memory
3. [Lists: Dynamic Arrays](04-list/) — Your first data structure deep dive

### 🥈 **Intermediate Track** (Some internals knowledge)
1. [How Dicts Actually Work](03-dict/) — Hash table implementation
2. [Memory Model & GC](02-memory/) — Garbage collection details
3. [Everything is an Object](01-objects/) — Object model nuances

### 🥇 **Advanced Track** (Preparing for staff/senior roles)
- Read all topics
- Modify the `explore.py` scripts
- Compare with other language implementations (Go, Java, etc.)

---

## 🤝 Contributing

Found a bug? Want to add a topic? Have a better explanation?

**We welcome:**
- 🐛 Bug fixes and typo corrections
- 📚 New topics or expanded examples
- 🎨 Better diagrams and visualizations  
- 💡 Real-world examples and use cases

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## ⭐ Found This Useful?

If this helped you understand Python better:

1. **Give it a star** ⭐ — helps others discover it
2. **Share it** with fellow Python developers
3. **Open an issue** with topics you'd love to see

---

## 📚 Additional Resources

**Want to go even deeper?**

- 📖 [CPython Internals](https://realpython.com/cpython-internals/) by Real Python
- 🔍 [CPython Source Code](https://github.com/python/cpython) 
- 📺 [Python Core Developer Talks](https://www.youtube.com/results?search_query=python+core+developer)
- 📋 [PEPs (Python Enhancement Proposals)](https://www.python.org/dev/peps/)

---

## 📄 License

[MIT License](LICENSE) — feel free to use this content for learning, teaching, or your own projects!

---

**Made with 🧠 by [Dimple](https://github.com/bBlazewavE) and way too many hours reading CPython source code.**

*"The best way to understand something is to build it yourself." — and then take it apart to see how it really works.*