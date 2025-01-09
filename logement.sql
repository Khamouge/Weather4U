-- TP1 IoT Partie 2 - BOU ALI Aymen

-- ----------------------------------------------------- Question 2 ----------------------------------------------------- 

-- On détruit une à une les tables créées
DROP TABLE IF EXISTS Logement;

DROP TABLE IF EXISTS Adresse;

DROP TABLE IF EXISTS Piece;

DROP TABLE IF EXISTS Capteur;

DROP TABLE IF EXISTS Type_capteur;

DROP TABLE IF EXISTS Mesure;

DROP TABLE IF EXISTS Facture;


-- ----------------------------------------------------- Question 3 ----------------------------------------------------- 

-- On crée les tables demandées

-- Table pour Logement :
-- Ici on instancie une clé primaire en incrémentation automatique pour ne pas avoir de problèmes.
-- On décide de mettre le numéro de téléphone en tant que INT. Puisqu'il peut arriver d'avoir des numéro de téléphones étrangers et donc d'avoir des (+...) devant le numéro on décide que le numéro sera décrit comme étant : 0011223344
-- La date sera décrite comme étant : JJMMAAAA
CREATE TABLE Logement (id INTEGER PRIMARY KEY AUTOINCREMENT, Numero_tel TEXT NOT NULL, Adresse_IP TEXT NOT NULL, Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, idAd INTEGER NOT NULL, FOREIGN KEY (idAd) REFERENCES Adresse(id));

-- Table pour Adresse :
-- On décide de séparer l'adresse et d'en faire une table afin de faciliter la prise d'information.
CREATE TABLE Adresse (id INTEGER PRIMARY KEY AUTOINCREMENT, Numero INT NOT NULL, Nom_voie TEXT NOT NULL, Code INT NOT NULL, Ville Text NOT NULL);

-- Table pour Piece :
-- Chacun des éléments de la pièce sont des valeurs pour la matrice indiquant la position de la pièce, c'est pourquoi ils seront en INT.
CREATE TABLE Piece (id INTEGER PRIMARY KEY AUTOINCREMENT, X INT NOT NULL, Y INT NOT NULL, Z INT NOT NULL);

-- Table pour Capteur :
-- Toutes les références des capteurs seront en texte si jamais ils sont composés de lettres ou de caractères spéciaux. La date sera décrite comme étant : JJMMAAAA
CREATE TABLE Capteur (id INTEGER PRIMARY KEY AUTOINCREMENT, Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Ref_commerciale TEXT NOT NULL, Ref_piece TEXT NOT NULL, Port INTEGER NOT NULL, FOREIGN KEY (Port) REFERENCES Mesure(id));

-- Table pour Type_capteur :
-- Cette table ne contiendra que la plage de précision et aucune autre spécificités.
CREATE TABLE Type_capteur (id INTEGER PRIMARY KEY AUTOINCREMENT, Nom TEXT NOT NULL, Unite TEXT NOT NULL, Plage_de_precision TEXT NOT NULL);

-- Table pour Mesure :
-- La date sera décrite comme étant : JJMMAAAA
CREATE TABLE Mesure (id INTEGER PRIMARY KEY AUTOINCREMENT, Id_capteur INT NOT NULL, Valeur INT NOT NULL, Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- Table pour Facture :
-- La date sera décrite comme étant : JJMMAAAA
CREATE TABLE Facture (id INTEGER PRIMARY KEY AUTOINCREMENT, Unite TEXT NOT NULL, Type_facture TEXT NOT NULL, Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Montant FLOAT NOT NULL, Val_conso INT NOT NULL);


-- ----------------------------------------------------- Question 4 -----------------------------------------------------

-- On instancie un logement avec 4 pièces

INSERT INTO Logement (Numero_tel, Adresse_IP, idAd) VALUES
        (0011223344, "123.123.12", 1);

INSERT INTO Adresse (Numero, Nom_voie, Code, Ville) VALUES
       (4, "allée des groseilliers", 92140, "Clamart");

INSERT INTO Piece (X, Y, Z) VALUES
        (1, 2, 3),
        (2, 1, 3),
        (3, 2, 1),
        (1, 3, 2);


-- ----------------------------------------------------- Question 5 -----------------------------------------------------

INSERT INTO Type_capteur (Nom, Unite, Plage_de_precision) VALUES
        ("Luminosite", "ISO", "[50 ; 3200]"),
        ("Humidite", "%", "[0 ; 100]"),
        ("Temperature", "°C", "[-30 ; 60]"),
        ("Presence", "Yes/No", "0/1");


-- ----------------------------------------------------- Question 6 -----------------------------------------------------

INSERT INTO Capteur (Ref_commerciale, Ref_piece, Port) VALUES
        ("1A2Z3E4R5T6Y", "000001", 1),
        ("1Q2W3E4R5T6Y", "000001", 2);


-- ----------------------------------------------------- Question 7 -----------------------------------------------------

INSERT INTO Mesure (Id_capteur, Valeur) VALUES
        (1, 700),
        (2, 20);


-- ----------------------------------------------------- Question 8-----------------------------------------------------

INSERT INTO Facture (Unite, Type_facture, Montant, Val_conso) VALUES
        ("L", "Eau", 450.1, 5000),
        ("W", "Electricite", 240, 75),
        ("Kg", "Dechet", 60, 245),
        ("Euro", "Impot", 1400, 30);


