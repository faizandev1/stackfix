# Contributing to stackfix

Thank you for your interest in contributing. This document outlines how to get started, the development workflow, and the standards we hold code to.

---

## Getting Started

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/stackfix
cd stackfix

# Install all dev dependencies
pip install -e ".[dev]"

# Verify everything works
pytest
stackfix version
```

---

## Project Structure

```
stackfix/
├── stackfix/
│   ├── cli.py              ← Click CLI entry-point
│   ├── config.py           ← Configuration system (TOML + defaults)
│   ├── core/
│   │   ├── parser.py       ← Multi-language error parser
│   │   ├── analyzer.py     ← Orchestrates providers, scores results
│   │   ├── context.py      ← Reads local project for context
│   │   └── history.py      ← SQLite history tracker
│   ├── providers/
│   │   ├── patterns.py     ← Offline bundled pattern database ← great place to contribute
│   │   ├── stackoverflow.py← Stack Overflow API client
│   │   └── github_issues.py← GitHub search client
│   └── ui/
│       ├── display.py      ← All Rich terminal rendering
│       └── themes.py       ← Colour constants
└── tests/
    ├── test_parser.py
    ├── test_analyzer.py
    └── conftest.py
```

---

## Types of Contributions

### 1. Add an error pattern

Edit `stackfix/providers/patterns.py` and append to `_PATTERNS`.

```python
{
    "id":          "py-your-new-pattern",   # kebab-case, unique
    "lang":        ["python"],              # or ["javascript", "bash", …]
    "match_type":  ["SomeError"],           # exact error_type strings
    "match_msg":   r"some regex (?P<key>[^']+)",
    "title":       "Description: {key}",
    "explanation": "Why this happens and what to think about.",
    "fix_code":    "command or code to fix it",
    "fix_type":    "command",               # command | suggestion | patch
    "confidence":  0.85,                    # 0.0 – 1.0
    "tags":        ["relevant", "tags"],
}
```

Then add a test in `tests/test_analyzer.py`.

### 2. Add a language parser

Create a `_parse_<language>` function in `stackfix/core/parser.py` following the existing patterns and register it in `_PARSER_CHAIN`.

### 3. Fix a bug

Open an issue first to discuss. Reference the issue number in your PR: `Fix #123`.

### 4. Improve docs or tests

Always welcome — no issue needed, just open the PR.

---

## Code Standards

- **Formatter:** `black --line-length 100`
- **Linter:** `ruff check stackfix/`
- **Types:** `mypy stackfix/ --ignore-missing-imports`
- **Tests:** `pytest --cov=stackfix`

All four must pass before a PR is merged.

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add PHP error parser
fix: handle Unicode in bash error messages
docs: add contributing guide
test: add edge cases for Go parser
chore: bump rich to 13.7
```

---

## Pull Request Checklist

- [ ] Tests pass locally (`pytest`)
- [ ] Linting passes (`ruff check stackfix/`)
- [ ] New feature has tests
- [ ] README updated if behaviour changed
- [ ] CHANGELOG.md entry added

---

## Code of Conduct

Be kind and constructive. We're all here to build something useful.
