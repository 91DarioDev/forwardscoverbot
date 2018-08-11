#!/usr/bin/env python

import setuptools


setuptools.setup(

    name="hatsunebot",
    version="0.2",

    license="AGPL-3.0",

    author="Hatsune",
    author_email="xxy1836@gmail.com",

    install_requires=[
        "python-telegram-bot",
        "Pyyaml",
        "PyMySQL"
    ],

    packages=[
        "hatsune",
    ],

    entry_points={
        "console_scripts": [
            "hatsune = hatsunebot.__main__:main",
        ],
    },

    include_package_data=True,
    zip_safe=False,

    classifiers=[
        "Not on PyPI"
    ],

)
