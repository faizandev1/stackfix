<div align="center">

# stackfix

**Pipe any error. Get the fix. Instantly.**

[![CI](https://github.com/yourusername/stackfix/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/stackfix/actions)
[![PyPI](https://img.shields.io/pypi/v/stackfix?color=4285F4)](https://pypi.org/project/stackfix)
[![Python](https://img.shields.io/pypi/pyversions/stackfix?color=4285F4)](https://pypi.org/project/stackfix)
[![License: MIT](https://img.shields.io/badge/License-MIT-34A853.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/stackfix?color=FBBC05)](https://pypi.org/project/stackfix)

---

```
python app.py 2>&1 | stackfix
```

*Stop Googling. Start fixing.*

</div>

---

## The Problem

Every developer — every day — wastes hours doing this:

```
Traceback (most recent call last):
  File "app.py", line 4, in <module>
    import pandas as pd
ModuleNotFoundError: No module named 'pandas'
```

1. Copy the error
2. Open a browser
3. Search Stack Overflow
4. Read 4 tabs
5. Try 3 suggestions
6. Finally fix it

**stackfix collapses all of that into one command.**

---

## What It Does

```
┌─────────────────────────────────────────────────────────────────────┐
│  python app.py 2>&1 | stackfix                                       │
│                                                                      │
│  ● Error Detected                                                    │
│  🐍 ModuleNotFoundError: No module named 'pandas'                   │
│                                                                      │
│  ✦ 3 Fixes Found                                                    │
│                                                                      │
│  ┌── 1/3 ─────────────────────────────────────────── 95% ──────┐   │
│  │  Missing Python package: pandas                               │   │
│  │  The package `pandas` is not installed in the current env.   │   │
│  │                                                               │   │
│  │  $ pip install pandas                                         │   │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

stackfix:
- **Parses** the error — extracts type, message, traceback, line numbers
- **Searches** 3 sources in parallel: local pattern DB + Stack Overflow + GitHub Issues
- **Scores** every result with a confidence percentage
- **Renders** a clean, ranked list of actionable fixes

---

## Installation

```bash
pip install stackfix
```

**Verify:**
```bash
stackfix version
```

---

## Usage

### Pipe any error

```bash
# Python
python app.py 2>&1 | stackfix

# Node.js
node server.js 2>&1 | stackfix

# Any shell command
./deploy.sh 2>&1 | stackfix

# Docker
docker-compose up 2>&1 | stackfix
```

### Pass directly

```bash
stackfix "ModuleNotFoundError: No module named 'requests'"
stackfix "KeyError: 'user_id'"
stackfix "EADDRINUSE: address already in use :::3000"
```

### Force language

```bash
stackfix --lang bash "permission denied"
stackfix --lang docker "manifest not found"
```

### Offline mode (no network requests)

```bash
stackfix --offline "ZeroDivisionError: division by zero"
```

### Output formats

```bash
# JSON (for scripting / piping into jq)
stackfix --format json "ModuleNotFoundError: …" | jq '.fixes[0].fix_code'

# Markdown (for bug reports, docs)
stackfix --format markdown "TypeError: …" > REPORT.md

# Plain text (for logging)
stackfix --format plain "IndexError: …" >> debug.log
```

### History

```bash
# List recent errors
stackfix history list

# Search past errors
stackfix history search "ModuleNotFoundError"

# Get full details of entry #42
stackfix history get 42

# Clear history
stackfix history clear
```

---

## How It Works

```
Raw error text
      │
      ▼
 ┌─────────────────────────────────┐
 │         Parser Layer            │  Detects language, extracts error_type,
 │  Python · JS · Bash · Docker    │  message, traceback frames
 │  Go · Rust · Java · Generic     │
 └──────────────┬──────────────────┘
                │
                ▼
 ┌─────────────────────────────────┐
 │       Provider Layer (async)    │
 │                                 │
 │  LocalPatterns  ──── 0ms        │  120+ bundled patterns, works offline
 │  StackOverflow  ──── ~500ms     │  Searches SO API, extracts accepted answers
 │  GitHub Issues  ──── ~800ms     │  Searches GitHub for related discussions
 └──────────────┬──────────────────┘
                │
                ▼
 ┌─────────────────────────────────┐
 │        Analyzer                 │  Deduplicates, scores confidence (0–1),
 │    Score · Sort · Trim          │  sorts by score + community votes
 └──────────────┬──────────────────┘
                │
                ▼
 ┌─────────────────────────────────┐
 │         Rich UI                 │  Colour-coded panels, syntax-highlighted
 │   (or JSON / Markdown / plain)  │  code blocks, confidence badges
 └─────────────────────────────────┘
```

---

## Supported Languages

| Language       | Error parsing | Pattern DB | Notes                        |
|----------------|:-------------:|:----------:|------------------------------|
| Python         | ✅            | ✅         | Full traceback + all builtins |
| JavaScript     | ✅            | ✅         | Node.js error codes          |
| TypeScript     | ✅            | ✅         | Via JS parser                |
| Bash / Shell   | ✅            | ✅         | Exit codes, common errors    |
| Docker         | ✅            | ✅         | Daemon + image errors        |
| Go             | ✅            | ✅         | Compile errors + panics      |
| Rust           | ✅            | ✅         | Borrow checker errors        |
| Java           | ✅            | ⚡ planned | Exception hierarchy          |

---

## Configuration

stackfix reads `~/.config/stackfix/config.toml` (and `.stackfix.toml` at project root).

Generate the default config:

```bash
stackfix config --init
```

Key options:

```toml
[general]
max_results       = 5       # Max fix suggestions
confidence_cutoff = 0.25    # Minimum confidence to show (0–1)
offline           = false   # Disable all network requests

[providers]
stackoverflow  = true
github_issues  = true
local_patterns = true

[output]
format = "rich"   # rich | plain | json | markdown
```

---

## Adding Custom Patterns

You can extend the pattern database without forking — just open a PR adding entries to `stackfix/providers/patterns.py`.

Each pattern follows this schema:

```python
{
    "id":          "py-my-error",             # unique id
    "lang":        ["python"],                # languages this applies to
    "match_type":  ["MyCustomError"],         # error_type to match
    "match_msg":   r"some (?P<detail>regex)", # regex on the message
    "title":       "Fix for {detail}",        # {named groups} are interpolated
    "explanation": "Why this happens…",
    "fix_code":    "pip install something",   # shell/code to run
    "fix_type":    "command",                 # command | suggestion | patch
    "confidence":  0.90,
    "tags":        ["tag1", "tag2"],
}
```

---

## Contributing

Contributions are what make this project useful to the whole community.

```bash
# 1. Fork → Clone
git clone https://github.com/yourusername/stackfix
cd stackfix

# 2. Create a branch
git checkout -b feat/your-feature

# 3. Install dev dependencies
pip install -e ".[dev]"

# 4. Make changes + add tests

# 5. Run the full suite
pytest

# 6. Open a PR
```

Good first contributions:
- 🔵 **Add a pattern** — found an error stackfix doesn't handle? Add a pattern entry.
- 🟡 **Add a language parser** — PHP, Ruby, C#, Kotlin?
- 🟢 **Improve the UI** — better formatting, progress bars, interactive fix selection.
- 🔴 **Write tests** — more coverage is always welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## Roadmap

- [ ] Interactive fix selector (arrow-key navigation, apply fix directly)
- [ ] `--watch` mode — monitor a log file and fix errors in real-time
- [ ] VS Code extension
- [ ] PHP, Ruby, C#, Kotlin parsers
- [ ] AI-powered fallback (local Ollama / OpenAI) for unknown errors
- [ ] `stackfix explain` — explain what an error means in plain English

---

## Author

Built by **Faizan** — open to contributions, feedback, and ideas.

If this saved you time, a ⭐ star goes a long way.

---

## License

MIT © Faizan. See [LICENSE](LICENSE).
