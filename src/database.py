import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host"     : "localhost",
    "database" : "gestion_etudiants",
    "user"     : "postgres",
    "password" : "Mot2pass",
    "port"     : "5432"
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return None

def test_connection():
    conn = get_connection()
    if conn:
        print("✅ Connexion à PostgreSQL réussie !")
        conn.close()
    else:
        print("❌ Connexion échouée !")

if __name__ == "__main__":
    test_connection()