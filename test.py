#!/usr/bin/env python

import utils
import dbutils
import os
import gc
reload(utils)
reload(dbutils)

os.getpid()
printf = utils.printf


file_names = utils.list_csv_files("~/csv")
rows = utils.read_csv_files(file_names)
bad_rows = utils.write_csv("all.csv", rows)

rows = utils.read_csv_files(["all.csv"], display_interval=100000)
utils.display_row(rows[0])
engine = dbutils.get_engine()
dbutils.attach_engine(engine)
mapper = dbutils.get_col_mappers(dbutils.Court)

courts = []
n = len(rows)
for i in xrange(0, n):
    nr = dbutils.row2dbrow(rows[i], mapper)
    if i % 100000 == 0:
        percent = 100.0*float(i)/float(n)
        printf("%i of %i %f %% complete\n", i, n, percent)
    courts.append(nr)


s = dbutils.Session()

i = 0
n = len(courts)
while i < n:
    rows = utils.pop_rows(courts, 100000)
    i += len(rows)
    s.add_all(rows)
    s.commit()
    percent = 100.0*(float(i)/float(n))
    printf("%i of %i rows %f %% complete\n", i, n , percent)
    


