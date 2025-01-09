import sqlite3
import random

# Ouverture ou initialisation de la base de données
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Insertion de plusieurs données
values = []
for i in range(3):
    # Capteur de luminosite :
    values.append((1, random.randint(50, 3200)))

    # Capteur d'humidite :
    values.append((2, random.randint(1, 100)))

    # Capteur de temperature:
    values.append((3, random.randint(-30, 60)))

    # Capteur de presence :
    values.append((4, random.randint(0, 1)))


# Insertion des données dans la table 'Mesure'
c.executemany('INSERT INTO Mesure (Id_capteur, Valeur) VALUES (?, ?)', values)

#-------------------------------------------------------------------------------------------

# Lecture dans la base avec un SELECT (optionnel)
c.execute('SELECT * FROM Mesure')
rows = c.fetchall()
for row in rows:
    print(dict(row))  # Affichage de chaque ligne comme un dictionnaire




# Insertion de plusieurs données
values2 = []
val_conso_eau = random.randint(10, 2000)
val_conso_elec = random.randint(250, 1100)
val_conso_dechet = random.randint(20, 200)
val_conso_impot = random.randint(10, 75)
for i in range(3):
    # Eau :
    values2.append(("L", "Eau", random.randint(int(val_conso_eau*0.0039), int(val_conso_eau*0.0043)), val_conso_eau))

    # Electricite :
    values2.append(("kWh", "Electricite", random.randint(int(val_conso_elec*0.10), int(val_conso_elec*0.12)), val_conso_elec))

    # Dechet :
    values2.append(("Kg", "Dechet", random.randint(int(val_conso_dechet*0.09), int(val_conso_dechet*0.1)), val_conso_dechet))

    # Impot: location du m carré à Paris
    values2.append(("m^2", "Impot", random.randint(val_conso_impot*39, val_conso_impot*45), val_conso_impot))


# Insertion des données dans la table 'Facture'
c.executemany('INSERT INTO Facture (Unite, Type_facture, Montant, Val_conso) VALUES (?, ?, ?, ?)', values2)

#-------------------------------------------------------------------------------------------------

# Lecture dans la base avec un SELECT (optionnel)
c.execute('SELECT * FROM Facture')
rows = c.fetchall()
for row in rows:
    print(dict(row))  # Affichage de chaque ligne comme un dictionnaire

# Commit et fermeture de la connexion
conn.commit()
conn.close()
