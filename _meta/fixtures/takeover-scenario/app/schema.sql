-- Schema as deployed. See models.py for the objects the code expects.
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    email       TEXT NOT NULL,
    plan        TEXT NOT NULL DEFAULT 'free',
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE reports (
    id          SERIAL PRIMARY KEY,
    payload     TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);
