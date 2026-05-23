
-- ============================================================
-- PROJET : Gestion des Étudiants
-- AUTEURE : Ndeye Penda Sarr
-- BASE    : PostgreSQL
-- JOUR    : 1 — Modélisation SQL
-- ============================================================

-- TABLE 1 : ecoles
CREATE TABLE IF NOT EXISTS ecoles (
    id_ecole    VARCHAR(10)  PRIMARY KEY,
    nom_ecole   VARCHAR(100) NOT NULL,
    ville       VARCHAR(50)  DEFAULT 'Dakar'
);

-- TABLE 2 : etudiants
CREATE TABLE IF NOT EXISTS etudiants (
    id_eleve        VARCHAR(10)  PRIMARY KEY,
    id_ecole        VARCHAR(10)  REFERENCES ecoles(id_ecole),
    nom             VARCHAR(50)  NOT NULL,
    prenom          VARCHAR(50)  NOT NULL,
    date_naissance  DATE,
    classe          VARCHAR(10)  NOT NULL,
    created_at      TIMESTAMP    DEFAULT NOW()
);

-- TABLE 3 : notes
CREATE TABLE IF NOT EXISTS notes (
    id              SERIAL       PRIMARY KEY,
    id_eleve        VARCHAR(10)  REFERENCES etudiants(id_eleve) ON DELETE CASCADE,
    matiere         VARCHAR(30)  NOT NULL,
    notes_dev       FLOAT[],
    examen          FLOAT,
    moyenne         FLOAT,
    created_at      TIMESTAMP    DEFAULT NOW()
);

-- INDEX
CREATE INDEX IF NOT EXISTS idx_etudiants_classe  ON etudiants(classe);
CREATE INDEX IF NOT EXISTS idx_etudiants_ecole   ON etudiants(id_ecole);
CREATE INDEX IF NOT EXISTS idx_notes_eleve       ON notes(id_eleve);
CREATE INDEX IF NOT EXISTS idx_notes_matiere     ON notes(matiere);