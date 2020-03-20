"""
Describes the project and the files that belong to it.
"""

from setuptools import find_packages, setup

setup(
    name='marca',
    version='1.0.0',
    packages=find_packages(), # tells Python what package directories (and the Python files they contain) to include
    include_package_data=True, # include other files, such as the static and templates directories
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

