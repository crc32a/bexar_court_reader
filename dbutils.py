#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime
import sqlalchemy
import sqlalchemy.orm
import utils

Base = declarative_base()


class Court(Base):
    __tablename__ = 'court'
    id = Column(Integer, primary_key=True)
    addr_city = Column(String(24))
    addr_house_nbr = Column(String(12))
    addr_post_direction = Column(String(4))
    addr_pre_direction = Column(String(4))
    addr_state = Column(String(4))
    addr_street = Column(String(24))
    addr_street_suffix = Column(String(6))
    addr_unit = Column(String(8))
    addr_zip_code = Column(Integer)
    addr_zip_plus_4 = Column(Integer)
    alias = Column(String(3))
    attorney = Column(String(32))
    attorney_appointed_retained = Column(String(3))
    attorney_bar_nbr = Column(Integer)
    birthdate = Column(Date)
    bond_amount = Column(Float)
    bond_date = Column(Date)
    bond_status = Column(String(5))
    bondsman_name = Column(String(32))
    case_cause_nbr = Column(String(22))
    case_date = Column(Date)
    case_desc = Column(String(32))
    complaint_date = Column(Date)
    court = Column(String(6))
    court_costs = Column(Float)
    court_type = Column(String(4))
    custody_date = Column(Date)
    disposition_code = Column(Integer)
    disposition_date = Column(Date)
    disposition_desc = Column(String(32))
    filing_agency_description = Column(String(42))
    fine_amount = Column(Float)
    full_name = Column(String(64))
    g_jury_date = Column(Date)
    g_jury_status = Column(String(5))
    house_suf = Column(String(3))
    intake_prosecutor = Column(String(32))
    judgement_code = Column(Integer)
    judgement_date = Column(Date)
    judgement_desc = Column(String(20))
    judicial_nbr = Column(Integer)
    location = Column(String(5))
    offense_code = Column(Integer)
    offense_date = Column(Date)
    offense_desc = Column(String(64))
    offense_type = Column(String(4))
    original_sentence = Column(String(22))
    outtake_prosecutor = Column(String(32))
    post_judicial_date = Column(Date)
    post_judicial_field = Column(String(21))
    probation_prosecutor = Column(String(32))
    race = Column(String(3))
    reduced_offense_code = Column(Integer)
    reduced_offense_desc = Column(String(32))
    reduced_offense_type = Column(String(4))
    revokation_prosecutor = Column(String(32))
    sentence = Column(String(12))
    sentence_desc = Column(String(25))
    sentence_end_date = Column(Date)
    sentence_start_date = Column(Date)
    setting_date = Column(Date)
    setting_type = Column(String(3))
    sex = Column(String(3))
    sid = Column(Integer)

class DbDisplay(object):
    def __init__(self,rows=[],cols=[], rename={}):
        self.rows = rows
        self.cols = cols
        self.rename = rename

    def padstr(self,fl, val):
        vstr = str(val).strip()
        n = len(vstr)
        pad = fl-n
        return " "*pad + vstr

    def get_default_col_names(self):
        rows = self.rows
        if rows is None or len(rows) <=0:
            return []
        return list(rows[1].__class__.__table__.columns.keys())


    def get_col_lens(self):
        cols = self.cols
        rows = self.rows
        rename = self.rename
        if len(cols) <= 0:
            cols = self.get_default_col_names()
        if rows is None or len(rows) <=0:
            return {}
        clm = {}
        for col in cols:
            if col not in clm:
                if col in rename:
                    clm[col] = len(str(rename[col]).strip())
                else:
                    clm[col] = len(str(col).strip())
        for r in rows:
            for c in cols:
                v = getattr(r, c, None)
                if v is None:
                    v = str(None)
                else:
                    v = str(v).strip()
                n = len(v)
                if clm[c] < n:
                    clm[c] = n
        return clm

    def display(self):
        cols = self.cols
        rows = self.rows
        rename = self.rename
        clm = self.get_col_lens()
        if len(cols) ==0:
            cols = self.get_default_col_names()
        out = []
        if len(rows) <= 0:
            return "Empty set\n"
        for col in cols:
            if col in rename:
                out.append(self.padstr(clm[col], rename[col]) + " ")
            else:
                out.append(self.padstr(clm[col], col) + " ")
        out.append("\n")
        for row in rows:
            for col in cols:
                val = getattr(row, col)
                strval = str(val)
                out.append(self.padstr(clm[col], strval) + " ")
            out.append("\n")
        return "".join(out)

def colsplit(arry):
    strjoin = "".join(arry)
    cols = strjoin.split(",")
    return cols


def get_engine(conf_file="./conf.json"):
    conf = utils.load_json(conf_file)
    engine = sqlalchemy.create_engine(conf["engine"], pool_recycle=60)
    return engine

def get_col_names(cls):
    return list(cls.__table__.columns.keys())

def get_coltypes(cls):
    out = {}
    for k in cls.__table__.columns.keys():
        out[k] = cls.__table__.columns[k].type.__class__.__name__
    return out


def row2dbrow(row, mapper):
    court = Court()
    for k in sorted(row.keys()):
        nk = k.replace("-", "_").lower()
        if nk not in mapper:
            continue
        cf = mapper[nk]
        nv = cf(row, k)
        setattr(court, nk, nv)
    return court


def get_col_mappers(cls):
    col_mapper = {}
    coltypes = get_coltypes(cls)
    for (k, v) in coltypes.items():
        if v == "Date":
            col_mapper[k] = utils.get_date
        if v == "Integer":
            col_mapper[k] = utils.get_int
        if v == "Float":
            col_mapper[k] = utils.get_float
        if v == "String":
            col_mapper[k] = utils.get_string
    return col_mapper


def create_tables(engine):
    Base.metadata.create_all(engine)


def attach_engine(engine):
    Session.configure(bind=engine)

def calculate_age(today,born):
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

Session = sqlalchemy.orm.sessionmaker()


