#!/usr/bin/env python
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
        self.args = None
        self.data_directory = None
        self.extraction_directory = None
        self.default_extraction_directory_name= 'data_store'
        self.parser = None
        data_dir = os.path.dirname(esdvd.__file__)
        self.data_file_name = 'dvd_csv.txt.gz'
        self.data_path = os.path.join(data_dir, self.data_file_name)
        self.parser = argparse.ArgumentParser(description='Extracts and converts DVD records to JSON files',
                                              version=esdvd.__version__)

    def add_command_line_arguments(self):
        self.parser.add_argument('-e','--extract-dir', action='store', dest='extract_dir', type=str,
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

    def initialize(self):
        """
        Perform any initial configuration
        """

        # if the extraction directory was not specified then
        #
        if self.extraction_directory is None:
            self.extraction_directory = os.path.join(os.getcwdu(), self.default_extraction_directory_name)

        if not os.path.exists(self.extraction_directory):
            os.mkdir(self.extraction_directory)

    def execute(self):
        """
        Execute the program
        """
        self.handle_arguments()
        self.initialize()
        self.load(self.data_path)

    def load(self, file_name):
        """
        Load the zip file with our DVD and process 
        """
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
