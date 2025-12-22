CREATE OR REPLACE VIEW market_divergence_view AS
WITH last_7d AS (
    SELECT
        COALESCE(a.canonical_tag, s.tag) AS tag,
        s.signal_source,
        AVG(s.csi)      AS avg_csi,
        AVG(s.velocity) AS avg_velocity,
        COUNT(*)        AS signal_count
    FROM signals s
    LEFT JOIN tag_alias a
        ON s.tag = a.source_tag
    WHERE s.event_ts >= NOW() - INTERVAL '7 days'
    GROUP BY COALESCE(a.canonical_tag, s.tag), s.signal_source
),

demand AS (
    SELECT
        tag,
        AVG(avg_csi) AS demand_csi,
        SUM(signal_count) AS demand_signals
    FROM last_7d
    WHERE signal_source IN (
        'reddit_trends',
        'wikipedia_pageviews',
        'ai_signals'
    )
    GROUP BY tag
),

supply AS (
    SELECT
        tag,
        AVG(avg_csi) AS supply_csi,
        SUM(signal_count) AS supply_signals
    FROM last_7d
    WHERE signal_source = 'steam_tag_growth'
    GROUP BY tag
)

SELECT
    d.tag,
    ROUND(d.demand_csi::numeric, 4) AS demand_csi,
    ROUND(s.supply_csi::numeric, 4) AS supply_csi,
    ROUND((d.demand_csi - s.supply_csi)::numeric, 4) AS divergence,
    d.demand_signals,
    s.supply_signals,
    CASE
        WHEN d.demand_csi - s.supply_csi > 0.25 THEN 'UNDER-SUPPLIED'
        WHEN d.demand_csi - s.supply_csi < -0.25 THEN 'OVER-CROWDED'
        ELSE 'BALANCED'
    END AS market_state,
    -- Confidence indicator based on signal count
    CASE
        WHEN d.demand_signals >= 7 AND s.supply_signals >= 3 THEN 'HIGH'
        WHEN d.demand_signals >= 3 AND s.supply_signals >= 1 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS confidence_level
FROM demand d
LEFT JOIN supply s
    ON d.tag = s.tag
WHERE s.supply_csi IS NOT NULL
ORDER BY ABS(d.demand_csi - s.supply_csi) DESC;
