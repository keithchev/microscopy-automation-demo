#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='microscopy-automation-demo',
    author='Keith Cheveralls',
    description='Dummy microscoy automation script to illustrate testing',
    packages=setuptools.find_packages(),
    python_requires='>3.7',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'run-script = microscopy_automation.cli:main',
        ]
    },
    extras_require={
        "dev": [
            "black==22.3.0",
            "docker==5.0.3",
            "flake8==3.7.9",
            "isort==5.10.1",
            "pre-commit==2.19.0",
            "pytest==5.3.4",
        ],
    },
)
