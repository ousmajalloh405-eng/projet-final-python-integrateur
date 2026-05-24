

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from src.database import get_connection

# Créer l'application FastAPI
app = FastAPI(
    title="Gestion des Étudiants",
    description="API REST pour gérer les résultats scolaires",
    version="1.0.0"
)

# Autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Modèle pour ajouter un étudiant ──
class EtudiantCreate(BaseModel):
    code      : str
    numero    : str
    prenom    : str
    nom       : str
    date_naissance : str
    classe    : str

# ── Modèle pour modifier un étudiant ──
class EtudiantUpdate(BaseModel):
    prenom    : Optional[str] = None
    nom       : Optional[str] = None
    date_naissance : Optional[str] = None
    classe    : Optional[str] = None

# ─────────────────────────────────────────────
# ROUTE 1 : Health check
# ─────────────────────────────────────────────
@app.get("/")
def health_check():
    return {
        "status"  : "✅ API en ligne",
        "message" : "Bienvenue sur l'API Gestion des Étudiants"
    }

# ─────────────────────────────────────────────
# ROUTE 2 : Liste des étudiants
# ─────────────────────────────────────────────
@app.get("/etudiants")
def get_etudiants():
    conn = get_connection()
    if not conn:
        return {"erreur": "Connexion échouée"}

    cur = conn.cursor()
    cur.execute("""
        SELECT
            e.id, e.code, e.numero, e.prenom, e.nom,
            e.date_naissance, c.nom_classe,
            e.moyenne_generale, e.source, e.is_archived
        FROM etudiants e
        JOIN classes c ON e.id_classe = c.id
        WHERE e.is_archived = FALSE
        ORDER BY e.nom, e.prenom
    """)

    colonnes  = [desc[0] for desc in cur.description]
    resultats = [dict(zip(colonnes, row)) for row in cur.fetchall()]

    cur.close()
    conn.close()

    return {"total": len(resultats), "etudiants": resultats}

# ─────────────────────────────────────────────
# ROUTE 3 : Un étudiant par numéro
# ─────────────────────────────────────────────
@app.get("/etudiants/{numero}")
def get_etudiant(numero: str):
    conn = get_connection()
    if not conn:
        return {"erreur": "Connexion échouée"}

    cur = conn.cursor()
    cur.execute("""
        SELECT
            e.id, e.code, e.numero, e.prenom, e.nom,
            e.date_naissance, c.nom_classe,
            e.moyenne_generale, e.source
        FROM etudiants e
        JOIN classes c ON e.id_classe = c.id
        WHERE e.numero = %s
    """, (numero,))

    colonnes = [desc[0] for desc in cur.description]
    row      = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {"erreur": f"Étudiant {numero} non trouvé"}

    return dict(zip(colonnes, row))

# ─────────────────────────────────────────────
# ROUTE 4 : Ajouter un étudiant
# ─────────────────────────────────────────────
@app.post("/etudiants")
def ajouter_etudiant(etudiant: EtudiantCreate):
    conn = get_connection()
    if not conn:
        return {"erreur": "Connexion échouée"}

    cur = conn.cursor()

    # Créer la classe si elle n'existe pas
    cur.execute("""
        INSERT INTO classes (nom_classe)
        VALUES (%s)
        ON CONFLICT (nom_classe) DO NOTHING
        RETURNING id
    """, (etudiant.classe,))
    row = cur.fetchone()
    if row:
        id_classe = row[0]
    else:
        cur.execute("SELECT id FROM classes WHERE nom_classe = %s", (etudiant.classe,))
        id_classe = cur.fetchone()[0]

    # Insérer l'étudiant
    cur.execute("""
        INSERT INTO etudiants (code, numero, prenom, nom, date_naissance, id_classe, source)
        VALUES (%s, %s, %s, %s, %s, %s, 'DB')
        RETURNING id
    """, (
        etudiant.code, etudiant.numero, etudiant.prenom,
        etudiant.nom, etudiant.date_naissance, id_classe
    ))

    id_etudiant = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "✅ Étudiant ajouté !", "id": id_etudiant}

# ─────────────────────────────────────────────
# ROUTE 5 : Modifier un étudiant
# ─────────────────────────────────────────────
@app.put("/etudiants/{numero}")
def modifier_etudiant(numero: str, data: EtudiantUpdate):
    conn = get_connection()
    if not conn:
        return {"erreur": "Connexion échouée"}

    cur = conn.cursor()

    if data.classe:
        cur.execute("""
            INSERT INTO classes (nom_classe)
            VALUES (%s) ON CONFLICT (nom_classe) DO NOTHING
        """, (data.classe,))
        cur.execute("SELECT id FROM classes WHERE nom_classe = %s", (data.classe,))
        id_classe = cur.fetchone()[0]
        cur.execute("UPDATE etudiants SET id_classe = %s WHERE numero = %s", (id_classe, numero))

    if data.prenom:
        cur.execute("UPDATE etudiants SET prenom = %s WHERE numero = %s", (data.prenom, numero))
    if data.nom:
        cur.execute("UPDATE etudiants SET nom = %s WHERE numero = %s", (data.nom, numero))
    if data.date_naissance:
        cur.execute("UPDATE etudiants SET date_naissance = %s WHERE numero = %s", (data.date_naissance, numero))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": f"✅ Étudiant {numero} modifié !"}

# ─────────────────────────────────────────────
# ROUTE 6 : Archiver un étudiant
# ─────────────────────────────────────────────
@app.put("/etudiants/{numero}/archiver")
def archiver_etudiant(numero: str):
    conn = get_connection()
    if not conn:
        return {"erreur": "Connexion échouée"}

    cur = conn.cursor()
    cur.execute("UPDATE etudiants SET is_archived = TRUE WHERE numero = %s", (numero,))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": f"✅ Étudiant {numero} archivé !"}
@app.get("/stats")
def get_stats():
    conn = get_connection()
    if not conn:
        return {"erreur": "Connexion échouée"}
    cur = conn.cursor()
    # Total étudiants
    cur.execute("SELECT COUNT(*) FROM etudiants WHERE is_archived = FALSE")
    total = cur.fetchone()[0]

    # Répartition par classe
    cur.execute("""
        SELECT c.nom_classe, COUNT(e.id), AVG(e.moyenne_generale)
        FROM etudiants e
        JOIN classes c ON e.id_classe = c.id
        WHERE e.is_archived = FALSE
        GROUP BY c.nom_classe
        ORDER BY c.nom_classe
    """)
    par_classe = [
        {"classe": row[0], "total": row[1], "moyenne": round(row[2] or 0, 2)}
        for row in cur.fetchall()
    ]

    # Total archivés
    cur.execute("SELECT COUNT(*) FROM etudiants WHERE is_archived = TRUE")
    total_archives = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "total"         : total,
        "total_archives": total_archives,
        "par_classe"    : par_classe
    }