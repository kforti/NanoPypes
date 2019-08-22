#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Kevin Fortier",
    author_email='kevin.r.fortier@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Package for rapidly building ONT MinIon sequence analysis core.yml",
    entry_points={
        'console_scripts': [
            'build_cluster = nanopypes.cli:build_cluster',
            'albacore_basecaller = nanopypes.cli:albacore_basecaller',
            'prsync = nanopypes.cli:parallel_rsync',
            'nanopypes-app = nanopypes.cli:start_app',
            'get_config_template = nanopypes.cli:get_config_template',
            'run_pipeline = nanopypes.cli:run_pipeline',
        ],
    },
    install_requires= [
        'Click',
        'dask[distributed]',
        'dask-jobqueue',
        'dask[dataframe]',
        'dask-kubernetes',
        'h5py',
        'ont_fast5_api',
        'bokeh',
        'conda',
        'cytoolz',
        'pexpect',
        'spython',
        'prefect',
        'pandas'
    ],
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nanopypes',
    name='nanopypes',
    packages=find_packages(include=['nanopypes']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kforti/pai-nanopypes',
    version='0.2.0',
    zip_safe=False,
)
