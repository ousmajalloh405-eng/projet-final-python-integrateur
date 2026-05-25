

import sys
sys.path.append(".")
from src.database import get_connection

def calculer_moyennes():
    conn = get_connection()
    if not conn:
        print("❌ Connexion échouée !")
        return

    cur = conn.cursor()

    # Calculer et mettre à jour la moyenne générale de chaque étudiant
    cur.execute("""
        UPDATE etudiants
        SET moyenne_generale = (
            SELECT ROUND(AVG(moyenne)::numeric, 2)
            FROM etudiant_matiere
            WHERE id_etudiant = etudiants.id
        )
    """)

    conn.commit()

    # Vérifier le résultat
    cur.execute("""
        SELECT nom, prenom, moyenne_generale
        FROM etudiants
        WHERE moyenne_generale IS NOT NULL
        ORDER BY moyenne_generale DESC
        LIMIT 5
    """)

    print("🏆 Top 5 des meilleurs étudiants :")
    for row in cur.fetchall():
        print(f"   {row[1]} {row[0]} → {row[2]}")

    cur.close()
    conn.close()
    print("✅ Moyennes calculées !")

if __name__ == "__main__":
    calculer_moyennes()