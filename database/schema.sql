

-- TABLE 1 : classes
CREATE TABLE IF NOT EXISTS classes (
    id          SERIAL       PRIMARY KEY,
    nom_classe  VARCHAR(20)  NOT NULL UNIQUE
);

-- TABLE 2 : matieres
CREATE TABLE IF NOT EXISTS matieres (
    id           SERIAL       PRIMARY KEY,
    nom_matiere  VARCHAR(30)  NOT NULL UNIQUE
);

-- TABLE 3 : etudiants
CREATE TABLE IF NOT EXISTS etudiants (
    id               SERIAL       PRIMARY KEY,
    code             VARCHAR(10)  NOT NULL,
    numero           VARCHAR(10)  NOT NULL UNIQUE,
    prenom           VARCHAR(50)  NOT NULL,
    nom              VARCHAR(50)  NOT NULL,
    date_naissance   DATE,
    id_classe        INT          REFERENCES classes(id),
    moyenne_generale FLOAT        DEFAULT 0,
    source           VARCHAR(5)   DEFAULT 'DB',
    is_archived      BOOLEAN      DEFAULT FALSE,
    created_at       TIMESTAMP    DEFAULT NOW()
);

-- TABLE 4 : etudiant_matiere
CREATE TABLE IF NOT EXISTS etudiant_matiere (
    id           SERIAL  PRIMARY KEY,
    id_etudiant  INT     REFERENCES etudiants(id) ON DELETE CASCADE,
    id_matiere   INT     REFERENCES matieres(id),
    note_exam    FLOAT   DEFAULT 0,
    moyenne      FLOAT   DEFAULT 0
);

-- TABLE 5 : devoirs
CREATE TABLE IF NOT EXISTS devoirs (
    id                  SERIAL  PRIMARY KEY,
    id_etudiant_matiere INT     REFERENCES etudiant_matiere(id) ON DELETE CASCADE,
    note                FLOAT   NOT NULL
);

-- INDEX
CREATE INDEX IF NOT EXISTS idx_etudiants_numero  ON etudiants(numero);
CREATE INDEX IF NOT EXISTS idx_etudiants_classe  ON etudiants(id_classe);
CREATE INDEX IF NOT EXISTS idx_etudiants_archive ON etudiants(is_archived);
CREATE INDEX IF NOT EXISTS idx_etudiant_matiere  ON etudiant_matiere(id_etudiant);