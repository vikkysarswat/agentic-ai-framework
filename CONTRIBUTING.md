# Contributing to Agentic AI Framework

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/agentic-ai-framework.git`
3. Add upstream remote: `git remote add upstream https://github.com/vikkysarswat/agentic-ai-framework.git`

## Development Setup

### Using Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install
```

### Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-new-tool` - New features
- `fix/memory-leak` - Bug fixes
- `docs/update-readme` - Documentation
- `refactor/agent-class` - Code refactoring
- `test/add-orchestrator-tests` - Tests

### Commit Messages

Follow the conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(agent): add support for custom reasoning strategies

fix(memory): resolve vector store initialization error

docs(readme): update installation instructions
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agentic_framework --cov-report=html

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::test_agent_creation
```

### Writing Tests

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Include both positive and negative test cases
- Use fixtures for common setup

Example:

```python
import pytest

@pytest.mark.asyncio
async def test_agent_executes_task_successfully():
    """Test that agent successfully executes a simple task."""
    agent = Agent(config=AgentConfig(name="Test", role="Test", goal="Test"))
    result = await agent.execute("Test task")
    assert result["success"] is True
```

## Submitting Changes

### Before Submitting

1. Update your branch with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Run tests and linting:
   ```bash
   pytest
   black .
   flake8
   mypy agentic_framework
   ```

3. Update documentation if needed

### Pull Request Process

1. Push your changes to your fork
2. Create a Pull Request against the `main` branch
3. Fill out the PR template completely
4. Link any related issues
5. Wait for review and address feedback

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Style Guidelines

### Python Code Style

We use:
- **Black** for code formatting (line length: 100)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

### Code Quality

- Write clear, self-documenting code
- Add docstrings to all public functions and classes
- Use type hints
- Keep functions focused and small
- Follow SOLID principles

### Documentation Style

- Use Google-style docstrings
- Include examples in docstrings when helpful
- Update README.md for user-facing changes
- Add inline comments for complex logic

Example docstring:

```python
def execute_task(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a task with the given context.
    
    Args:
        task: The task description to execute
        context: Additional context for task execution
        
    Returns:
        A dictionary containing:
            - success: Whether execution succeeded
            - result: The execution result
            - error: Error message if failed
            
    Raises:
        ValueError: If task is empty
        
    Example:
        >>> result = execute_task("Analyze data", {"data": [1, 2, 3]})
        >>> print(result["success"])
        True
    """
```

## Areas for Contribution

We especially welcome contributions in:

- **New Tools**: Implement new tools for agents
- **LLM Providers**: Add support for more LLM providers
- **Memory Systems**: Implement alternative memory backends
- **Examples**: Create new example use cases
- **Documentation**: Improve guides and tutorials
- **Tests**: Increase test coverage
- **Performance**: Optimize slow operations
- **Bug Fixes**: Fix reported issues

## Getting Help

If you need help:

- Check existing documentation
- Search existing issues
- Ask in discussions
- Join our community chat

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to join the core team (for significant contributions)

Thank you for contributing! 🚀