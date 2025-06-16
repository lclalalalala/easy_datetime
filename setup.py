from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name="easy-datetime",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dateutil>=2.8.2",
        "pytz>=2021.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    author="Lucy",
    author_email="lucy@example.com",
    description="A comprehensive datetime utility package for easy datetime manipulation, conversion, and formatting",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/lclalalalala/easy_datetime",
    project_urls={
        "Bug Tracker": "https://github.com/lclalalalala/easy_datetime/issues",
        "Documentation": "https://github.com/lclalalalala/easy_datetime#readme",
        "Source Code": "https://github.com/lclalalalala/easy_datetime",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="datetime timestamp timezone date time parsing formatting",
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)
