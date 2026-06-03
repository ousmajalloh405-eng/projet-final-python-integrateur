#!/bin/bash
# SCRIPT : Lancer le projet automatiquement
# AUTEUR : Ousmane Jalloh
# USAGE  : bash scripts/start.sh


echo "🚀 Démarrage du projet Gestion des Étudiants..."

# 1. Vérifier PostgreSQL
echo "🗄️  Vérification de PostgreSQL..."
sudo service postgresql start

# 2. Aller dans le bon dossier
cd ~/gestion-etudiants

# 3. Lancer le serveur FastAPI
echo "⚡ Lancement du serveur FastAPI..."
echo "✅ Serveur disponible sur http://127.0.0.1:8000"
echo "📖 Documentation sur http://127.0.0.1:8000/docs"
echo "🌐 Application sur file:///home/phonix/gestion-etudiants/frontend/index.html"
echo ""
echo "⚠️  Appuie sur CTRL+C pour arrêter le serveur"
echo ""

python3 -m uvicorn src.main:app --reload