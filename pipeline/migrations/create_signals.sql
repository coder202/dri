-- Migration: create signals table
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
