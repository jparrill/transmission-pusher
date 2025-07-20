#!/usr/bin/env python3
"""
Setup script for Transmission Pusher
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="transmission-pusher",
    version="1.0.0",
    author="Juan Manuel Parrilla",
    author_email="padajuan@gmail.com",
    description="A Python client for Transmission BitTorrent client",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jparrill/transmission-pusher",
    project_urls={
        "Bug Reports": "https://github.com/jparrill/transmission-pusher/issues",
        "Source": "https://github.com/jparrill/transmission-pusher",
        "Documentation": "https://github.com/jparrill/transmission-pusher#readme",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=6.2.0",
            "pytest-mock>=3.10.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "transmission-pusher=transmission_pusher.transmission_client:main",
            "transmission-diagnose=transmission_pusher.diagnose_connection:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="transmission, bittorrent, client, api, rpc",
)