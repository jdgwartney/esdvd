#!/usr/bin/env python
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
import csv
import argparse
import json
import uuid
import gzip
import os
import esdvd
from esdvd import Common


class ExtractData(Common):

    def __init__(self):
        Common.__init__(self)

        self.data_directory = None
        data_dir = os.path.dirname(esdvd.__file__)
        self.data_file_name = 'dvd_csv.txt.gz'
        self.data_path = os.path.join(data_dir, self.data_file_name)

    def get_description(self):
        return 'Extracts and converts DVD records to JSON files'

    def add_command_line_arguments(self):
        Common.add_command_line_arguments(self)

    def get_command_line_arguments(self):
        Common.get_command_line_arguments(self)

    def execute(self):
        """
        Execute the program
        """
        self.handle_arguments()
        self.load(self.data_path)

    def load(self, file_name):
        """
        Load the zip file with our DVD and process 
        """

        # Call our method to make sure we have a path to an output directory
        # and mask sure it exists, creating if if necessary
        self.ensure_extraction_directory()
        with gzip.open(file_name, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.process_row(row)

    def process_row(self, row):
        """
        Handle the processing of the individual row of data
        """
        try:
            self.write_row(json.dumps(row))
        except UnicodeDecodeError:
            pass

    def write_row(self, row):
        """
        Write data to a unique path
        """
        unique_file_name = uuid.uuid4()
        path = os.path.join(self.extraction_directory, str(unique_file_name))
        self.write_data(path, row)

    def write_data(self, path, data):
        """
        Writes data to provide file name
        """
        with open(path, 'wt') as f:
            f.write(data)


def main():
    ed = ExtractData()
    ed.execute()


if __name__ == "__main__":
    main()
