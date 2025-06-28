# Contributing to Smart Warehouse Management System

We welcome contributions to the Smart Warehouse Management System! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or bug fix

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/smart-warehouse-system.git
cd smart-warehouse-system

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt

# Set up pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

## 📝 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write clean, readable code

### Python Code Style
```python
def calculate_inventory_value(products: List[Product]) -> float:
    """Calculate total value of inventory.
    
    Args:
        products: List of product objects
        
    Returns:
        Total monetary value of all products
    """
    return sum(product.price * product.quantity for product in products)
```

## 🧪 Testing

Always include tests for new features:

```bash
# Run existing tests
./test_phase3.sh

# Add new tests in appropriate test files
# Follow the existing test structure
```

## 📋 Pull Request Process

1. **Create a descriptive branch name**
   ```bash
   git checkout -b feature/add-barcode-scanning
   git checkout -b fix/inventory-calculation-bug
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   ./test_phase3.sh
   python -m pytest  # If pytest is available
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: add barcode scanning functionality
   
   - Implement QR/barcode reader integration
   - Add product lookup by barcode
   - Update inventory management interface"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/add-barcode-scanning
   ```

## 🏷️ Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## 🎯 Areas for Contribution

### High Priority
- AI/ML improvements for demand forecasting
- Performance optimizations
- Additional test coverage
- API documentation improvements

### Medium Priority
- Mobile responsive design improvements
- Additional inventory management features
- Integration with external systems
- Advanced analytics features

### Low Priority
- UI/UX enhancements
- Code cleanup and refactoring
- Additional language support

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment information**
   - Python version
   - Operating system
   - Browser (for frontend issues)

2. **Steps to reproduce**
   - Clear step-by-step instructions
   - Expected vs actual behavior

3. **Error messages**
   - Full error logs
   - Screenshots if relevant

4. **Additional context**
   - Configuration details
   - Data that triggers the issue

## 💡 Feature Requests

For new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Propose a solution** with technical details
4. **Consider the impact** on existing functionality

## 📖 Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update API documentation for endpoint changes
- Include code examples for complex features

## 🔍 Code Review Guidelines

As a reviewer:
- Be constructive and respectful
- Focus on code quality and maintainability
- Test the changes locally when possible
- Suggest improvements rather than just pointing out problems

As a contributor:
- Respond to feedback promptly
- Be open to suggestions and changes
- Test your updates after making changes

## 📞 Getting Help

- Create an issue for questions
- Join discussions in existing issues
- Check the documentation first
- Be patient and respectful

## 🎉 Recognition

Contributors will be:
- Listed in the project contributors
- Mentioned in release notes for significant contributions
- Recognized in the community

Thank you for contributing to Smart Warehouse Management System!
