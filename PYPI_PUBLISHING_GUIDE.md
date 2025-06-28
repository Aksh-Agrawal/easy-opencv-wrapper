# PyPI Publishing Guide for Easy OpenCV

This guide will help you publish the Easy OpenCV package to PyPI (Python Package Index).

## 📋 Prerequisites

1. **PyPI Account**: Create accounts on both Test PyPI and PyPI

   - Test PyPI: https://test.pypi.org/account/register/
   - PyPI: https://pypi.org/account/register/

2. **API Tokens**: Generate API tokens for both platforms

   - Test PyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/

3. **Required Tools**: Already installed in the virtual environment
   - `build` - For building packages
   - `twine` - For uploading to PyPI

## 🚀 Publishing Steps

### Step 1: Test Build (Local)

```bash
# Activate virtual environment
d:/Codes/python/easy_cv/.venv/Scripts/activate

# Build and test locally
python build_publish.py build
```

### Step 2: Upload to Test PyPI

```bash
# Upload to Test PyPI first
python build_publish.py test

# When prompted, use your Test PyPI API token:
# Username: __token__
# Password: pypi-... (your Test PyPI token)
```

### Step 3: Test Installation from Test PyPI

```bash
# Test install from Test PyPI
pip install -i https://test.pypi.org/simple/ easy-opencv-wrapper

# Test the package
python -c "from easy_opencv import cv; print('Package works!')"
```

### Step 4: Upload to PyPI (Production)

```bash
# Upload to PyPI (FINAL STEP)
python build_publish.py publish

# When prompted, use your PyPI API token:
# Username: __token__
# Password: pypi-... (your PyPI token)
```

## 🔧 Manual Publishing (Alternative)

If you prefer manual control:

```bash
# 1. Clean and build
python -m build

# 2. Check the built package
twine check dist/*

# 3. Upload to Test PyPI
twine upload --repository testpypi dist/*

# 4. Upload to PyPI
twine upload dist/*
```

## 📦 Package Information

- **Package Name**: `easy-opencv-wrapper`
- **Installation Command**: `pip install easy-opencv-wrapper`
- **Import Statement**: `from easy_opencv import cv`
- **Version**: 1.0.0
- **License**: MIT
- **Python Support**: 3.7+

## 🛡️ Security Notes

1. **Never commit API tokens** to version control
2. **Use environment variables** for tokens in CI/CD
3. **Test thoroughly** on Test PyPI before publishing to PyPI
4. **Cannot delete** published versions from PyPI (only hide them)

## 📁 Files Included in Package

The following files will be included in the published package:

```
easy-opencv-wrapper/
├── easy_opencv/           # Main package code
├── examples/              # Example scripts
├── tests/                 # Test suite
├── README.md             # Main documentation
├── LICENSE               # MIT license
├── CHANGELOG.md          # Version history
├── requirements.txt      # Dependencies
├── pyproject.toml        # Modern Python packaging
└── setup.py              # Legacy setup file
```

## 📚 Documentation Files (Included)

- `DOCUMENTATION.md` - Complete API documentation
- `USAGE_GUIDE.md` - Detailed usage examples
- `PROJECT_STRUCTURE.md` - Package organization
- `EASY_OPENCV_BENEFITS.md` - Benefits analysis
- `WHY_EASY_OPENCV.md` - Design philosophy
- `DIFFERENCES.md` - OpenCV vs Easy OpenCV comparisons

## 🚫 Excluded Files

- `OPERATOR_MANUAL.md` - Internal documentation
- `TEST_ANALYSIS_REPORT.md` - Internal reports
- `test_output/` - Test artifacts
- `__pycache__/` - Python cache files
- `.git/` - Git repository data

## 🔄 Version Updates

For future releases:

1. Update version in `pyproject.toml` and `setup.py`
2. Update `__version__` in `easy_opencv/__init__.py`
3. Add entry to `CHANGELOG.md`
4. Build and test thoroughly
5. Publish to Test PyPI first
6. Then publish to PyPI

## 📞 Support

- **GitHub**: https://github.com/aksh-github/easy-opencv-wrapper
- **Issues**: https://github.com/aksh-github/easy-opencv-wrapper/issues
- **Email**: akshagrawal0801@gmail.com

## ✅ Final Checklist

Before publishing:

- [ ] All tests pass
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] README.md looks good
- [ ] License file included
- [ ] Dependencies correct
- [ ] Package builds without errors
- [ ] Tested on Test PyPI
- [ ] Ready for production publish

**Current Status**: ✅ Ready for PyPI publishing!
