from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easy-opencv-wrapper",
    version="1.0.1",
    author="Aksh Agrawal",
    author_email="akshagr10@gmail.com",
    description="A simplified and intuitive OpenCV wrapper that reduces code complexity by 50-70% for common computer vision tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aksh-agrawal/easy-opencv-wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/aksh-agrawal/easy-opencv-wrapper/issues",
        "Documentation": "https://github.com/aksh-agrawal/easy-opencv-wrapper#readme",
        "Repository": "https://github.com/aksh-agrawal/easy-opencv-wrapper.git",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education", 
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Topic :: Multimedia :: Video :: Capture",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
        ],
    },
    keywords="opencv computer-vision image-processing cv wrapper simplified easy",
    include_package_data=True,
)
