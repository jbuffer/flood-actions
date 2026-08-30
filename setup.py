"""Setup configuration for flood-actions package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flood-actions",
    version="0.1.0",
    author="Jennifer Bufton",
    description="GitHub Actions to schedule daily flood data collection from Environment Agency API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jbuffer/flood-actions",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.23.1",
        "pandas>=1.4.3",
        "requests>=2.28.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.1.0",
            "pytest-cov>=3.0.0",
            "flake8>=4.0.0",
            "black>=22.3.0",
            "isort>=5.10.0",
            "mypy>=0.910",
        ]
    },
)
