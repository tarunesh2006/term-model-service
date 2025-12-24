from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[schemas.SelfsameGroupResponse])
def get_selfsame_groups(db: Session = Depends(get_db)):
    rows = db.query(models.TermSelfsame).all()

    groups = {}

    for row in rows:
        key = (row.term_selfsame_id, row.turf_rid)

        if key not in groups:
            groups[key] = []

        groups[key].append(row.term_name)

    response = []
    for (group_id, turf_rid), terms in groups.items():
        response.append({
            "term_selfsame_id": group_id,
            "turf_name": "Oil and Gas",   # or map turf_rid → name
            "terms": terms
        })

    return response


# ✅ CREATE
@router.post("/", response_model=schemas.SelfsameGroupResponse)
def create_selfsame_group(
    data: schemas.SelfsameGroupCreate,
    db: Session = Depends(get_db)
):
    turf_rid = 0  # example

    # validate terms exist
    for name in data.terms:
        if not db.query(models.Term).filter_by(term_name=name).first():
            raise HTTPException(400, f"Term '{name}' does not exist")

    last = (
        db.query(models.TermSelfsame)
        .order_by(models.TermSelfsame.term_selfsame_id.desc())
        .first()
    )
    new_id = "SS001" if not last else f"SS{int(last.term_selfsame_id[2:]) + 1:03d}"

    for name in data.terms:
        db.add(models.TermSelfsame(
            term_selfsame_id=new_id,
            turf_rid=turf_rid,
            term_name=name
        ))

    db.commit()

    return {
        "term_selfsame_id": new_id,
        "turf_name": data.turf_name,
        "terms": data.terms
    }

# ✅ DELETE GROUP
@router.delete("/{term_selfsame_id}")
def delete_selfsame(term_selfsame_id: str, db: Session = Depends(get_db)):
    records = db.query(models.TermSelfsame).filter_by(
        term_selfsame_id=term_selfsame_id
    ).all()

    if not records:
        raise HTTPException(404, "Selfsame not found")

    # Delete selected records
    for r in records:
        db.delete(r)
    db.commit()

    return {"message": "Selfsame group deleted"}


