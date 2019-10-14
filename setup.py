#!/usr/bin/env python3
"""Install the :mod:`artiq-dynaconf-loader` package.

Loads "datasets" pulled from ARTIQ into the :mod:`dynaconf` namespace,
specifically :attr:`dynaconf.settings`.
"""
import pathlib

import setuptools

if __name__ == "__main__":
    base_requirements = pathlib.Path("requirements.txt").open("r").read().splitlines()

    extra_requirements = {"doc": ["sphinx"], "dev": ["pre-commit"]}

    setuptools.setup(
        name="artiq-dynaconf-loader",
        version="0.1",
        packages=setuptools.find_packages(),
        author="Drew Risinger",
        author_email="drisinger@gmail.com",
        description="Dynaconf loader to pull ARTIQ datasets into settings values.",
        install_requires=base_requirements,
        extras_require=extra_requirements,
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        package_data={
            # Include (restructured text, markdown) documentation files from
            # any directory
            "": ["*.rst", "*.md"],
            # Include text files from the eggs package:
            "eggs": ["*.txt"],
        },
        long_description=open("README.md", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        license="GNU GPL v3",
        url="https://github.com/drewrisinger/artiq-dynaconf-loader",
    )
