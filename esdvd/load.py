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
from esdvd import ESCommon
import json


class LoadData(ESCommon):

    def __init__(self):
        ESCommon.__init__(self)
        self.files = None

    def process_one_file(self, path):
        data = self.get_file_contents(path)
        doc = json.loads(data)
        self.send_data(doc)

    def send_data(self, doc):
        res = self.es.index(index=self.index, doc_type=self.doc_type, id=doc[self.id_field_name], body=doc)
        print(res)
        #print(res['_source'])

    def execute(self):
        self.handle_arguments()
        self.set_extraction_directory()
        self.process_files()

    def get_description(self):
        return "Loads DVD records in the form of JSON files into a Elasticsearch database"


def main():
    l = LoadData()
    l.execute()

if __name__ == '__main__':
    main()
