# Backend Tests

This directory contains tests for the backend API of the notes application.

## Structure

The test directory structure mirrors the main application structure:

```
tests/
├── __init__.py
├── conftest.py           # Test fixtures and setup
├── api/                  # Tests for API endpoints
│   ├── login/
│   ├── notes/
│   └── users/
└── core/                 # Tests for core functionality
    └── ...
```

## Running Tests

### Run all tests

```bash
python -m pytest
```

### Run with coverage report

```bash
python -m pytest --cov=app --cov-report=html
```

This will create an HTML coverage report in the `htmlcov` directory.

### Run specific test files

```bash
python -m pytest tests/api/users/test_routes.py
```

### Run specific test functions

```bash
python -m pytest tests/api/users/test_routes.py::test_read_user_me
```

### Run tests with specific markers

```bash
python -m pytest -m "unit"
python -m pytest -m "integration"
python -m pytest -m "not slow"
```

## Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interaction between components
- **API Tests**: Test API endpoints through the FastAPI TestClient

## Adding New Tests

1. Create a new file with the name pattern `test_*.py`
2. Write test functions with the name pattern `test_*`
3. Use fixtures from `conftest.py` as needed
4. Mark tests with appropriate markers (unit, integration, slow, etc.)

## Mocking Strategy

Most API tests use mocking to isolate the API layer from the service and database layers. The general pattern is:

```python
with patch("app.api.module.routes.Service.method") as mock_service:
    mock_service.return_value = mock_result
    response = client.get("/endpoint", headers=auth_headers)
```

For integration tests that require database interaction, use the `db_session` fixture.
