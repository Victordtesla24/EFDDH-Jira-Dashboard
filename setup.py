from setuptools import setup, find_packages

setup(
    name="efddh-dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.13.0",
    ],
     python_requires=">=3.9",
)