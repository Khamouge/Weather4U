# Projet Logement Éco-responsable - Weather4U BOU ALI Aymen

## Présentation du Projet
Weather4U combine plusieurs outils comme une API météo, une base de données, et des graphiques interactifs pour fournir une interface intuitive permettant de surveiller la météo, gérer la consommation énergétique, et suivre les capteurs présents dans le logement.

## Fonctionnalités du Projet

### Page Météo

- Utilisation de l'API OpenMeteo pour afficher des graphiques météo.
- Affiche des données sur les températures, l'humidité, et les précipitations.
- Les graphiques couvrent les 3 derniers jours et les 5 jours à venir.

### Page Consommation

- Intègre un Google Pie Chart qui montre les consommations énergétiques.
- Les données sont reliées à une base de données pour une gestion simple et efficace.

### Page Capteurs

- Liste des capteurs avec des boutons d’activation et de désactivation.
- Améliorations prévues : possibilité d’ajouter et de supprimer des capteurs, ainsi que de visualiser leurs données sous forme de graphiques.

### Base de Données

- Permet de stocker les mesures des capteurs et les factures énergétiques.
- Mise en place d’API pour ajouter et récupérer des données facilement.

## Structure du Projet

### Backend :

- Développé avec FastAPI pour gérer les différentes routes et fonctionnalités.
- Une base de données SQLite est utilisée pour stocker les données.

### Frontend :

- Pages web simples utilisant HTML et CSS.
- Graphiques météo générés avec Matplotlib et intégrés sous forme d’images.

### API Externe :

- Intégration de l’API OpenMeteo pour récupérer les prévisions météorologiques.
- Mise en cache des requêtes avec requests_cache pour améliorer les performances.

## Principaux Endpoints

### /weather/

Affiche les graphiques météo sur la température, l'humidité, et les précipitations.

### /accueil/

Affiche la page d'accueil du projet.

### /capteurs/

Permet de gérer l'état des capteurs installés.

### /factures/piechart

Génère un camembert affichant la répartition des consommations énergétiques.

### /mesures/ et /factures/

Points d'accès pour gérer les données des capteurs et les factures via des requêtes HTTP.

## Améliorations à Venir

Ajout de la gestion complète des capteurs :

- Possibilité d’ajouter et de supprimer des capteurs depuis l’interface.
- Visualisation des données collectées par les capteurs.
Optimisation de l’intégration des données météo.

Mise en place d’un système d’authentification pour protéger les données sensibles.
