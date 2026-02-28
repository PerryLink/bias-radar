from setuptools import setup, find_packages

setup(
    name="bias-radar",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "bias-scan=bias_radar.cli:app",
        ],
    },
    python_requires=">=3.8",
)
