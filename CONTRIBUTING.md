# Contributing to NFL_stats

Thank you for your interest in contributing to **NFL_stats**! Contributions help improve the project for everyone using it for fantasy football analysis, NFL statistics exploration, and related tooling.

This document outlines how to contribute code, report issues, and suggest improvements.

---

# Table of Contents

- Code of Conduct
- How to Contribute
- Development Setup
- Branching Strategy
- Pull Request Process
- Coding Standards
- Testing
- Documentation
- Reporting Issues
- Feature Requests

---

# Code of Conduct

Please be respectful and constructive when interacting with other contributors.  
Disagreements are fine, but discussions should always remain professional and focused on improving the project.

---

# How to Contribute

You can contribute in several ways:

## 1. Reporting Bugs

If you find a bug:

1. Check if the issue already exists.
2. If not, create a new issue including:
   - A clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs or screenshots

---

## 2. Suggesting Features

Feature suggestions are welcome.

When submitting a feature request:

- Describe the feature
- Explain the use case
- Include examples if possible

---

## 3. Contributing Code

To contribute code:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Test your changes
5. Submit a Pull Request

---

# Development Setup

Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/NFL_stats.git
cd NFL_stats
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies (if a requirements file exists):

```bash
pip install -r requirements.txt
```

---

# Branching Strategy

Use descriptive branch names:

```
feature/add-new-stat-endpoint
bugfix/fix-player-mapping
docs/update-readme
```

General format:

```
type/short-description
```

Types include:

- `feature`
- `bugfix`
- `docs`
- `refactor`
- `test`

---

# Pull Request Process

When opening a Pull Request:

1. Ensure your code runs without errors
2. Keep PRs focused on a single feature or fix
3. Provide a clear description of:
   - What changed
   - Why it changed
   - Any testing performed

Example PR title:

```
Add Sleeper league matchup endpoint
```

---

# Coding Standards

Please follow these guidelines.

## Python

- Follow **PEP8 style guidelines**
- Use descriptive variable names
- Avoid unnecessary complexity
- Add comments where logic may be unclear

Example:

```python
def get_player_stats(player_id):
    """Fetch statistics for a player."""
```

---

# Testing

Before submitting a Pull Request:

- Run existing tests (if present)
- Verify that new features work as expected
- Avoid breaking existing functionality

---

# Documentation

If your contribution adds functionality:

- Update the README if necessary
- Add docstrings to functions
- Include usage examples when appropriate

---

# Reporting Issues

Create an issue using the following format:

```
Title: Short summary

Description:
Detailed explanation of the issue.

Steps to Reproduce:
1.
2.
3.

Expected Behavior:
What should happen.

Actual Behavior:
What actually happened.
```

---

# Feature Requests

Feature requests should include:

- A clear description
- Why the feature is useful
- Example usage

---

# Questions

If you have questions about contributing, open a discussion or issue in the repository.

---

Thank you for contributing to **NFL_stats**!
