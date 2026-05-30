# 🎓 Exploitation des Données Python dans une Application Web

> Application web complète de gestion des résultats scolaires.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/Status-Terminé-green?style=flat)

---

## 📖 À propos

Ce projet permet de gérer les résultats scolaires d'élèves à partir d'un fichier JSON.
Il offre une API REST complète, une interface frontend interactive et un dashboard de statistiques.

---

## 🚀 Fonctionnalités

- ✅ Liste des étudiants avec pagination
- ✅ Recherche par nom, prénom, numéro
- ✅ Filtrage par classe
- ✅ Ajouter un étudiant
- ✅ Modifier un étudiant
- ✅ Archiver / Restaurer un étudiant
- ✅ Dashboard avec graphiques Chart.js
- ✅ Calcul automatique des moyennes générales

---

## 🛠️ Technologies

| Côté | Technologies |
|------|-------------|
| Backend | Python, FastAPI, Psycopg2 |
| Base de données | PostgreSQL |
| Frontend | HTML5, CSS3, JavaScript |
| Visualisation | Chart.js |
| Versioning | Git, GitHub |

---

## ⚙️ Installation

```bash
# 1. Cloner le projet
git clone https://github.com/ousmajalloh405-eng/projet-final-python-integrateur.git
cd projet-final-python-integrateur

# 2. Installer les dépendances
pip3 install fastapi uvicorn psycopg2-binary --break-system-packages

# 3. Créer la base de données
sudo -u postgres psql -c "CREATE DATABASE gestion_etudiants;"
cp database/schema.sql /tmp/schema.sql
sudo -u postgres psql -d gestion_etudiants -f /tmp/schema.sql

# 4. Importer les données
python3 scripts/csv_to_json.py
python3 scripts/import_data.py
python3 scripts/calculer_moyennes.py

# 5. Lancer le serveur
python3 -m uvicorn src.main:app --reload
```

---

## 🔌 API Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/` | Health check |
| GET | `/etudiants` | Liste des étudiants |
| POST | `/etudiants` | Ajouter un étudiant |
| PUT | `/etudiants/{numero}` | Modifier un étudiant |
| PUT | `/etudiants/{numero}/archiver` | Archiver |
| PUT | `/etudiants/{numero}/restaurer` | Restaurer |
| GET | `/etudiants/archives` | Liste des archives |
| GET | `/stats` | Statistiques dashboard |

---

## 📁 Structure
projet-final-python-integrateur/
├── data/
│   ├── eleves_valides.csv
│   └── valides.json
├── database/
│   └── schema.sql
├── src/
│   ├── main.py
│   └── database.py
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   └── archives.html
├── scripts/
│   ├── csv_to_json.py
│   ├── import_data.py
│   └── calculer_moyennes.py
└── README.md
---

## 👨‍💻 Auteur

**Ousmane Jalloh** — Data Engineer en formation · Dakar 🇸🇳

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/ousmajalloh405-eng)

---

<p align="center">Fait avec ❤️ par Ousmane Jalloh · DEV DATA P8</p>