---
name: pr-review
description: review pull requests for code quality. Use when reviewing PRs or checking code changes.
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

When reviewing code in this python repository, please follow these guidelines:

## Code Quality
- Ensure that the code follows PEP 8 style guidelines.
- Check for clear and descriptive variable and function names.
- Look for proper use of comments and docstrings to explain complex logic.
- No hardcoded secrets or sensitive information should be present in the code.

## Python Best Practices
- Ensure that functions and methods are small and focused on a single task.
- Check for proper error handling and exception management.
- Verify that the code uses list comprehensions and generator expressions where appropriate.
- Ensure that the code avoids unnecessary global variables and uses local scope effectively.
- Check for proper use of Python's built-in data structures (lists, dictionaries, sets, etc.) and their methods.
- Ensure that the code uses Python's standard library effectively and avoids reinventing the wheel.
- Check for proper use of classes and object-oriented programming principles, such as encapsulation and inheritance.
- Ensure that the code uses type hints and annotations where appropriate for better readability and maintainability.
