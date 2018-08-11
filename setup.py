#!/usr/bin/env python

import setuptools


setuptools.setup(

    name="hatsunebot",
    version="1.1",

    license="AGPL-3.0",

    author="Hatsune",
    author_email="xxy1836@gmail.com",

    install_requires=[
        "python-telegram-bot",
        "Pyyaml"
    ],

    packages=[
        "hatsunebot",
    ],

    entry_points={
        "console_scripts": [
            "hatsunebot = hatsunebot.main:main",
        ],
    },

    include_package_data=True,
    zip_safe=False,

    classifiers=[
        "Not on PyPI"
    ],

)
