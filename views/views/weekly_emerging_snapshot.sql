CREATE TABLE IF NOT EXISTS weekly_emerging_snapshot (
    id BIGSERIAL PRIMARY KEY,

    snapshot_week DATE NOT NULL,           -- ISO week start (Monday)
    tag VARCHAR(150) NOT NULL,

    steam_csi DECIMAL(6,4) NOT NULL,
    steam_velocity DECIMAL(6,4) NOT NULL,

    social_csi DECIMAL(6,4) NOT NULL,
    social_velocity DECIMAL(6,4) NOT NULL,

    divergence DECIMAL(6,4) NOT NULL,
    regime VARCHAR(40) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE (snapshot_week, tag)
);

CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_week ON weekly_emerging_snapshot(snapshot_week);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_tag ON weekly_emerging_snapshot(tag);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_regime ON weekly_emerging_snapshot(regime);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_csi ON weekly_emerging_snapshot(steam_csi, social_csi);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_divergence ON weekly_emerging_snapshot(divergence);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_created_at ON weekly_emerging_snapshot(created_at);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_steam_csi ON weekly_emerging_snapshot(steam_csi);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_social_csi ON weekly_emerging_snapshot(social_csi);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_steam_velocity ON weekly_emerging_snapshot(steam_velocity);
CREATE INDEX IF NOT EXISTS idx_weekly_emerging_snapshot_social_velocity ON weekly_emerging_snapshot(social_velocity);

-- Insert or update weekly snapshot data
INSERT INTO weekly_emerging_snapshot (
    snapshot_week,
    tag,
    steam_csi,
    steam_velocity,
    social_csi,
    social_velocity,
    divergence,
    regime
)
SELECT 
    date_trunc('week', CURRENT_DATE)::DATE as snapshot_week,
    tag,
    steam_csi / 100.0,
    steam_velocity / 100.0,
    social_csi / 100.0,
    social_velocity / 100.0,
    divergence / 100.0,
    regime
FROM emerging_category_correlation
ON CONFLICT (snapshot_week, tag) 
DO UPDATE SET
    steam_csi = EXCLUDED.steam_csi,
    steam_velocity = EXCLUDED.steam_velocity,
    social_csi = EXCLUDED.social_csi,
    social_velocity = EXCLUDED.social_velocity,
    divergence = EXCLUDED.divergence,
    regime = EXCLUDED.regime,
    created_at = NOW();
