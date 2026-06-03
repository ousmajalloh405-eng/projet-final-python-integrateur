
# SCRIPT : Import valides.json → PostgreSQL


import json
import sys
sys.path.append(".")
from src.database import get_connection

def import_data():
    # Lire le fichier JSON
    with open("data/valides.json", "r", encoding="utf-8") as f:
        etudiants = json.load(f)

    conn = get_connection()
    if not conn:
        print("❌ Connexion échouée !")
        return

    cur = conn.cursor()
    compteur = 0

    for etudiant in etudiants:
        try:
            # 1. Insérer la classe
            cur.execute("""
                INSERT INTO classes (nom_classe)
                VALUES (%s)
                ON CONFLICT (nom_classe) DO NOTHING
                RETURNING id
            """, (etudiant["classe"],))

            row = cur.fetchone()
            if row:
                id_classe = row[0]
            else:
                cur.execute("SELECT id FROM classes WHERE nom_classe = %s",
                           (etudiant["classe"],))
                id_classe = cur.fetchone()[0]

            # 2. Insérer l'étudiant
            cur.execute("""
                INSERT INTO etudiants
                (code, numero, prenom, nom, date_naissance, id_classe, source)
                VALUES (%s, %s, %s, %s, %s, %s, 'DB')
                ON CONFLICT (numero) DO NOTHING
                RETURNING id
            """, (
                etudiant["code"],
                etudiant["numero"],
                etudiant["prenom"],
                etudiant["nom"],
                etudiant["date_naissance"],
                id_classe
            ))

            row = cur.fetchone()
            if not row:
                continue
            id_etudiant = row[0]

            # 3. Insérer les matières et notes
            for matiere in etudiant["matieres"]:
                # Insérer la matière
                cur.execute("""
                    INSERT INTO matieres (nom_matiere)
                    VALUES (%s)
                    ON CONFLICT (nom_matiere) DO NOTHING
                    RETURNING id
                """, (matiere["matieres"],))

                row = cur.fetchone()
                if row:
                    id_matiere = row[0]
                else:
                    cur.execute("SELECT id FROM matieres WHERE nom_matiere = %s",
                               (matiere["matieres"],))
                    id_matiere = cur.fetchone()[0]

                # Insérer etudiant_matiere
                cur.execute("""
                    INSERT INTO etudiant_matiere
                    (id_etudiant, id_matiere, note_exam, moyenne)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (
                    id_etudiant,
                    id_matiere,
                    matiere.get("examen", 0),
                    matiere.get("moyenne", 0)
                ))
                id_em = cur.fetchone()[0]

                # Insérer les notes de devoir
                for note in matiere.get("notes_dev", []):
                    cur.execute("""
                        INSERT INTO devoirs (id_etudiant_matiere, note)
                        VALUES (%s, %s)
                    """, (id_em, note))

            compteur += 1

        except Exception as e:
            print(f"❌ Erreur pour {etudiant.get('numero')} : {e}")
            conn.rollback()
            continue

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Import terminé ! {compteur} étudiants importés.")

if __name__ == "__main__":
    import_data()
