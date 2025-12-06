# Contributing to Email-to-Task Automation System

Thank you for your interest in contributing! This project was built using Spec-Driven Development with Kiro AI.

## Development Process

This project follows a formal specification-driven approach:

1. **Requirements** - EARS-compliant user stories (see `.kiro/specs/email-task-automation/requirements.md`)
2. **Design** - Detailed design with correctness properties (see `.kiro/specs/email-task-automation/design.md`)
3. **Tasks** - Incremental implementation plan (see `.kiro/specs/email-task-automation/tasks.md`)
4. **Implementation** - Code with property-based testing

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. Check if the feature aligns with project goals
2. Open an issue with the feature request template
3. Describe:
   - Use case
   - Proposed solution
   - Alternative approaches
   - Impact on existing functionality

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow existing code style
   - Add tests if applicable
   - Update documentation
4. **Test your changes**:
   ```bash
   python -m pytest
   python check_gmail_status.py
   ```
5. **Commit** with clear messages:
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve issue #123"
   git commit -m "docs: update README"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** with:
   - Clear description
   - Link to related issues
   - Screenshots (if UI changes)
   - Test results

## Code Style

### Python

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions/classes
- Keep functions focused and small

**Example:**
```python
def extract_tasks(email: str) -> List[Dict]:
    """
    Extract actionable tasks from email content.
    
    Args:
        email: Raw email text
        
    Returns:
        List of task dictionaries
    """
    pass
```

### JavaScript

- Use ES6+ features
- Prefer `const` over `let`
- Use meaningful variable names
- Add comments for complex logic

### CSS

- Use BEM naming convention
- Keep selectors specific
- Group related properties
- Add comments for sections

## Testing

### Running Tests

```bash
# Test Gmail connection
python check_gmail_status.py

# Test email processing
python test_manual_email.py

# Clean task data
python clean_tasks.py
```

### Adding Tests

- Add test files to `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names

## Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for system changes
- Update API documentation for endpoint changes
- Add examples for new features

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep formatting consistent

## Project Structure

```
email-task-automation/
├── app.py                 # Flask application
├── gmail_integration.py   # Email polling
├── task_extractor.py     # AI extraction
├── task_store.py         # Storage
├── static/               # Frontend
├── data/                 # Storage
├── .kiro/specs/          # Specifications
└── docs/                 # Documentation
```

## Commit Message Guidelines

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: add email filtering by sender
fix: resolve duplicate task detection issue
docs: update Gmail setup instructions
style: format code with black
refactor: simplify task extraction logic
test: add unit tests for task store
chore: update dependencies
```

## Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address review comments
4. **Approval**: Maintainer approves PR
5. **Merge**: PR merged to main branch

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues/PRs

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing! 🎉
