#!/usr/bin/env python

import utils
import dbutils
import gc
reload(utils)
reload(dbutils)

printf = utils.printf


file_names = utils.list_csv_files("~/csv")
rows = utils.read_csv_files(file_names)
bad_rows = utils.write_csv("all.csv", rows)



rows = utils.read_csv_files(["all.csv"], display_interval=100000)

utils.display_row(row[0])




engine = dbutils.get_engine()
dbutils.attach_engine(engine)



dbutils.create_tables(engine)

