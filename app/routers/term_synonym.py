from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[schemas.TermSynonymResponse])
def get_all_synonyms(db: Session = Depends(get_db)):
    rows = db.query(models.TermSynonym).all()

    grouped = {}
    for r in rows:
        if r.term_synonym_id not in grouped:
            grouped[r.term_synonym_id] = {
                "term_synonym_id": r.term_synonym_id,
                "turf_name": r.turf_name,
                "terms": [],
            }
        grouped[r.term_synonym_id]["terms"].append(r.term_name)

    return list(grouped.values())

# ✅ CREATE
@router.post("/", response_model=schemas.TermSynonymResponse)
def create_term_synonym(
    data: schemas.TermSynonymCreate,
    db: Session = Depends(get_db),
):
    # 1️⃣ Validate BOTH terms exist in terms table
    term1 = (
        db.query(models.Term)
        .filter(models.Term.term_name.ilike(data.term))
        .first()
    )
    term2 = (
        db.query(models.Term)
        .filter(models.Term.term_name.ilike(data.synonym))
        .first()
    )

    if not term1:
        raise HTTPException(400, detail=f"Term '{data.term}' does not exist")

    if not term2:
        raise HTTPException(400, detail=f"Synonym '{data.synonym}' does not exist")

    # 2️⃣ Check if synonym group already exists for turf
    existing = (
        db.query(models.TermSynonym)
        .filter(models.TermSynonym.turf_name.ilike(data.turf_name))
        .first()
    )

    if existing:
        synonym_id = existing.term_synonym_id
    else:
        last = (
            db.query(models.TermSynonym)
            .order_by(models.TermSynonym.id.desc())
            .first()
        )
        next_num = int(last.term_synonym_id[2:]) + 1 if last else 1
        synonym_id = f"SY{next_num:03d}"

    # 3️⃣ Insert BOTH terms if not already present
    for term_name in {term1.term_name, term2.term_name}:
        exists = (
            db.query(models.TermSynonym)
            .filter(
                models.TermSynonym.term_synonym_id == synonym_id,
                models.TermSynonym.term_name.ilike(term_name),
            )
            .first()
        )
        if not exists:
            db.add(
                models.TermSynonym(
                    term_synonym_id=synonym_id,
                    turf_name=data.turf_name,
                    term_name=term_name,
                )
            )

    db.commit()

    # 4️⃣ Return grouped response
    rows = (
        db.query(models.TermSynonym)
        .filter(models.TermSynonym.term_synonym_id == synonym_id)
        .all()
    )

    return {
        "term_synonym_id": synonym_id,
        "turf_name": data.turf_name,
        "terms": [r.term_name for r in rows],
    }


    # 3️⃣ Prevent duplicate
    duplicate = (
        db.query(models.TermSynonym)
        .filter(
            models.TermSynonym.turf_name.ilike(data.turf_name),
            models.TermSynonym.term_name.ilike(data.term_name),
        )
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=400, detail="Term already exists in this turf")

    # 4️⃣ Insert
    new_row = models.TermSynonym(
        term_synonym_id=synonym_id,
        turf_name=data.turf_name,
        term_name=term_exists.term_name,  # normalized
    )
    db.add(new_row)
    db.commit()

    rows = (
        db.query(models.TermSynonym)
        .filter(models.TermSynonym.term_synonym_id == synonym_id)
        .all()
    )

    return {
        "term_synonym_id": synonym_id,
        "turf_name": data.turf_name,
        "terms": [r.term_name for r in rows],
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