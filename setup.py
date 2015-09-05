# -*- coding: UTF-8 -*-

# Copyright 2015 David Gwartney
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

ld = """Tooling to load DVD database into Elasticsearch

DVD database data is provided by:

Home Theater Info <http://www.hometheater.info

and

Michael's Mayhem <http://dvdlist.kazart.com>
"""

setup(
    name='esdvd',
    version='0.1.0',
    author='David Gwartney',
    author_email='david.gwartney@gmail.com',
    url='https://github.com/jdgwartney/esdvd',
    description='Tools to load a DVD Database into Elasticsearch',
    long_description=ld,
    install_requires=['elasticsearch >= 1.6.0',
                      'py-lru-cache >= 0.1.4',
                     ],
    packages=['esdvd'],
    package_data={
        '': ['README.md'],
        'esdvd': ['dvd_csv.txt.gz','copyright',],
    },
    entry_points={
        'console_scripts': [
            'esdvd-delete = esdvd.delete:main',
            'esdvd-extract = esdvd.extract:main',
            'esdvd-load = esdvd.load:main',
            'esdvd-query = esdvd.query:main',
            'esdvd-update = esdvd.update:main',
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Utilities",
    ],
    license='Apache 2.0',
    #    test_suite = "",
)
