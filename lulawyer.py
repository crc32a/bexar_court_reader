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
    printf("Usage is %s <lawyer bar number>\nm")
    printf("\n")
    printf("Lookup this lawyers cases\n")

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 1:
        usage(args[0])
        sys.exit()

    bar_num = int(args[1])
    cols = ["sid,full_name,sex,race,birthdate,offense_date,offense_desc,",
            "offense_type,case_desc,bond_status,bond_amount,g_jury_date,"
            "g_jury_status,case_date,judgement_date,disposition_desc,",
            "judgement_desc,original_sentence,sentence,attorney,",
            "attorney_appointed_retained,reduced_offense_desc" ]
    rename = {"attorney_appointed_retained":"aar","offense_type":"ot",
              "bond_status": "bs","bond_amount":"bond","race":"r"}
    s = dbutils.Session()
    cs = s.query(Court).filter(Court.attorney_bar_nbr==bar_num)\
         .order_by(Court.offense_date).all()
    d = DbDisplay(rows=cs,cols=colsplit(cols),rename=rename)
    dstr = d.display()
    printf("%s\n", dstr)
