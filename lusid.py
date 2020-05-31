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

def sidlookup(sid):
    s = dbutils.Session()
    rows = s.query(Court).filter(Court.sid==sid).\
        order_by(Court.offense_date).all()
    return rows

def usage(prog):
    printf("usage is %s <sid number>\n", prog)
    printf("\n")
    printf("Fetch sid information for the given sid ID\n")

if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        usage(args[0])
        sys.exit()
    sid = int(args[1])
    rows = sidlookup(sid)
    cols = ["sid,full_name,sex,race,birthdate,offense_date,offense_desc,",
            "offense_type,case_desc,bond_status,bond_amount,case_date,",
            "judgement_date,disposition_desc,judgement_desc,",
            "original_sentence,sentence,attorney,",
            "attorney_appointed_retained,reduced_offense_desc" ]
    rename = {"attorney_appointed_retained":"aar","offense_type":"ot",
              "bond_status": "bs","bond_amount":"bond","race":"r"}
    d = DbDisplay(rows=rows,cols=colsplit(cols),rename=rename)
    out = d.display()
    sys.stdout.write(out)
