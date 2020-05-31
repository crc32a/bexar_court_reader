#!/usr/bin/env python


from dbutils import Court, DbDisplay, colsplit, calculate_age
import datetime
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
    printf("Usage is %s <name1..> <..nameN>\n", prog)
    printf("\n");
    printf("Print off sids and names of sids matching the names\n")
    printf("listed on the command line\n")

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        usage(args[0])
        sys.exit()
    today = datetime.date.today()
    names = args[1:]
    cols = "sid,full_name,race,birthdate,age"
    s = dbutils.Session()
    q = s.query(Court)
    for name in names:
        nstr = "%%%s%%" %(name)
        q = q.filter(Court.full_name.ilike(nstr))
    q = q.order_by(Court.birthdate,Court.sid)
    cs = q.all()
    n = len(cs)
    printf("Fetched %d mataches\n", n)
    now = datetime.datetime.now()
    for c in cs:
        if c.birthdate is None:
            setattr(c,"age",None)
        else:
            birthdate = c.birthdate
            age = calculate_age(today,birthdate)
            setattr(c, "age", age)
    d = DbDisplay(rows=cs, cols=colsplit(cols))
    printf("cols = %s\n", cols)
    out = d.display()
    printf("%s\n",out)