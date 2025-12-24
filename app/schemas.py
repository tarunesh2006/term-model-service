from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TermCreate(BaseModel):
    turf_name: str
    term_name: str
    language: str
    country: str
    term_description: str | None = None
    term_acronym: str | None = None


class TermResponse(BaseModel):
    term_id: str
    term_name: str
    language: str
    country: str
    term_description: str | None
    term_acronym: str | None

    class Config:
        from_attributes = True


class SynonymGroupCreate(BaseModel):
    turf_name: str
    terms: List[str]


class SynonymGroupResponse(BaseModel):
    term_synonym_id: str
    turf_name: str
    terms: List[str]


class SelfsameGroupCreate(BaseModel):
    turf_name: str
    terms: List[str]


class SelfsameGroupResponse(BaseModel):
    term_selfsame_id: str
    turf_name: str
    terms: List[str]