# Contributing to flood-actions

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/flood-actions.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Before Making Changes

- Check existing [issues](https://github.com/jbuffer/flood-actions/issues) to avoid duplicates
- For new features, open an issue for discussion before starting work
- For bug fixes, describe the issue clearly in your PR

### Making Changes

1. **Write clean code**:
   - Follow PEP 8 style guide
   - Add type hints to functions
   - Write docstrings for modules and functions
   - Keep functions focused and single-purpose

2. **Write tests**:
   - Add tests for new features
   - Ensure existing tests pass
   - Aim for >80% code coverage

3. **Run quality checks**:
   ```bash
   # Format code
   black src/ tests/
   isort src/ tests/
   
   # Check linting
   flake8 src/ tests/
   
   # Run tests
   pytest tests/ -v
   
   # Type checking
   mypy src/
   ```

## Submitting Changes

1. **Commit messages**:
   - Use clear, descriptive commit messages
   - Reference related issues: `Fixes #123`
   - Keep commits focused on a single change

2. **Push to your fork**: `git push origin feature/your-feature-name`

3. **Create a Pull Request**:
   - Provide a clear description of changes
   - Link related issues
   - Ensure all CI checks pass
   - Request review from maintainers

## Pull Request Guidelines

- Keep PRs focused on a single concern
- Include tests for new functionality
- Update documentation if needed
- Ensure CI/CD workflows pass
- Be open to feedback and discussion

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_fetch.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run a specific test
pytest tests/test_fetch.py::TestFetchFloodData::test_fetch_flood_data_success
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to code
- Include type hints
- Keep inline comments minimal and meaningful

## Issues and Discussions

- Report bugs by opening an [issue](https://github.com/jbuffer/flood-actions/issues)
- Use descriptive titles and provide reproduction steps
- Include Python version, OS, and relevant error messages

## Recognition

Contributors will be:
- Added to the contributors list
- Mentioned in release notes
- Thanked in commit messages

## Questions?

- Open an issue on GitHub
- Start a discussion for questions and ideas

Thank you for contributing to flood-actions!
