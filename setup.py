from setuptools import setup, find_packages

setup(
    name="queuesync",
    version="1.0.0",
    description="A library for coordinated client-server communication using a queue-based approach.",
    author="Joshua McDonagh",
    author_email="joshua.mcdonagh@manchester.ac.uk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},  # Tells setuptools to look in 'src' for modules
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
