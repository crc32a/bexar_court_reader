#!/usr/bin/env python


import utils
import os

printf = utils.printf
printf("this pid is %s\n", os.getpid())
rows = utils.read_csv_urls()
bad_rows = utils.write_csv("all.csv", rows)
printf("unable to convert %d rows\n", len(bad_rows))

