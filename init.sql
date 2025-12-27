-- Initialization script to create dridb and driuser
ALTER USER postgres WITH PASSWORD 'biscuit';

CREATE USER driuser WITH PASSWORD 'dripass';

CREATE DATABASE signals_db OWNER driuser;

\connect signals_db

CREATE TABLE IF NOT EXISTS signals (
  id SERIAL PRIMARY KEY,
  event_ts TIMESTAMP NOT NULL,
  signal_source TEXT,
  tag TEXT,
  velocity REAL,
  delta REAL,
  CSI REAL,
  category TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

GRANT ALL PRIVILEGES ON TABLE signals TO driuser;
GRANT ALL PRIVILEGES ON SEQUENCE signals_id_seq TO driuser;

-- Create tag_alias table for tag normalization
CREATE TABLE IF NOT EXISTS tag_alias (
  source_tag VARCHAR(255) PRIMARY KEY,
  canonical_tag VARCHAR(255) NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE tag_alias TO driuser;

-- Insert common tag aliases
INSERT INTO tag_alias (source_tag, canonical_tag) VALUES
('deck-building', 'deckbuilder'),
('rogue-like', 'roguelike'),
('auto battler', 'autobattler'),
('survivor-like', 'survivor-like'),
('4x', '4x-strategy')
ON CONFLICT (source_tag) DO NOTHING;
