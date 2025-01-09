from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import openmeteo_requests
import requests_cache
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from retry_requests import retry
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


# FastAPI app
app = FastAPI()

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Fonction utilitaire pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect('logement.db')           # http://127.0.0.1:8000/weather/
    conn.row_factory = sqlite3.Row
    return conn

# API Open-Meteo setup
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Fonction pour récupérer les données météo pour les 7 jours à venir
def get_5_day_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,  # Vous pouvez changer ces coordonnées
        "longitude": 13.41,
        "daily": [
            "temperature_2m_max", "temperature_2m_min", 
            "precipitation_sum", "relative_humidity_2m_max", "relative_humidity_2m_min"
        ],
        "timezone": "Europe/Berlin",  # Définir le fuseau horaire
        "past_days": 3,
        "forecast_days": 5
    }
    responses = openmeteo.weather_api(url, params=params)

    # Extraire les données de réponse
    response = responses[0]
    daily = response.Daily()

    # Extraire les valeurs pour les 5 prochains jours
    dates = pd.to_datetime(daily.Time(), unit="s", utc=True)
    temp_max = daily.Variables(0).ValuesAsNumpy()
    temp_min = daily.Variables(1).ValuesAsNumpy()
    precipitation = daily.Variables(2).ValuesAsNumpy()
    humidity_max = daily.Variables(3).ValuesAsNumpy()
    humidity_min = daily.Variables(4).ValuesAsNumpy()

    # Créer un DataFrame avec les données des 5 jours
    daily_data = {
        "date": pd.date_range(start = pd.to_datetime(daily.Time(), unit = "s", utc = True),end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),freq = pd.Timedelta(seconds = daily.Interval()),inclusive = "left"),
        "temperature_max": temp_max,
        "temperature_min": temp_min,
        "precipitation": precipitation,
        "humidity_max": humidity_max,
        "humidity_min": humidity_min
    }

    # Nous limitons ici à 5 jours
    daily_dataframe = pd.DataFrame(data=daily_data)
    return daily_dataframe

# Fonction pour générer un graphique
def generate_weather_graph(data, title, xlabel, ylabel, color, y_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['date'], y_data, color=color, marker='o')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

    # Convertir le graphique en image PNG et encoder en base64 pour l'afficher dans HTML
    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return img_str

# Configuration des templates
templates = Jinja2Templates(directory="templates")

@app.get("/weather/", response_class=HTMLResponse)
async def weather(request: Request):
    daily_dataframe = get_5_day_weather_data()

    temp_img = generate_weather_graph(
        daily_dataframe,
        title="Température Maximale et Minimale",
        xlabel="Date",
        ylabel="Température (°C)",
        color="tab:red",
        y_data=daily_dataframe['temperature_max']
    )

    humidity_img = generate_weather_graph(
        daily_dataframe,
        title="Humidité Maximale et Minimale",
        xlabel="Date",
        ylabel="Humidité (%)",
        color="tab:blue",
        y_data=daily_dataframe['humidity_max']
    )

    precipitation_img = generate_weather_graph(
        daily_dataframe,
        title="Précipitations",
        xlabel="Date",
        ylabel="Précipitations (mm)",
        color="tab:green",
        y_data=daily_dataframe['precipitation']
    )
 
    return templates.TemplateResponse(
    "weather_HTML.html",
    context={
        "request": request,
        "temp_img": temp_img,                   # Graphique des températures
        "humidity_img": humidity_img,           # Graphique de l'humidité
        "precipitation_img": precipitation_img  # Graphique des précipitations
    }
)

# Ici on permet l'accès au fichier html accueil
@app.get("/accueil/")
async def accueil(request: Request):
    return templates.TemplateResponse("accueil_html_site.html", {"request": request})
# Fin

# Ici on permet l'accès au fichier html capteurs
@app.get("/capteurs/")
async def accueil(request: Request):
    return templates.TemplateResponse("capteurs_html.html", {"request": request})
# Fin

class Mesure(BaseModel):
    id_capteur: int
    valeur: int

class Facture(BaseModel):
    unite: str
    type_facture: str
    montant: float
    val_conso: int

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

# Nouvel endpoint pour afficher un camembert des factures
@app.get("/factures/piechart", response_class=HTMLResponse)
async def get_factures_piechart(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Type_facture, SUM(Montant) as total FROM Facture GROUP BY Type_facture")
    facture_data = cursor.fetchall()
    conn.close()

    # Préparer les données pour Google Charts
    data_rows = [
        {"type_facture": row["Type_facture"], "total": row["total"]}
        for row in facture_data
    ]

    # Retourner le template Jinja
    return templates.TemplateResponse(
        "piechart.html",
        context={
            "request": request,
            "data_rows": data_rows,
        }
    )
