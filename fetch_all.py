#!/usr/bin/env python


import utils
import os
import csv
import sys
import gc

printf = utils.printf
printf("this pid is %s\n", os.getpid())
urls = utils.get_csv_urls()
i = 0
nurls = len(urls)
fp = open("all.csv", "w", 64*1024)
writer = None
nbadrows = 0
ri = 0
for url in urls:
    printf("reading %i of %i file name %s:\n", i, nurls, url)
    for row in utils.read_csv_url(url):
        if not writer:
            fields = row.keys()
            printf("fields = %s\n", fields)
            writer = csv.DictWriter(fp, fieldnames=fields)
            writer.writeheader()
        try:
            writer.writerow(row)
            ri += 1
        except KeyboardInterrupt:
            raise
        except:
            printf("Bad row %i\n", ri)
            nbadrows += 1
    i += 1
fp.close()
printf("unable to convert %d rows\n", nbadrows)

