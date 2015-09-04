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

import esdvd
import argparse
import os

class Common:

    def __init__(self):
        self.extraction_directory = None
        self.default_extraction_directory_name = 'data_store'
        self.args = None
        self.parser = argparse.ArgumentParser(description=self.get_description(), version=esdvd.__version__)

    def add_command_line_arguments(self):
        """
        Add command line arguments to the parser
        """
        self.parser.add_argument('-e', '--extract-dir', action='store', dest='extract_dir', type=str,
                                 metavar='path', required=False,
                                 help='Path to store the extracted DVD records in JSON files')

    def get_command_line_arguments(self):
        """
        Fetch the data from the command line parser
        """
        if self.args.extract_dir is not None:
            self.extraction_directory = self.args.extract_dir

    def handle_arguments(self):
        """
        Handles the parsing of the command line arguments passed to the program
        """
        self.add_command_line_arguments()
        self.args = self.parser.parse_args()
        self.get_command_line_arguments()

    def ensure_extraction_directory(self):

        # if the extraction directory was not specified then
        # create
        if self.extraction_directory is None:
            self.extraction_directory = os.path.join(os.getcwdu(), self.default_extraction_directory_name)

        if not os.path.exists(self.extraction_directory):
            os.mkdir(self.extraction_directory)




class ESCommon(Common):
    def __init__(self):
        Common.__init__(self)
