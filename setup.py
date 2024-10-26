from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="queuesync",
    version="1.0.1",
    description="A library for coordinated client-server communication using a queue-based approach.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Set this to "text/markdown" for Markdown or "text/x-rst" for reStructuredText
    author="Joshua McDonagh",
    author_email="joshua.mcdonagh@manchester.ac.uk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
