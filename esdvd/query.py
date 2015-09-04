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

from esdvd import ESCommon
from lru import lru_cache_function
import json
import random
import time
import os


class QueryData(ESCommon):

    def __init__(self):
        ESCommon.__init__(self)

    @staticmethod
    @lru_cache_function(max_size=1024*8, expiration=60)
    def get_id(q, rindex):
        path = q.get_file_path(rindex)
        record_id = q.get_id_from_file(path)
        return record_id

    def get_description(self):
        return "Queries Elasticsearch for random DVD documents"

    def add_command_line_arguments(self):
        ESCommon.add_command_line_arguments(self)

    def get_command_line_arguments(self):
        ESCommon.get_command_line_arguments(self)

    def get_file_path(self, findex):
        """
        Returns the full path to file using index into list of a directory
        :return:
        """
        file_name = self.files[findex]
        file_path = os.path.join(self.extraction_directory,file_name)
        return file_path

    def get_id_from_file(self, path):
        contents = self.get_file_contents(path)
        doc = json.loads(contents)
        record_id = doc[self.id_field_name]
        return record_id

    def query_record(self, record_id):
        """
        Look up record in elastic search
        :param record_id:
        :return:
        """
        res = self.es.get(index=self.index, doc_type=self.doc_type, id=record_id)
        print(res['_source'])

    def increment_count(self):
        self.count += 1

    def done(self):
        result = None
        if self.limit is not None and self.count > self.limit:
            result = True
        else:
            result = False
        return result

    def query_database(self):
        self.files = self.get_files()
        print("number of files: {0}".format(len(self.files)))
        while not self.done():
            rindex = random.randrange(0, len(self.files) - 1)
            record_id = QueryData.get_id(self, rindex)
            print("+++++")
            self.query_record(record_id)
            print("-----")
            time.sleep(self.sleep)
            self.increment_count()

    def execute(self):
        self.handle_arguments()
        self.set_extraction_directory()
        self.query_database()


def main():
    l = QueryData()
    l.execute()

if __name__ == '__main__':
    main()
