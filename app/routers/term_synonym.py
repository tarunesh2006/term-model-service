from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[schemas.SynonymGroupResponse])
def list_synonym_groups(db: Session = Depends(get_db)):
    rows = db.query(models.TermSynonym).all()

    groups = {}
    for r in rows:
        groups.setdefault(r.term_synonym_id, []).append(r.term_name)

    return [
        {
            "term_synonym_id": k,
            "turf_name": "Oil and Gas",
            "terms": v
        }
        for k, v in groups.items()
    ]

# ✅ CREATE
@router.post("/", response_model=schemas.SynonymGroupResponse)
def create_synonym_group(data: schemas.SynonymGroupCreate, db: Session = Depends(get_db)):
    turf_rid = 0  # example mapping

    # validate all terms exist
    for name in data.terms:
        if not db.query(models.Term).filter_by(term_name=name).first():
            raise HTTPException(400, f"Term '{name}' does not exist")

    last = db.query(models.TermSynonym).order_by(models.TermSynonym.term_synonym_id.desc()).first()
    new_id = "SY001" if not last else f"SY{int(last.term_synonym_id[2:]) + 1:03d}"

    for name in data.terms:
        db.add(models.TermSynonym(
            term_synonym_id=new_id,
            turf_rid=turf_rid,
            term_name=name
        ))

    db.commit()

    return {
        "term_synonym_id": new_id,
        "turf_name": data.turf_name,
        "terms": data.terms
    }

# ✅ DELETE GROUP
@router.delete("/{term_synonym_id}")
def delete_synonym(term_synonym_id: str, db: Session = Depends(get_db)):
    records = db.query(models.TermSynonym).filter_by(
        term_synonym_id=term_synonym_id
    ).all()

    if not records:
        raise HTTPException(404, "Synonym not found")

    for r in records:
        db.delete(r)
    db.commit()

    return {"message": "Synonym group deleted"}