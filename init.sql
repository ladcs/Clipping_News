-- =========================
-- EXTENSÕES
-- =========================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- TABELA: news_sources
-- =========================
CREATE TABLE news_sources (
    id SERIAL PRIMARY KEY,
    label TEXT NOT NULL UNIQUE,
    source_link TEXT NOT NULL UNIQUE,
    is_scratch BOOLEAN NOT NULL,
    need_summary BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- =========================
-- TABELA: news
-- =========================
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    source_id INT NOT NULL REFERENCES news_sources(id),
    title TEXT NOT NULL,
    link TEXT,
    summary TEXT NOT NULL,
    content TEXT,
    about TEXT,
    datetime TIMESTAMP,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_news_source_id ON news(source_id);
CREATE INDEX idx_news_datetime ON news(datetime);

-- =========================
-- TABELA: actives
-- =========================
CREATE TABLE actives (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    is_cripto BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX idx_actives_name ON actives(name);

-- =========================
-- TABELA: changes
-- =========================
CREATE TABLE changes (
    id SERIAL PRIMARY KEY,
    active_id INT NOT NULL REFERENCES actives(id),
    active_value FLOAT NOT NULL,
    active_value_prev FLOAT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_changes_active_id ON changes(active_id);

-- =========================
-- TABELA: change_reasons
-- =========================
CREATE TABLE change_reasons (
    id SERIAL PRIMARY KEY,
    active_id INT REFERENCES actives(id),
    change_id INT REFERENCES changes(id),
    news_id INT REFERENCES news(id),
    label TEXT,
    porcent FLOAT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_change_reasons_active_id ON change_reasons(active_id);
CREATE INDEX idx_change_reasons_change_id ON change_reasons(change_id);
CREATE INDEX idx_change_reasons_news_id ON change_reasons(news_id);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW IS DISTINCT FROM OLD THEN
        NEW.updated_at = now();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_news_sources_updated_at
BEFORE UPDATE ON news_sources
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_news_updated_at
BEFORE UPDATE ON news
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_actives_updated_at
BEFORE UPDATE ON actives
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_changes_updated_at
BEFORE UPDATE ON changes
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_change_reasons_updated_at
BEFORE UPDATE ON change_reasons
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE VIEW news_active AS
SELECT *
FROM news
WHERE deleted_at IS NULL;

CREATE VIEW news_sources_active AS
SELECT *
FROM news_sources
WHERE deleted_at IS NULL;

CREATE VIEW actives_active AS
SELECT *
FROM actives
WHERE deleted_at IS NULL;

CREATE VIEW changes_active AS
SELECT *
FROM changes
WHERE deleted_at IS NULL;

CREATE VIEW change_reasons_active AS
SELECT *
FROM change_reasons
WHERE deleted_at IS NULL;
