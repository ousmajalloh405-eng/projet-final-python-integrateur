import json
import psycopg2

JSON_FILE = "data/valides.json"
DB_PARAMS = {
    "dbname": "gestion_etudiants_db",
    "user": "phonix"
}

def insert_all_data():
    conn = None
    cursor = None

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            etudiants = json.load(f)
        
        # ÉTAPES DE SÉCURITÉ POUR VOIR CE QUI SE PASSE
        print(f"📋 Type de données lues : {type(etudiants)}")
        print(f"📊 Nombre d'éléments détectés dans le JSON : {len(etudiants)}")

        if len(etudiants) == 0:
            print("⚠️ Attention : Le fichier JSON lu est vide !")
            return

        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        print("🔌 Connexion réussie à PostgreSQL ! Début de l'insertion...")

        ecoles_inserees = set()
        compteur_etudiants = 0

        for etu in etudiants:
            id_ecole = etu.get("code")
            id_eleve = etu.get("numero")
            nom = etu.get("nom")
            prenom = etu.get("prenom")
            classe = etu.get("classe")
            date_naiss = etu.get("date_naissance")

            if not id_eleve:
                continue # Sécurité si la ligne est bizarre

            # Insertion École
            if id_ecole not in ecoles_inserees:
                cursor.execute(
                    """
                    INSERT INTO ecoles (id_ecole, nom_ecole, ville)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id_ecole) DO NOTHING;
                    """,
                    (id_ecole, f"Établissement {id_ecole}", "Dakar")
                )
                ecoles_inserees.add(id_ecole)

            # Insertion Étudiant
            cursor.execute(
                """
                INSERT INTO etudiants (id_eleve, id_ecole, nom, prenom, date_naissance, classe)
                VALUES (%s, %s, %s, %s, TO_DATE(%s, 'DD/MM/YYYY'), %s)
                ON CONFLICT (id_eleve) DO NOTHING;
                """,
                (id_eleve, id_ecole, nom, prenom, date_naiss, classe)
            )
            
            compteur_etudiants += 1

            # Insertion Notes
            for mat in etu.get("matieres", []):
                nom_matiere = mat.get("matieres", "Inconnu")
                notes_dev = mat.get("notes_dev", [])
                examen = mat.get("examen", None)
                moyenne = mat.get("moyenne", None)

                cursor.execute(
                    """
                    INSERT INTO notes (id_eleve, matiere, notes_dev, examen, moyenne)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (id_eleve, nom_matiere, notes_dev, examen, moyenne)
                )

        conn.commit()
        print(f"🚀 Succès ! {compteur_etudiants} étudiants ont été réellement enregistrés.")

    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")
        if conn is not None:
            conn.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    insert_all_data()