📚 Projet – Books to Scrape
🎯 Objectif

Ce projet consiste à scraper le site Books to Scrape
 afin de récupérer des informations sur tous les livres disponibles.
Les données collectées sont ensuite enregistrées dans des fichiers CSV et les images des livres sont téléchargées localement.

⚙️ Technologies utilisées

Python 3

requests – pour envoyer les requêtes HTTP

scrapy (Selector) – pour extraire les données du HTML

pandas – pour sauvegarder les données en CSV

📁 Structure du projet
projet_scraper/
│
├── main.py
├── requirements.txt
└── outputs/
    ├── csv/
    │   ├── category_travel.csv
    │   ├── category_poetry.csv
    │   └── ...
    └── img/
        ├── Travel/
        ├── Poetry/
        └── ...

🚀 Installation et exécution

Cloner ou copier le projet

cd projet_scraper


Créer un environnement virtuel (optionnel mais conseillé)

python -m venv .venv
.venv\Scripts\activate     # sur Windows
source .venv/bin/activate  # sur macOS / Linux


Installer les dépendances

pip install -r requirements.txt


Lancer le script

python main.py

💾 Résultats

Un CSV par catégorie dans outputs/csv/

Les images de chaque livre dans outputs/img/<catégorie>/

Chaque CSV contient :

Titre

Prix

Stock disponible

Note

UPC

Catégorie

Lien du produit

Lien de l’image
