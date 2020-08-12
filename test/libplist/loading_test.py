#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
from libplist import loads


def describe_loading():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'fixtures/*.plist')
    files = glob.glob(filename)

    def it_loads_all_fixtures():
        for file in files:
            with open(file, 'r') as content_file:
                content = content_file.read()
                plist = loads(content)
                print(f"Loading file {file} results in {plist}")