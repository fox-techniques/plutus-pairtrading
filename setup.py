from setuptools import setup, find_packages

setup(
    name="plutus-pairtrading",
    version="1.0.0",
    author="FOX Techniques",
    author_email="contact+plutus@fox-techniques.com",
    description="PLUTUS is a Python-based toolkit for performing pair-trading analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fox-techniques/plutus-pairtrading",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.2.0",
        "pandas>=2.2.3",
        "requests>=2.32.3",
        "plotly>=5.24.1",
        "matplotlib>=3.9.3",
        "yfinance>=0.2.50",
        "arch>=7.2.0",
        "seaborn>=0.13.2",
    ],
    extras_require={"dev": ["pytest>=8.3.4"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
