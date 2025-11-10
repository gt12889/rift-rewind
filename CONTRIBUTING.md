# Contributing to Rift Rewind

Thank you for your interest in contributing to Rift Rewind!

## Development Setup

1. Follow the setup instructions in `SETUP.md`
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes: `pytest tests/`
5. Commit your changes: `git commit -m "Add feature"`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Add integration tests for API endpoints

## AWS Resource Tagging

All AWS resources must be tagged with:
- Key: `rift-rewind-hackathon`
- Value: `2025`

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

