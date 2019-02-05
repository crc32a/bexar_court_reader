#!/usr/bin/env python


import utils

printf = utils.printf

rows = utils.read_csv_urls()
bad_rows = utils.write_csv("all.csv", rows)
printf("unable to convert %d rows\n", len(bad_rows))

