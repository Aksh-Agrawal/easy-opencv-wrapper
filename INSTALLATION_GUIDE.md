# Easy OpenCV Installation Guide

## 🚀 Installation Instructions

### Step 1: Install the Package

The package is published on PyPI with the name `easy-opencv-wrapper`. Install it using pip:

```bash
pip install easy-opencv-wrapper
```

### Step 2: Import and Use

After installation, you can import and use the package in your Python code:

```python
# Import the main module (note: underscores, not hyphens!)
from easy_opencv import cv

# Or import specific functions
from easy_opencv.image_operations import load_image, save_image
from easy_opencv.filters import apply_gaussian_blur
```

### ⚠️ Critical Import Note

**The PyPI package name uses hyphens (`easy-opencv-wrapper`), but the import name uses underscores (`easy_opencv`)**. This is standard Python convention.

```python
# ❌ WRONG - Will cause ModuleNotFoundError
import easy_opencv_wrapper
from easy_opencv_wrapper import cv

# ✅ CORRECT - This is the proper import
from easy_opencv import cv
```

## ⚠️ Common Installation Issues

### Issue 1: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'easy_opencv'
```

**Cause**: Package not installed or trying to import with wrong name.

**Solutions**:

1. Make sure you have installed the package first:

   ```bash
   pip install easy-opencv-wrapper
   ```

2. Make sure you're using the correct import statement:

   ```python
   # ❌ WRONG
   import easy_opencv_wrapper

   # ✅ CORRECT
   from easy_opencv import cv
   ```

### Issue 1a: Using Wrong Import Name

```
ModuleNotFoundError: No module named 'easy_opencv_wrapper'
```

**Cause**: Trying to import using the PyPI package name instead of the module name.

**Solution**: Use the correct import name with underscores:

```python
# ❌ WRONG - Don't use the PyPI package name
import easy_opencv_wrapper

# ✅ CORRECT - Use the module name
from easy_opencv import cv
```

### Issue 2: OpenCV Not Found

```
ImportError: No module named 'cv2'
```

**Solution**: Install OpenCV dependency:

```bash
pip install opencv-python
```

### Issue 3: Version Conflicts

If you encounter dependency conflicts, create a virtual environment:

```bash
# Create virtual environment
python -m venv easy_opencv_env

# Activate it (Windows)
easy_opencv_env\Scripts\activate

# Activate it (macOS/Linux)
source easy_opencv_env/bin/activate

# Install the package
pip install easy-opencv-wrapper
```

## 🔧 Verify Installation

Test your installation with this simple script:

```python
# test_installation.py
try:
    from easy_opencv import cv
    print("✅ Easy OpenCV imported successfully!")
    print(f"📦 Package version: {cv.__version__ if hasattr(cv, '__version__') else 'Available'}")

    # Test basic functionality
    import numpy as np
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    resized = cv.resize_image(test_image, width=50, height=50)
    print("✅ Basic functionality working!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Solution: Run 'pip install easy-opencv-wrapper'")
except Exception as e:
    print(f"❌ Error: {e}")
```

## 📋 System Requirements

- **Python**: 3.7 or higher
- **OpenCV**: 4.5 or higher (installed automatically)
- **NumPy**: 1.19 or higher (installed automatically)
- **Pillow**: 8.0 or higher (installed automatically)

## 🎯 Quick Start Example

Once installed, try this example:

```python
from easy_opencv import cv
import numpy as np

# Create a test image
test_img = np.zeros((200, 200, 3), dtype=np.uint8)
test_img[50:150, 50:150] = [255, 0, 0]  # Red square

# Apply some operations
blurred = cv.apply_gaussian_blur(test_img, kernel_size=15)
edges = cv.apply_edge_detection(blurred, low_threshold=50, high_threshold=150)

print("✅ Easy OpenCV is working correctly!")
```

## 📞 Support

If you encounter any issues:

1. **Check this guide** for common solutions
2. **Verify dependencies** are installed correctly
3. **Create a virtual environment** if needed
4. **Report issues** on the GitHub repository

## 🔄 Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade easy-opencv-wrapper
```

---

**Next Steps**: Check out the [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed examples and the [README.md](README.md) for comprehensive documentation.
