from setuptools import setup, find_packages

setup(
    name="conjure-python",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ipython",
        "ipywidgets",
    ],
    python_requires='>=3.7',
)