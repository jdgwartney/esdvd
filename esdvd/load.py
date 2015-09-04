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
from elasticsearch import Elasticsearch


class LoadData(ESCommon):

    def __init__(self):
        ESCommon.__init__(self)

    def execute(self):
        self.handle_arguments()
        print('execute')

    def get_description(self):
        return "Loads DVD records in the form of JSON files into a Elasticsearch database"


def main():
    l = LoadData()
    l.execute()

if __name__ == '__main__':
    main()
