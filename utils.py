#!/usr/bin/env python

import cPickle
import json
import sys
import csv
import os


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

def read_csv(file_name):
    csv_rows = []
    fp = open(os.path.expanduser(file_name), "r")
    data = fp.read().replace("\x00","").splitlines()
    reader = csv.DictReader(data)
    for r in reader:
        csv_rows.append(r)
    fp.close()
    return csv_rows

def list_csv_files(path):
    file_names = []
    for file_name in os.listdir(path):
        ext = os.path.splitext(file_name)[1]
        if ext.lower() == ".csv":
            file_names.append(os.path.join(path, file_name))
    return file_names

def read_csv_files(file_names):
    n = len(file_names)
    i = 0
    all_rows = []
    for file_name in file_names:
        printf("reading %i of %i file name %s: ", i, n, file_name)
        sys.stdout.flush()
        rows = read_csv(file_name)
        all_rows.extend(rows)
        printf(" %i rows read\n", len(rows))
        i += 1
    return all_rows

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

