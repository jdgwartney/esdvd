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

from __future__ import print_function

from elasticsearch import Elasticsearch
import esdvd
import argparse
import os
import sys

class Common:

    def __init__(self):
        self.quiet = False
        self.extraction_directory = None
        self.default_extraction_directory_name = 'data_store'
        self.args = None
        self.parser = argparse.ArgumentParser(description=self.get_description(), version=esdvd.__version__)

    def extract_directory_required(self):
        """
        Indicate if the command requires that the extraction directory exists
        and has data contained within it
        """
        return False

    def add_command_line_arguments(self):
        """
        Add command line arguments to the parser
        """
        self.parser.add_argument('-e', '--extract-dir', action='store', dest='extract_dir', type=str,
                                 metavar='path', required=self.extract_directory_required(),
                                 help='Path to store the extracted DVD records in JSON files')
        self.parser.add_argument('-q', '--quit', action='store_true', dest='quiet', help='Silent mode')


    def get_command_line_arguments(self):
        """
        Fetch the data from the command line parser
        """
        if self.args.extract_dir is not None:
            self.extraction_directory = self.args.extract_dir

        if self.args.quiet is not None:
            self.quiet = self.args.quiet

    def handle_arguments(self):
        """
        Handles the parsing of the command line arguments passed to the program
        """
        self.add_command_line_arguments()
        self.args = self.parser.parse_args()
        self.get_command_line_arguments()

    def set_extraction_directory(self):
        """
        If the extraction directory was not specified on the commandline then form a default location
        which is the current location with a default directory name
        """
        if self.extraction_directory is None:
            self.extraction_directory = os.path.join(os.getcwdu(), self.default_extraction_directory_name)

    def ensure_extraction_directory(self):
        """
        1) Form the extraction directory
        2) Check for the existences of the directory, and create if not present
        """
        self.set_extraction_directory()
        if not os.path.exists(self.extraction_directory):
            os.mkdir(self.extraction_directory)




class ESCommon(Common):
    def __init__(self):
        Common.__init__(self)
        self.es = Elasticsearch()
        self.index = 'dvd-database'
        self.doc_type = 'dvd-record'
        self.id_field_name = 'ID'
        self.files = None
        self.count = 0
        self.limit = None
        self.sleep = 5

    def add_command_line_arguments(self):
        """
        Add command line arguments to the parser
        """
        Common.add_command_line_arguments(self)
        self.parser.add_argument('-d', '--doc-type', action='store', dest='doc_type', type=str,
                                 metavar='doc_type_name', required=False,
                                 help='Index name')
        self.parser.add_argument('-i', '--index', action='store', dest='index', type=str,
                                 metavar='index_name', required=False,
                                 help='Index name')
        self.parser.add_argument('-l', '--limit', action='store', dest='limit', type=int,
                                 metavar='value', required=False,
                                 help='Limit on the number of records')
        self.parser.add_argument('-s', '--sleep', action='store', dest='sleep', type=int,
                                 metavar='value', required=False,
                                 help='Sleep value')

    def get_command_line_arguments(self):
        """
        Fetch the data from the command line parser
        """
        Common.get_command_line_arguments(self)

        if self.args.extract_dir is not None:
            self.extraction_directory = self.args.extract_dir

        if self.args.index is not None:
            self.index = self.args.index

        if self.args.doc_type is not None:
            self.doc_type = self.args.doc_type

        if self.args.limit is not None:
            self.limit = self.args.limit

        if self.args.sleep is not None:
            self.sleep = self.args.sleep

    def get_file_contents(self, path):
        with open(path, 'rb') as f:
            lines = f.readlines()
        return lines[0]

    def process_one_file(self, path):
        print(path)

    def get_files(self):
        files = os.listdir(self.extraction_directory)
        return files

    def process_files(self):
        """
        Get a list of the files from the extraction directory
        """
        for file_name in self.get_files():
            path = os.path.join(self.extraction_directory, file_name)
            try:
                self.process_one_file(path)
            except Exception as e:
                print("Error processing {0} - {1}".format(path, e.message), file=sys.stderr)
                continue

    def get_file_contents(self, path):
        with open(path, 'rb') as f:
            lines = f.readlines()
        return lines[0]

    def process_one_file(self, path):
        print(path)

    def get_files(self):
        files = os.listdir(self.extraction_directory)
        return files

    def process_files(self):
        """
        Get a list of the files from the extraction directory
        """
        for file_name in self.get_files():
            path = os.path.join(self.extraction_directory, file_name)
            try:
                self.process_one_file(path)
            except Exception as e:
                print("Error processing {0} - {1}".format(path, e.message), file=sys.stderr)
                continue

