from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import sqlite3
import openmeteo_requests
import requests_cache
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from retry_requests import retry
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# FastAPI app
app = FastAPI()

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
def get_7_day_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,  # Vous pouvez changer ces coordonnées
        "longitude": 13.41,
        "daily": [
            "temperature_2m_max", "temperature_2m_min", 
            "precipitation_sum", "relative_humidity_2m_max", "relative_humidity_2m_min"
        ],
        "timezone": "Europe/Berlin",  # Définir le fuseau horaire
        "past_days": 5
    }
    responses = openmeteo.weather_api(url, params=params)

    # Extraire les données de réponse
    response = responses[0]
    daily = response.Daily()

    # Extraire les valeurs pour les 7 prochains jours
    dates = pd.to_datetime(daily.Time(), unit="s", utc=True)
    temp_max = daily.Variables(0).ValuesAsNumpy()
    temp_min = daily.Variables(1).ValuesAsNumpy()
    precipitation = daily.Variables(2).ValuesAsNumpy()
    humidity_max = daily.Variables(3).ValuesAsNumpy()
    humidity_min = daily.Variables(4).ValuesAsNumpy()

    # Créer un DataFrame avec les données des 7 jours
    daily_data = {
        "date": pd.date_range(start = pd.to_datetime(daily.Time(), unit = "s", utc = True),end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),freq = pd.Timedelta(seconds = daily.Interval()),inclusive = "left"),
        "temperature_max": temp_max,
        "temperature_min": temp_min,
        "precipitation": precipitation,
        "humidity_max": humidity_max,
        "humidity_min": humidity_min
    }

    # Nous limitons ici à 7 jours
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

# Endpoint pour récupérer et afficher les données météo pour les 7 jours à venir
@app.get("/weather/", response_class=HTMLResponse)
async def weather():
    # Récupérer les données météo pour les 7 jours à venir
    daily_dataframe = get_7_day_weather_data()

    # Générer un graphique pour la température (max et min)
    temp_img = generate_weather_graph(
        daily_dataframe,
        title="Température Maximale et Minimale (7 jours)",
        xlabel="Date",
        ylabel="Température (°C)",
        color="tab:red",
        y_data=daily_dataframe['temperature_max']
    )

    # Générer un graphique pour l'humidité (max et min)
    humidity_img = generate_weather_graph(
        daily_dataframe,
        title="Humidité Maximale et Minimale (7 jours)",
        xlabel="Date",
        ylabel="Humidité (%)",
        color="tab:blue",
        y_data=daily_dataframe['humidity_max']
    )

    # Générer un graphique pour les précipitations
    precipitation_img = generate_weather_graph(
        daily_dataframe,
        title="Précipitations (7 jours)",
        xlabel="Date",
        ylabel="Précipitations (mm)",
        color="tab:green",
        y_data=daily_dataframe['precipitation']
    )

    # Retourner la page HTML avec les graphiques et les valeurs
    html_content = f"""
    <html>
      <head>
        <title>Prévisions Météo pour les 7 Jours à Venir</title>
      </head>
      <body>
        <h2>Prévisions Météo pour les 7 Jours à Venir</h2>
        
        <h3>Graphiques Météo</h3>
        <h4>Température Maximale et Minimale</h4>
        <img src="data:image/png;base64,{temp_img}" />
        
        <h4>Humidité Maximale et Minimale</h4>
        <img src="data:image/png;base64,{humidity_img}" />
        
        <h4>Précipitations</h4>
        <img src="data:image/png;base64,{precipitation_img}" />
        
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)
