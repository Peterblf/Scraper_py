# 📚 Projet – Books to Scrape  

## 🎯 Objectif  
Ce projet consiste à scraper le site [Books to Scrape](https://books.toscrape.com/) afin de récupérer des informations sur tous les livres disponibles.  
Les données collectées sont ensuite enregistrées dans des fichiers CSV et les images des livres sont téléchargées localement.

## ⚙️ Outils Utilisé
- **Python 3**  
- **requests** – pour envoyer les requêtes HTTP  
- **scrapy (Selector)** – pour extraire les données du HTML  
- **pandas** – pour sauvegarder les données en CSV  

## 📁 Structure du projet  
```txt
projet_scraper/
│
├── main.py
├── requirements.txt
└── outputs/
├── csv/
│ ├── category_travel.csv
│ ├── category_poetry.csv
│ └── ...
└── img/
├── Travel/
├── Poetry/
└── ...
```
