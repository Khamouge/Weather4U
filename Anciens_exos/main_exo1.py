from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Fonction utilitaire pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    return conn

class Mesure(BaseModel):
    id_capteur: int
    valeur: int

class Facture(BaseModel):
    unite: str
    type_facture: str
    montant: float
    val_conso: int

app.mount("/static", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "home.html")

@app.get("/mesures/")
async def get_mesures():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Mesure")
    mesures = cursor.fetchall()
    conn.close()
    return [dict(mesure) for mesure in mesures]

@app.get("/factures/")
async def get_factures():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Facture")
    factures = cursor.fetchall()
    conn.close()
    return [dict(facture) for facture in factures]

@app.post("/mesures/")
async def add_mesure(mesure: Mesure):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Mesure (Id_capteur, Valeur) VALUES (?, ?)",
        (mesure.id_capteur, mesure.valeur)
    )
    conn.commit()
    mesure_id = cursor.lastrowid
    conn.close()
    return {"id": mesure_id, "message": "Mesure ajoutée avec succès"}

@app.post("/factures/")
async def add_facture(facture: Facture):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Facture (Unite, Type_facture, Montant, Val_conso) VALUES (?, ?, ?, ?)",
        (facture.unite, facture.type_facture, facture.montant, facture.val_conso)
    )
    conn.commit()
    facture_id = cursor.lastrowid
    conn.close()
    return {"id": facture_id, "message": "Facture ajoutée avec succès"}