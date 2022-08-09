from setuptools import setup
from flake8_tkinter import __version__


with open("README.md", "r") as file:
    long_description = file.read()


flake8_entry_point = "TK = flake8_tkinter:Plugin"


setup(
    name="flake8_tkinter",
    version=__version__,
    description="Flake8 plugin to detect (too) common mistakes and bad practices in Tkinter projects",
    author="rdbende",
    author_email="rdbende@gmail.com",
    url="https://github.com/rdbende/flake8-tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=["flake8>=3.7"],
    packages=["flake8_tkinter", "flake8_tkinter/checkers"],
    entry_points={"flake8.extension": ["TK = flake8_tkinter:Plugin"]},
    license="MIT license",
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
