from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app import models, schemas

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[schemas.TermSelfsameResponse])
def get_all_selfsame(db: Session = Depends(get_db)):
    rows = db.query(models.TermSelfsame).all()

    grouped = {}
    for r in rows:
        if r.term_selfsame_id not in grouped:
            grouped[r.term_selfsame_id] = {
                "term_selfsame_id": r.term_selfsame_id,
                "turf_name": r.turf_name,
                "terms": [],
            }
        grouped[r.term_selfsame_id]["terms"].append(r.term_name)

    return list(grouped.values())



# ✅ CREATE
@router.post("/", response_model=schemas.TermSelfsameResponse)
def create_term_selfsame(
    data: schemas.TermSelfsameCreate,
    db: Session = Depends(get_db),
):
    # 1️⃣ Validate both terms exist in terms table
    term1 = (
        db.query(models.Term)
        .filter(models.Term.term_name.ilike(data.term))
        .first()
    )
    term2 = (
        db.query(models.Term)
        .filter(models.Term.term_name.ilike(data.selfsame))
        .first()
    )

    if not term1:
        raise HTTPException(400, detail=f"Term '{data.term}' does not exist")

    if not term2:
        raise HTTPException(400, detail=f"Selfsame '{data.selfsame}' does not exist")

    # 2️⃣ Check if selfsame group already exists for this turf
    existing = (
        db.query(models.TermSelfsame)
        .filter(models.TermSelfsame.turf_name.ilike(data.turf_name))
        .first()
    )

    if existing:
        selfsame_id = existing.term_selfsame_id
    else:
        last = (
            db.query(models.TermSelfsame)
            .order_by(models.TermSelfsame.id.desc())
            .first()
        )
        next_num = int(last.term_selfsame_id[2:]) + 1 if last else 1
        selfsame_id = f"SS{next_num:03d}"

    # 3️⃣ Insert BOTH terms if not already present
    for term_name in {term1.term_name, term2.term_name}:
        exists = (
            db.query(models.TermSelfsame)
            .filter(
                models.TermSelfsame.term_selfsame_id == selfsame_id,
                models.TermSelfsame.term_name.ilike(term_name),
            )
            .first()
        )

        if not exists:
            db.add(
                models.TermSelfsame(
                    term_selfsame_id=selfsame_id,
                    turf_name=data.turf_name,
                    term_name=term_name,
                )
            )

    db.commit()

    # 4️⃣ Return grouped response
    rows = (
        db.query(models.TermSelfsame)
        .filter(models.TermSelfsame.term_selfsame_id == selfsame_id)
        .all()
    )

    return {
        "term_selfsame_id": selfsame_id,
        "turf_name": data.turf_name,
        "terms": [r.term_name for r in rows],
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


