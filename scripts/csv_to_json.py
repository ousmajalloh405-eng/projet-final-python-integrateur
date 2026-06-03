
# SCRIPT : Conversion CSV → JSON

import csv
import json
import ast
import os

# Chemins des fichiers
CSV_FILE = "data/eleves_valides.csv"
JSON_FILE = "data/valides.json"

def csv_to_json():
    etudiants = []

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue

            # Séparer les 7 colonnes
            parties = ligne.split(",", 6)

            if len(parties) < 7:
                continue

            code           = parties[0]
            numero         = parties[1]
            nom            = parties[2]
            prenom         = parties[3]
            date_naissance = parties[4]
            classe         = parties[5]
            matieres_raw   = parties[6]

            # Convertir la liste de matières
            try:
                matieres = ast.literal_eval(matieres_raw)
            except:
                matieres = []

            etudiant = {
                "code"           : code,
                "numero"         : numero,
                "nom"            : nom,
                "prenom"         : prenom,
                "date_naissance" : date_naissance,
                "classe"         : classe,
                "matieres"       : matieres
            }

            etudiants.append(etudiant)

    # Sauvegarder en JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(etudiants, f, ensure_ascii=False, indent=2)

    print(f"✅ Conversion terminée ! {len(etudiants)} étudiants exportés.")
    print(f"📁 Fichier créé : {JSON_FILE}")

# Lancer le script
csv_to_json()