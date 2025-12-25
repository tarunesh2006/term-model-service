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


class TermSynonymCreate(BaseModel):
    turf_name: str
    term: str
    synonym: str

class TermSynonymResponse(BaseModel):
    term_synonym_id: str
    turf_name: str
    terms: list[str]

class TermSelfsameCreate(BaseModel):
    turf_name: str
    term: str
    selfsame: str


class TermSelfsameResponse(BaseModel):
    term_selfsame_id: str
    turf_name: str
    terms: list[str]


