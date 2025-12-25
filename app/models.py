from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Turf(Base):
    __tablename__ = "turf"
    turf_rid = Column(Integer, primary_key=True)
    turf_name = Column(String, unique=True)

class Term(Base):
    __tablename__ = "terms"
    term_rid = Column(Integer, primary_key=True)
    turf_rid = Column(Integer, ForeignKey("turf.turf_rid"))
    term_id = Column(String, unique=True)
    term_name = Column(String)
    language = Column(String)
    country = Column(String)
    term_description = Column(String)
    term_acronym = Column(String)

class TermSynonym(Base):
    __tablename__ = "term_synonym"

    id = Column(Integer, primary_key=True, index=True)
    term_synonym_id = Column(String, index=True)
    turf_name = Column(String, index=True)
    term_name = Column(String, index=True)


class TermSelfsame(Base):
    __tablename__ = "term_selfsame"

    id = Column(Integer, primary_key=True, index=True)
    term_selfsame_id = Column(String, index=True)   # SS001, SS002...
    turf_name = Column(String, index=True)
    term_name = Column(String, index=True)
