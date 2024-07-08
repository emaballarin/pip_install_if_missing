#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

DESCRIPTION = "Easily install Python packages if they are missing. Thought for Colab-like disposable environments."

setup(
    name="pip_install_if_missing",
    version="0.0.5",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    keywords=["pip", "install", "missing", "dependency"],
    author="Emanuele Ballarin",
    author_email="emanuele@ballarin.cc",
    url="https://github.com/emaballarin/pip_install_if_missing",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    include_package_data=False,
    zip_safe=True,
    install_requires=[],
    packages=["piim"],
)
