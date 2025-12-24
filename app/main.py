from fastapi import FastAPI
from app.db import engine, Base
from app.routers import auth, terms, term_selfsame, term_synonym
import time
from sqlalchemy.exc import OperationalError

app = FastAPI(title="Term Model Service with JWT")

@app.on_event("startup")
def startup():
    retries = 5
    while retries:
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected")
            break
        except OperationalError:
            retries -= 1
            print("⏳ Waiting for database...")
            time.sleep(2)

app.include_router(auth.router)
app.include_router(terms.router, prefix="/terms", tags=["terms"])
app.include_router(term_selfsame.router, prefix="/term-selfsame", tags=["term_selfsame"])
app.include_router(term_synonym.router, prefix="/term-synonym", tags=["term_synonym"])
