#!/usr/bin/env python


import traceback
import tempfile
import requests
import datetime
import io
import pycurl
import json
import sys
import csv
import os
import re

felony_url = "https://www.bexar.org/2988/Online-District-Clerk-Criminal-Records"
misdemeaner_url = "https://www.bexar.org/2923/Misdemeanor-Records"

dtstr_re = re.compile("([0-9]+)/([0-9]+)/([0-9]+)")

dtint_re = re.compile("([0-9]{4})([0-9]{2})([0-9]{2})")

http_re = re.compile(r"(http://.*\.csv+)")

def printf(format,*args): sys.stdout.write(format%args)

def fprintf(fp,format,*args): fp.write(format%args)

def read_url_rows(url):
    fp = tempfile.TemporaryFile('w')
    r = requests.get(url)
    data = r.text.replace("\x00","").splitlines()
    fp.write(data)

def clean_ascii(text):
    return text

def curl_url(url):
    buffer = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CONNECTTIMEOUT, 15)
    c.perform()
    c.close()
    body = buffer.getvalue()    
    return clean_ascii(body)
        
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
    data = fp.read().replace("\x00", "").splitlines()
    fp.close()
    lfp = open("log.txt", "a")
    fprintf(lfp, "reading rows: ")
    reader = csv.DictReader(data)
    for r in reader:
        if display_interval and i % display_interval == 0:
            printf("%i rows read\n", i)
        csv_rows.append(r)
        i += 1
        fprintf(lfp, "%d, ", i)
        lfp.flush()
    lfp.close()
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
        printf("file %s found\n", file_name)
    for file_name in file_names:
        printf("reading %i of %i file name %s:\n", i, n, file_name)
        sys.stdout.flush()
        rows = read_csv(file_name, display_interval=display_interval)
        all_rows.extend(rows)
        printf(" %i rows read\n", len(rows))
        i += 1
    return all_rows

def get_csv_urls():
    csv_urls = []
    r = requests.get(felony_url)
    for csv_url in http_re.findall(r.text):
        csv_urls.append(csv_url)
    r = requests.get(misdemeaner_url)
    for csv_url in http_re.findall(r.text):
        csv_urls.append(csv_url)
    return csv_urls

def read_csv_url(file_url, display_interval=None):
    i = 0
    csv_rows = []
    while True:
        try:
            byteString = curl_url(file_url)
            uniStr = byteString.decode("utf-8", "ignore")
            replacedStr = uniStr.replace("\0", "")
            lines = replacedStr.splitlines()
            reader = csv.DictReader(lines)
            break
        except:
            printf("%s: retrying %s\n", excuse(),  file_url)
    for r in reader:
        if display_interval and i % display_interval == 0:
            printf("%i rows read\n", i)
        csv_rows.append(r)
        i += 1
    return csv_rows

def read_csv_urls(display_interval=None):
    urls = get_csv_urls()
    n = len(urls)
    i = 0
    all_rows = []
    for url in urls:
        printf("url %s found\n", url)

    for url in urls:
        printf("reading %i of %i file name %s: ", i, n, url)
        sys.stdout.flush()
        rows = read_csv_url(url, display_interval=display_interval)
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
    for i in range(0,n):
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
    for i in range(0, n):
        out.append(rows.pop())
    return out


def dtstr2date(dtstr):
    m = dtstr_re.match(dtstr)
    if m:
        month = int(m.group(1))
        day = int(m.group(2))
        year = int(m.group(3))
        return datetime.date(year, month, day)
    m = dtint_re.match(dtstr)
    if m:
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))
        return datetime.date(year, month, day)
    return None


