# dri - Shadow Demand & Microtrend Scanner
**Dark Research Index**

**What it is**

A fully automated micro-SaaS that scrapes and clusters:

product categories rising quietly (not mainstream yet)

keywords with sudden demand spikes

app niches with exponential installs

emerging micro-genres in gaming, media, API markets

**Use Case**

Small studios, solo devs, writers, and micro SaaS builders need early signals before niches explode.

# Market Intelligence Pipeline

A deterministic market signal engine that identifies emerging opportunities and market saturation patterns by analyzing public data sources across gaming, technology, and digital markets.

## What This Pipeline Does

This system automatically collects, processes, and analyzes market signals from multiple free public sources to identify:

- **Under-supplied niches** (high demand, low supply - build opportunities)
- **Over-crowded markets** (high supply, low demand - avoid or differentiate)
- **Balanced markets** (stable conditions)
- **Market divergence trends** (weekly snapshots for analysis)

## Data Sources

### Free Public APIs & Sources
- **Steam/SteamSpy**: Game market supply and tag growth
- **Reddit**: Community attention and discussion velocity  
- **Wikipedia**: Knowledge-seeking and intent signals
- **AI Research Feeds**: Capability diffusion (GitHub, arXiv, HN)
- **itch.io**: Indie experimentation velocity
- **Additional sources**: Easy to extend with new signal collectors

## Key Components

### Signal Collection Pipeline
Python-based ingestion system that:
- Collects data from 6+ free sources
- Normalizes tags across platforms
- Computes deterministic CSI (Composite Signal Index)
- Stores atomic signals in PostgreSQL

### Analytics Engine
PostgreSQL-based analysis with:
- **Tag normalization layer** for cross-source correlation
- **Market divergence views** comparing demand vs supply
- **Weekly snapshot system** for historical analysis
- **Confidence scoring** based on signal volume

### Core Metrics
- **Demand CSI**: Weighted blend of social attention + intent + capability signals
- **Supply CSI**: Market supply pressure from Steam/itch.io
- **Divergence**: Demand CSI - Supply CSI (positive = opportunity, negative = saturation)
- **Confidence Level**: Based on number of confirming signals

## Technical Architecture

### Database Schema
```sql
signals: event_ts, signal_source, tag, velocity, delta, csi, category
tag_alias: source_tag, canonical_tag  
weekly_market_snapshot: snapshot_week, tag, demand_csi, supply_csi, divergence, market_state
