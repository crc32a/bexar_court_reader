#!/usr/bin/env python


import traceback
import cPickle
import datetime
import json
import sys
import csv
import os
import re

dtstr_re = re.compile("([0-9]+)/([0-9]+)/([0-9]+)")

dtint_re = re.compile("([0-9]{4})([0-9]{2})([0-9]{2})")



def printf(format,*args): sys.stdout.write(format%args)


def fprintf(fp,format,*args): fp.write(format%args)


def read_csv(file_name):
    file_path = os.path.expandusr


def load_json(pathIn):
    return json.loads(open(os.path.expanduser(pathIn), "r").read())


def save_json(pathOut, obj):
    fp = open(os.path.expanduser(pathOut),"w")
    jsonStr = json.dumps(obj, indent=2)
    fp.write(jsonStr)
    fp.close()


def read_csv(file_name, display_interval=None):
    i = 0
    csv_rows = []
    fp = open(os.path.expanduser(file_name), "r")
    data = fp.read().replace("\x00","").splitlines()
    reader = csv.DictReader(data)
    for r in reader:
        if display_interval and i % display_interval == 0:
            printf("%i rows read\n", i)
        csv_rows.append(r)
        i += 1
    fp.close()
    return csv_rows

def list_csv_files(path):
    file_names = []
    for file_name in os.listdir(os.path.expanduser(path)):
        ext = os.path.splitext(file_name)[1]
        if ext.lower() == ".csv":
            file_names.append(os.path.join(path, file_name))
    return file_names

def read_csv_files(file_names, display_interval=None):
    n = len(file_names)
    i = 0
    all_rows = []
    for file_name in file_names:
        printf("reading %i of %i file name %s: ", i, n, file_name)
        sys.stdout.flush()
        rows = read_csv(file_name, display_interval=display_interval)
        all_rows.extend(rows)
        printf(" %i rows read\n", len(rows))
        i += 1
    return all_rows

def excuse():
    except_message = traceback.format_exc()
    stack_message  = traceback.format_stack()
    return except_message + " " + str(stack_message)

def write_csv(file_name, rows):
    fields = rows[0].keys()
    fp = open(os.path.expanduser(file_name),"w")
    writer = csv.DictWriter(fp, fieldnames=fields)
    writer.writeheader()
    i = 0
    n = len(rows)
    bad_rows = []
    for i in xrange(0,n):
        try:
            writer.writerow(rows[i])
        except:
            printf("Bad row %i\n", i)
            bad_rows.append(rows[i])
        if i % 10000 == 0:
            printf("%0.2f%% percent complete\n", 100.0*float(i)/float(n))
        i += 1
    fp.close()
    return bad_rows

def display_row(row):
    for key in sorted(row.keys()):
        printf("%s: %s\n", key, row[key])

def test_re(val, exp):
    p = re.compile(exp)
    m = p.match(val)
    if m:
        return m.groups()
    return False

def getcollens(rows):
    lens = {}
    keys = rows[0].keys()
    for k in keys:
        lens[k] = 0
    for r in rows:
        for k in r.keys():
            try:
                l = len(r[k])
                if l > lens[k]:
                    lens[k] = l
            except:
                continue
    return lens


def get_string(row, k):
    if k not in row:
        return None
    return row[k]


def get_int(row, k):
    if k not in row:
        return None
    try:
        return int(row[k])
    except:
        return None


def get_date(row, k):
    if k not in row:
        return None
    try:
        return dtstr2date(row[k])
    except:
        return None


def make_cols(rows, lens, keys):
    out = []
    for k in sorted(keys):
        new_key = k.replace("-", "_").lower()
        out.append("    %s = Column(String(%s))\n"%(new_key, lens[k]+1))
    return out


def get_float(row, k):
    if k not in row:
        return None
    try:
        return float(row[k])
    except:
        return None


def pop_rows(rows, n):
    l = len(rows)
    out = []
    if l < n:
        n = l
    for i in xrange(0, n):
        out.append(rows.pop())
    return out


def dtstr2date(dtstr):
    m = dtstr_re(dtstr)
    if m:
        month = int(m.group(0))
        day = int(m.group(1))
        year = int(m.group(2))
        return datetime.date(year, month, day)
    m = dtint_re(dtstr)
    if m:
        year = int(m.group(0))
        month = int(m.group(1))
        day = int(m.group(2))
        return datetime.date(year, month, day)
    return None


