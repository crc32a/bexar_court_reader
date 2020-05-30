#!/usr/bin/env python

from dbutils import Court, DbDisplay, colsplit
import utils
import dbutils
import sys
import os
import gc

printf = utils.printf
engine = dbutils.get_engine()
dbutils.attach_engine(engine)
printf("pid=%s\n", os.getpid())

def usage(prog):
    printf("usage is %s <sid>\n", prog)
    printf("\n")
    printf("Lookup the current address off the above inmates bases\n")
    printf("On what they entered during booking\n")

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        usage(args[0])
        sys.exit()
    sid = int(args[1])
    cols = ["sid,full_name,offense_desc,offense_date,addr_house_nbr,",
            "addr_unit,addr_street,addr_street_suffix,addr_city,addr_state,",
            "addr_zip_code"]
    s = dbutils.Session()
    cs = s.query(Court).filter(Court.sid==sid).order_by(Court.offense_date).\
         all()
    d = DbDisplay(rows=cs,cols=colsplit(cols))
    dstr = d.display()
    printf("%s\n", dstr)
