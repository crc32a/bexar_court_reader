#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import sqlalchemy.orm
import utils

Base = declarative_base()


class Court(Base):
    __tablename__ = 'court'
    id = Column(Integer, primary_key=True)
    addr_city = Column(String(23))
    addr_house_nbr = Column(String(11))
    addr_post_direction = Column(String(3))
    addr_pre_direction = Column(String(3))
    addr_state = Column(String(3))
    addr_street = Column(String(23))
    addr_street_suffix = Column(String(5))
    addr_unit = Column(String(7))
    addr_zip_code = Column(Integer)
    addr_zip_plus_4 = Column(Integer)
    alias = Column(String(2))
    attorney = Column(String(31))
    attorney_appointed_retained = Column(String(2))
    attorney_bar_nbr = Column(Integer)
    birthdate = Column(Date)
    bond_amount = Column(Float)
    bond_date = Column(Date)
    bond_status = Column(String(4))
    bondsman_name = Column(String(31))
    case_cause_nbr = Column(String(21))
    case_date = Column(Date)
    case_desc = Column(String(19))
    complaint_date = Column(Date)
    court = Column(String(5))
    court_costs = Column(Float)
    court_type = Column(String(3))
    custody_date = Column(Date)
    disposition_code = Column(Integer)
    disposition_date = Column(Date)
    disposition_desc = Column(String(19))
    filing_agency_description = Column(String(41))
    fine_amount = Column(Float)
    full_name = Column(String(41))
    g_jury_date = Column(Date)
    g_jury_status = Column(String(4))
    house_suf = Column(String(2))
    intake_prosecutor = Column(String(31))
    judgement_code = Column(Integer)
    judgement_date = Column(Date)
    judgement_desc = Column(String(19))
    judicial_nbr = Column(Integer)
    location = Column(String(4))
    offense_code = Column(Integer)
    offense_date = Column(Date)
    offense_desc = Column(String(31))
    offense_type = Column(String(3))
    original_sentence = Column(String(21))
    outtake_prosecutor = Column(String(31))
    post_judicial_date = Column(Date)
    post_judicial_field = Column(String(20))
    probation_prosecutor = Column(String(31))
    race = Column(String(2))
    reduced_offense_code = Column(Integer)
    reduced_offense_desc = Column(String(31))
    reduced_offense_type = Column(String(3))
    revokation_prosecutor = Column(String(31))
    sentence = Column(String(11))
    sentence_desc = Column(String(24))
    sentence_end_date = Column(Date)
    sentence_start_date = Column(Date)
    setting_date = Column(Date)
    setting_type = Column(String(2))
    sex = Column(String(2))
    sid = Column(Integer)


def get_engine(conf_file="./conf.json"):
    conf = utils.load_json(conf_file)
    engine = sqlalchemy.create_engine(conf["engine"])
    return engine


def get_coltypes(cls):
    out = {}
    for k in cls.__table__.columns.keys():
        out[k] = cls.__table__.columns[k].type.__class__.__name__
    return out


def create_tables(engine):
    Base.metadata.create_all(engine)


def attach_engine(engine):
    Session.configure(bind=engine)


Session = sqlalchemy.orm.sessionmaker()


