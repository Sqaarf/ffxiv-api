# FFXIV API

A Flask REST API that serves Final Fantasy XIV game data scraped from the [FFXIV Console Games Wiki](https://ffxiv.consolegameswiki.com). Currently supports seafood (fishing) and mining node data.

## Setup

**Install dependencies:**

```bash
pip install flask requests beautifulsoup4
```

**Populate the databases:**

```bash
python data.py
```

This scrapes the wiki and writes SQLite databases under `data/`.

**Start the server:**

```bash
flask run
```

## Endpoints

### `GET /api/seafood`

Returns seafood items catchable by fishing.

| Parameter | Type | Description |
|---|---|---|
| `name` | string | Partial match on item name |
| `fishing_method` | string | Exact match (e.g. `Fishing`, `Spearfishing`) |
| `fishing_level` | integer | Exact match on required fishing level |
| `location` | string | Partial match on location name |

**Example:**

```
GET /api/seafood?fishing_method=Spearfishing&fishing_level=80
```

```json
[
  {
    "name": "Gurnard",
    "icon": "https://ffxiv.consolegameswiki.com/...",
    "fishing_method": "Spearfishing",
    "fishing_level": 80,
    "location": "The Tempest",
    "wiki_url": "https://ffxiv.consolegameswiki.com/wiki/Gurnard"
  }
]
```

---

### `GET /api/mining_node`

Returns miner node locations and the items they yield.

| Parameter | Type | Description |
|---|---|---|
| `node_type` | string | Exact match (e.g. `Mineral Deposit`, `Rocky Outcrop`) |
| `mining_level` | integer | Exact match on required mining level |
| `location` | string | Partial match on location name + coordinates |
| `item` | string | Partial match on any item the node yields |

**Example:**

```
GET /api/mining_node?mining_level=90&item=Garlond Steel
```

```json
[
  {
    "node_type": "Mineral Deposit",
    "mining_level": 90,
    "location": "Labyrinthos (X:12, Y:34)",
    "items": "Garlond Steel, Dark Matter Cluster"
  }
]
```

## Data Sources

Data is scraped on demand by running `data.py`. The two sources are:

- **Seafood** — `https://ffxiv.consolegameswiki.com/wiki/Seafood`
- **Mining nodes** — `https://ffxiv.consolegameswiki.com/wiki/Miner_Node_Locations`

To refresh data, run `python data.py` again. The script appends rows, so clear existing data first if needed:

```python
from data import DataManager
dm = DataManager()
dm.clear_table('seafood')
dm.clear_table('mining_node')
dm.migrate('seafood')
dm.migrate('mining_node')
```

## Project Structure

```
ffxiv-api/
├── app.py              # Flask routes
├── data.py             # Scraping + SQLite migration script
├── entities/
│   ├── seafood.py      # SeafoodManager + Seafood model
│   └── mining_node.py  # MiningNodeManager + MiningNode model
├── data/
│   ├── seafood.db
│   └── mining_node.db
└── templates/
    └── index.html
```
