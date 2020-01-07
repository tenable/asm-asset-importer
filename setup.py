from setuptools import setup, find_packages
import os

long_description = '''
BitDiscovery -> Tenable.io Asset Bridge
For usage documentation, please refer to the github repository at
https://github.com/bitdiscovery/integration-tenable
'''

setup(
    name='tenable-bitdiscovery',
    version='1.0.0',
    description='BitDiscovery to Tenable.io Asset importer',
    author='BitDiscovery',
    long_description=long_description,
    author_email='robert@bitdiscovery.com',
    url='https://github.com/bitdiscovery/integration-tenable',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking',
        'Topic :: Other/Nonlisted Topic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tenable tenable_io bitdiscovery',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pytenable>=1.0.0',
        'Click>=7.0',
        'RESTfly>=1.1.1',
    ],
    entry_points={
        'console_scripts': [
            'tenable-bitdiscovery=tenable_bitdiscovery.cli:cli',
        ],
    },
)
