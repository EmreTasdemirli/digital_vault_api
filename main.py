from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Digital Vault API", description="Sicherer Speicher für digitale Notizen")

# Datenmodell (Was darf ein Eintrag enthalten?)
class Note(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    category: str = "General"

# Simulierter Speicher (Datenbank-Ersatz)
db = []

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "Online", "message": "Willkommen bei der Vault API"}

@app.get("/notes", response_model=List[Note], tags=["Notes"])
def get_all_notes():
    """Gibt alle gespeicherten Notizen zurück."""
    return db

@app.post("/notes", response_model=Note, tags=["Notes"])
def create_note(note: Note):
    """Erstellt eine neue Notiz mit einer eindeutigen ID."""
    note.id = str(uuid.uuid4())[:8] # Generiert eine kurze ID
    db.append(note)
    return note

@app.delete("/notes/{note_id}", tags=["Notes"])
def delete_note(note_id: str):
    """Löscht eine Notiz anhand ihrer ID."""
    for index, item in enumerate(db):
        if item.id == note_id:
            db.pop(index)
            return {"message": f"Notiz {note_id} wurde gelöscht"}
    raise HTTPException(status_code=404, detail="Notiz nicht gefunden")