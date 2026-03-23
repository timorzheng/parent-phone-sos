# Contributing to Parent Phone SOS

Thank you for your interest in contributing to Parent Phone SOS! We love your input and appreciate all contributions, from bug reports to feature requests to code improvements.

## 🤝 Ways to Contribute

### 1. Report Bugs
Found a bug? Please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable

### 2. Suggest Features
Have an idea for improvement? Open an issue labeled as a feature request with:
- Clear description of the feature
- Why you think it's needed
- Possible implementation approach
- Any mockups or examples

### 3. Improve Documentation
Help us improve docs by:
- Fixing typos or clarity issues
- Adding missing information
- Creating tutorials or guides
- Translating documentation

### 4. Submit Code Changes
Want to code? Follow these steps:

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/timorzheng/parent-phone-sos.git
cd parent-phone-sos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov pytest-asyncio black flake8

# Copy environment file
cp .env.example .env
# Add your test API keys to .env
```

#### Development Workflow

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```

2. **Make your changes:**
   - Follow the coding style guidelines (see below)
   - Write tests for new features
   - Update documentation as needed

3. **Run tests:**
   ```bash
   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=src

   # Run specific test file
   pytest tests/test_analyzer.py
   ```

4. **Format code:**
   ```bash
   # Format with black
   black src/ tests/

   # Check with flake8
   flake8 src/ tests/
   ```

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   # or
   git commit -m "fix: resolve issue #123"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request:**
   - Go to GitHub and create a PR
   - Fill in the PR template
   - Link any related issues
   - Wait for review

## 📝 Coding Standards

### Style Guide

- **Python:** Follow PEP 8
- **Use type hints:** All functions should have type annotations
- **Docstrings:** Public functions must have docstrings
- **Comments:** Comment complex logic, not obvious code

### Example

```python
def analyze_screenshot(
    image: Image.Image,
    question: str,
    provider: Optional[str] = None
) -> Optional[AnalysisResult]:
    """
    Analyze a screenshot using AI.

    Args:
        image: PIL Image object
        question: User's question/problem description
        provider: Preferred provider ('openai' or 'anthropic')

    Returns:
        AnalysisResult or None if analysis fails
    """
    # Implementation here
    pass
```

### Testing Requirements

- Write tests for all new features
- Aim for >80% code coverage
- Use descriptive test names
- Mock external API calls

Example test:
```python
def test_analyze_screenshot_returns_valid_result(sample_image):
    """Test that analyze_screenshot returns a valid AnalysisResult."""
    result = analyze_screenshot(sample_image, "Test question")

    assert isinstance(result, AnalysisResult)
    assert len(result.steps) > 0
    assert result.difficulty in ["easy", "medium", "hard"]
```

## 🎨 Feature Development

### Adding a New Feature

1. **Create an issue** to discuss the feature
2. **Wait for feedback** before starting implementation
3. **Branch from main** for development
4. **Add tests** as you develop
5. **Update documentation** (README, API docs, docstrings)
6. **Create a PR** with clear description

### Adding to FAQ Database

Edit `src/faq.py` and add your FAQ item:

```python
"feature_id": FAQItem(
    id="feature_id",
    category="Feature Name in Chinese",
    category_en="Feature Name in English",
    steps=[
        "Step 1 instruction",
        "Step 2 instruction",
        # ... more steps
    ],
    platforms=["iPhone", "Android"],
),
```

### Adding a New API Endpoint

1. Update `src/models.py` with new data models
2. Add endpoint to `src/main.py`
3. Add tests in `tests/test_api.py`
4. Update `docs/API.md`

Example:
```python
@app.get("/api/newfeature")
async def new_feature():
    """Description of the endpoint."""
    return {"message": "success"}
```

## 🐛 Bug Reports

Use the bug report template when creating an issue:

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**
- OS: [e.g. macOS, Windows, Linux]
- Python Version: [e.g. 3.9, 3.11]
- Browser (if web UI): [e.g. Chrome, Firefox]
```

## 📋 Pull Request Process

1. **Fork** the repository
2. **Branch** from `main`
3. **Commit** with clear messages
4. **Push** to your fork
5. **Create PR** with:
   - Clear title
   - Description of changes
   - Related issues (if any)
   - Screenshots (if UI changes)
   - Checklist of tasks completed

### PR Checklist

- [ ] My code follows the style guidelines
- [ ] I have run tests locally (`pytest`)
- [ ] I have added/updated tests for my changes
- [ ] I have updated documentation
- [ ] No new warnings or errors in linter output
- [ ] I have tested on multiple platforms (if applicable)

## 🎯 Priority Areas

We're especially looking for contributions in these areas:

- [ ] Improved image annotation algorithms
- [ ] Support for more languages
- [ ] Mobile app version
- [ ] Video tutorial support
- [ ] Real-time video guidance
- [ ] Additional FAQ entries
- [ ] Performance optimizations
- [ ] More comprehensive tests

## 📚 Resources

- **Documentation:** See `docs/` directory
- **API Reference:** `docs/API.md`
- **Code Style:** PEP 8
- **Testing:** `tests/` directory

## ❓ Questions?

- Open a GitHub Discussion
- Join our community chat
- Email: support@parentphonesos.com

## 🙏 Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms:

- Be respectful and inclusive
- Welcome people of all backgrounds
- Focus on constructive criticism
- Report inappropriate behavior

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under its MIT License.

## 🎉 Recognition

We recognize all contributions! Contributors will be:
- Added to the CONTRIBUTORS.md file
- Mentioned in release notes
- Credited in documentation

---

Thank you for making Parent Phone SOS better! 🌟
