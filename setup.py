#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="push-to-acs",
    version="0.0.1",
    author="Alexander Mahabir",
    author_email="alex.mahabir@gmail.com",
    description="This is a small utility for pushing documents from a filesystem into ACS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex4u2nv/push-to-acs.git",
    scripts=['bin/push-to-acs'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['argparse', 'requests', 'watchdog', 'daemons']
)
