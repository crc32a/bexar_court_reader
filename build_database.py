#!/usr/bin/env python

import time
import utils
import dbutils
import os
import gc


printf = utils.printf

engine = dbutils.get_engine()
dbutils.attach_engine(engine)
printf("pid=%i\n", os.getpid())
try:
    dbutils.create_tables(engine)
    printf("court table built\n")
except:
    printf("%s ccoulden't build table\n", utils.excuse())

courts = []
i = 0
mapper = dbutils.get_col_mappers(dbutils.Court)
nrows = 0
total_rows = 0
time_start = time.time()
for chunk in utils.read_csv_file_lines("all.csv", chunk_size=10000):
    db_rows = []
    for row in chunk:
        db_rows.append(dbutils.row2dbrow(row, mapper))
    n = len(db_rows)
    total_rows += n
    s = dbutils.Session()
    s.add_all(db_rows)
    s.commit()
    s.close()
    time_stop = time.time()
    printf("Writing %d rows to data base total rows so far is %d ",
           n, total_rows)
    printf("in %f seconds\n", time_stop - time_start)
    time_start = time_stop
    gc.collect()

