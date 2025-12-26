# dri - Shadow Demand & Microtrend Scanner
**Dark Research Index - Prototype**

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


THIS SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. THERE IS NO SUPPORT WHATSOEVER.
