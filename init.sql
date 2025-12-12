-- Initialization script to create signals_db and signals table
ALTER USER postgres WITH PASSWORD 'malena';

CREATE DATABASE signals_db;

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
