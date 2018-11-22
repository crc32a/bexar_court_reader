#!/usr/bin/env python

import utils

reload(utils)

printf = utils.printf

file_names = utils.list_csv_files("/home/crc/Downloads")
rows = utils.read_csv_files(file_names)
bad_rows = utils.write_csv("all.csv", rows)
