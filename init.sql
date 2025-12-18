-- Initialization script to create dridb and driuser
ALTER USER postgres WITH PASSWORD 'bisquit';

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
