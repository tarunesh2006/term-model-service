from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app import models, schemas
import uuid

router = APIRouter(dependencies=[Depends(get_current_user)])

# ✅ GET ALL
@router.get("/")
def list_terms(db: Session = Depends(get_db)):
    return db.query(models.Term).all()

# ✅ GET BY ID
@router.get("/{term_id}")
def get_term(term_id: str, db: Session = Depends(get_db)):
    term = db.query(models.Term).filter_by(term_id=term_id).first()
    if not term:
        raise HTTPException(404, "Term not found")
    return term

# ✅ CREATE
@router.post("/")
def create_term(data: schemas.TermCreate, db: Session = Depends(get_db)):
    turf = db.query(models.Turf).filter_by(turf_name=data.turf_name).first()
    if not turf:
        turf = models.Turf(turf_name=data.turf_name)
        db.add(turf)
        db.commit()
        db.refresh(turf)

    term_id = f"{data.term_name.lower()}_{uuid.uuid4().hex[:4]}"

    term = models.Term(
        turf_rid=turf.turf_rid,
        term_id=term_id,
        term_name=data.term_name,
        language=data.language,
        country=data.country,
        term_description=data.term_description,
        term_acronym=data.term_acronym
    )
    db.add(term)
    db.commit()
    db.refresh(term)
    return term

# ✅ UPDATE
@router.put("/{term_id}")
def update_term(term_id: str, data: schemas.TermCreate, db: Session = Depends(get_db)):
    term = db.query(models.Term).filter_by(term_id=term_id).first()
    if not term:
        raise HTTPException(404, "Term not found")

    term.term_name = data.term_name
    term.language = data.language
    term.country = data.country
    term.term_description = data.term_description
    term.term_acronym = data.term_acronym

    db.commit()
    return {"message": "Term updated"}

# ✅ DELETE
@router.delete("/{term_name}")
def delete_term(term_name: str, db: Session = Depends(get_db)):
    term = db.query(models.Term).filter_by(term_name=term_name).first()
    if not term:
        raise HTTPException(404, "Term not found")

    # ---- SYNONYM GROUP CLEANUP ----
    groups = db.query(models.TermSynonym).filter_by(term_name=term_name).all()
    for g in groups:
        members = db.query(models.TermSynonym).filter_by(
            term_synonym_id=g.term_synonym_id
        ).all()

        if len(members) == 2:
            for m in members:
                db.delete(m)
        else:
            db.delete(g)

    # ---- SELFSAME GROUP CLEANUP ----
    groups = db.query(models.TermSelfsame).filter_by(term_name=term_name).all()
    for g in groups:
        members = db.query(models.TermSelfsame).filter_by(
            term_selfsame_id=g.term_selfsame_id
        ).all()

        if len(members) == 2:
            for m in members:
                db.delete(m)
        else:
            db.delete(g)

    db.delete(term)
    db.commit()

    return {"message": "Term deleted with relationship cleanup"}
