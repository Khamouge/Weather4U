from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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
async def get_factures_piechart():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Type_facture, SUM(Montant) as total FROM Facture GROUP BY Type_facture")
    facture_data = cursor.fetchall()
    conn.close()

    # Préparer les données pour Google Charts
    data_rows = ""
    for row in facture_data:
        data_rows += f"['{row['Type_facture']}', {row['total']}],"

    # Code HTML avec Google Charts pour afficher le camembert
    html_content = f"""
    <html>
      <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load('current', {{'packages':['corechart']}});
          google.charts.setOnLoadCallback(drawChart);

          function drawChart() {{
            var data = google.visualization.arrayToDataTable([
              ['Type de Facture', 'Montant'],
              {data_rows}
            ]);

            var options = {{
              title: 'Répartition des factures par type',
              is3D: true,
            }};

            var chart = new google.visualization.PieChart(document.getElementById('piechart'));
            chart.draw(data, options);
          }}
        </script>
      </head>
      <body>
        <h2>Camembert des factures</h2>
        <div id="piechart" style="width: 900px; height: 500px;"></div>
      </body>
    </html>
    """

    return HTMLResponse(content=html_content)



