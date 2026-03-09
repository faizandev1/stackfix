# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning: [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2025-03-09

### Added
- Multi-language error parser: Python, JavaScript, TypeScript, Bash, Docker, Go, Rust, Java
- Offline local pattern database with 40+ curated patterns
- Stack Overflow API provider (scored by votes + accepted status)
- GitHub Issues provider (scored by reactions + state)
- Async provider orchestration with configurable timeout
- Confidence scoring system (0.0 – 1.0) with colour-coded output
- Rich terminal UI with Google-inspired colour palette
- JSON, Markdown, and plain-text output formats
- SQLite-backed error history (list / get / search / clear)
- TOML configuration (~/.config/stackfix/config.toml + .stackfix.toml)
- Project context reader (reads requirements.txt, package.json, etc.)
- `--offline` flag for zero-network operation
- `stackfix config --init` for default config generation
- Full test suite with network isolation
- GitHub Actions CI (5 Python versions × 3 OS)
- PyPI publish workflow with OIDC trusted publishing
