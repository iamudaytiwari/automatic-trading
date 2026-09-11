from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="automatic-trading",
    version="0.1.0",
    author="Uday Tiwari",
    author_email="contact@iamudaytiwari.dev",
    description="Automatic Trading System - Algorithmic trading platform with real-time market analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamudaytiwari/automatic-trading",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "ccxt>=4.0.0",
        "ta-lib>=0.4.28",
        "scikit-learn>=1.3.0",
        "flask>=3.0.0",
        "dash>=2.14.0",
        "plotly>=5.18.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "prophet>=1.1.0",
        ],
        "dashboard": [
            "flask>=3.0.0",
            "dash>=2.14.0",
            "plotly>=5.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ata-cli=src.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
