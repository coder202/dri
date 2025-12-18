CREATE OR REPLACE VIEW emerging_category_correlation AS
WITH last_7d AS (
    SELECT *
    FROM signals
    WHERE event_ts >= NOW() - INTERVAL '7 days'
),

steam AS (
    SELECT
        tag,
        AVG(csi) AS steam_csi,
        AVG(velocity) AS steam_velocity
    FROM last_7d
    WHERE signal_source = 'steam_spy'
    GROUP BY tag
),

social AS (
    SELECT
        tag,
        AVG(csi) AS social_csi,
        AVG(velocity) AS social_velocity
    FROM last_7d
    WHERE signal_source IN ('reddit_trends')
    GROUP BY tag
)

SELECT
    s.tag,

    s.steam_csi,
    s.steam_velocity,

    COALESCE(so.social_csi, 0) AS social_csi,
    COALESCE(so.social_velocity, 0) AS social_velocity,

    (s.steam_csi - COALESCE(so.social_csi, 0)) AS divergence,

    CASE
        WHEN s.steam_csi >= 0.65 AND so.social_csi >= 0.65
            THEN 'CONFIRMED BREAKOUT'

        WHEN s.steam_csi >= 0.65 AND (so.social_csi < 0.35 OR so.social_csi IS NULL)
            THEN 'STEALTH OPPORTUNITY'

        WHEN s.steam_csi < 0.35 AND so.social_csi >= 0.65
            THEN 'HYPE WITHOUT SUPPLY'

        ELSE 'UNDECIDED'
    END AS regime

FROM steam s
LEFT JOIN social so ON s.tag = so.tag
ORDER BY divergence DESC;
