# Pokémon Champions AI Team Builder

An evolving data collection and knowledge platform designed to help AI systems understand **Pokémon Champions competitive play** and make informed team-building decisions.

The project provides structured Pokémon data, game regulations, battle information and competitive metagame statistics through JSON databases and a read-only REST API. It is designed to serve as a reliable knowledge layer for an AI assistant integrated with tools such as Open WebUI.

The goal is to move beyond a traditional Pokédex: instead of relying on an AI model's general Pokémon knowledge, the system gives it access to structured, game-specific and competitively relevant information.

---

## Table of Contents

- [Project Goals](#project-goals)
- [Current Features](#current-features)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Data Collection and Generation](#data-collection-and-generation)
- [Database Structure](#database-structure)
- [Metagame Data](#metagame-data)
- [REST API](#rest-api)
- [Open WebUI Integration](#open-webui-integration)
- [Installation and Development](#installation-and-development)
- [Running the API](#running-the-api)
- [Configuration](#configuration)
- [Data Quality and Design Principles](#data-quality-and-design-principles)
- [Roadmap](#roadmap)
- [Data Sources](#data-sources)

---

## Project Goals

The main objective is to build a knowledge system that allows an AI assistant to reason about Pokémon Champions competitive battles using actual game data and competitive statistics.

A traditional language model may know Pokémon, moves and abilities, but that does not necessarily mean it understands:

- Which Pokémon are available in a particular regulation.
- Which moves, abilities and items are actually legal.
- How Pokémon are used in the current competitive environment.
- Which teammates commonly appear together.
- Which competitive sets have demonstrated success.
- How game-specific mechanics affect team composition.

This project aims to provide that missing context.

### Long-term vision

The intended AI assistant should eventually be able to:

1. Understand the user's team-building requirements and restrictions.
2. Identify the active regulation and available Pokémon.
3. Analyze competitive usage statistics and tournament trends.
4. Identify useful Pokémon combinations and team cores.
5. Build complete competitive teams with appropriate moves, abilities, items and stat distributions.
6. Evaluate weaknesses, matchups and strategic consistency.
7. Explain its recommendations using actual data and game mechanics.

The project is being developed as a modular knowledge and tooling platform. Data collection, storage, API access and AI integration are kept separate so that each component can evolve independently.

---

## Current Features

The repository currently contains the following implemented components:

| Component | Status | Description |
|---|---|---|
| Pokémon database | Implemented | Pokémon species, forms, types, base stats, abilities and learnable moves |
| Moves database | Implemented | Move properties, categories, effects and Pokémon learnsets |
| Abilities database | Implemented | Ability names and descriptions |
| Items database | Implemented | Held items and descriptions |
| Regulation database | Implemented | Pokémon Champions regulations, restrictions and changes |
| Metagame database | Implemented | Official ladder and tournament statistics |
| Database generators | Implemented | Automated collection and JSON generation |
| REST API | Implemented | Read-only FastAPI service |
| Open WebUI integration | Present | Integration components for AI access to the data |
| Game mechanics documentation | In progress | Structured documentation of battle rules and mechanics |
| Damage calculator | Planned | Dedicated damage calculation engine |
| Team analyzer | Planned | Automated competitive team evaluation |
| AI team builder | Long-term goal | Complete team generation and strategic analysis |

The project is actively developed, and the available data and functionality may change as Pokémon Champions and its competitive environment evolve.

---

## Architecture Overview

The system is divided into four main layers.

```text
                  External Data Sources
                           |
                           v
                Data Collection Scripts
                       generate/
                           |
                           v
                   JSON Databases
                      database/
                           |
                           v
                    FastAPI Backend
                         api/
                           |
                           v
                    Open WebUI / AI
```

### 1. Data Collection

Python scripts retrieve information from external sources, parse it and normalize it into structured JSON files.

### 2. Data Storage

Collected information is stored in separate JSON databases. This keeps the datasets independent and makes them easy to inspect, regenerate and maintain.

### 3. REST API

A FastAPI application exposes the databases through read-only HTTP endpoints.

The API provides structured search and retrieval operations rather than requiring an AI model to inspect raw JSON files.

### 4. AI Integration

Open WebUI can use the API through its integration components to retrieve relevant information while answering questions and assisting with competitive team building.

The API does not generate teams or make strategic decisions itself. Its responsibility is to provide reliable, structured information to the AI layer.

---

## Project Structure

```text
pokemon_ai/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── pokemon.py
│   ├── moves.py
│   ├── abilities.py
│   ├── items.py
│   ├── rulesets.py
│   └── meta.py
│
├── database/
│   ├── pokemon.json
│   ├── moves.json
│   ├── abilities.json
│   ├── items.json
│   ├── rulesets.json
│   └── meta.json
│
├── generate/
│   ├── run_all.py
│   ├── get_pokemon.py
│   ├── get_moves.py
│   ├── get_abilities.py
│   ├── get_items.py
│   ├── get_rulesets.py
│   └── get_metagame.py
│
├── knowledge/
│   └── battle_rules.md
│
├── open_WebUI/
│
├── shell.nix
├── .gitignore
└── README.md
```

### `api/`

Contains the REST API implementation.

- `main.py` — FastAPI application and HTTP endpoint definitions.
- `database.py` — JSON database access, caching and file management.
- `pokemon.py` — Pokémon search and detailed information retrieval.
- `moves.py` — Move search, details and Pokémon learnset queries.
- `abilities.py` — Ability search and Pokémon ability retrieval.
- `items.py` — Item search and details.
- `rulesets.py` — Regulation information, restrictions and verification data.
- `meta.py` — Competitive metagame queries and data retrieval.

### `database/`

Contains the generated JSON databases used by the API.

These files are the primary data layer of the project.

### `generate/`

Contains the scrapers and data-generation scripts.

Each script is responsible for a specific dataset. `run_all.py` executes the generators in sequence.

### `knowledge/`

Contains human-readable documentation about Pokémon Champions mechanics and competitive rules.

This documentation is intended to provide additional context that cannot always be represented effectively through structured database records.

### `open_WebUI/`

Contains components related to integrating the API with Open WebUI, allowing an AI model to retrieve Pokémon and competitive information through dedicated tools.

---

## Data Collection and Generation

The project uses Python scripts to collect information from external sources and convert it into structured JSON databases.

The generators are located in `generate/`.

| Script | Output | Responsibility |
|---|---|---|
| `get_pokemon.py` | `pokemon.json` | Collects Pokémon species, forms, stats, types, abilities and learnable moves |
| `get_moves.py` | `moves.json` | Collects move information and learnset relationships |
| `get_abilities.py` | `abilities.json` | Collects abilities and their descriptions |
| `get_items.py` | `items.json` | Collects available items and descriptions |
| `get_rulesets.py` | `rulesets.json` | Collects regulation information and restrictions |
| `get_metagame.py` | `meta.json` | Collects official ladder and tournament metagame statistics |

### Running all generators

The project includes a script that executes all generators in the correct order:

```bash
python generate/run_all.py
```

The scripts are executed sequentially.

If a generator fails, the process stops and reports the failing script instead of continuing with potentially incomplete data.

### Running individual generators

Each generator can also be executed independently:

```bash
python generate/get_pokemon.py
python generate/get_moves.py
python generate/get_abilities.py
python generate/get_items.py
python generate/get_rulesets.py
python generate/get_metagame.py
```

This is useful when only one dataset needs to be refreshed.

**Important:** Running the generators performs external requests and rewrites the corresponding JSON databases. It is not necessary to run them when only the API code has changed.

---

## Database Structure

The project uses JSON files rather than a traditional relational database.

Each dataset is stored independently, which makes the data easy to inspect and allows individual components to be updated without changing the entire system.

### Pokémon — `pokemon.json`

Contains information about Pokémon available in Pokémon Champions.

Depending on the entry, this includes:

- Pokémon name and form.
- National Pokédex number.
- Typing.
- Base stats.
- Available abilities.
- Learnable moves.

The database distinguishes between different Pokémon forms where relevant.

### Moves — `moves.json`

Contains move information such as:

- Name.
- Type.
- Category.
- Power.
- Accuracy.
- Priority.
- Additional move properties.
- Pokémon that can learn the move.

### Abilities — `abilities.json`

Contains ability names and descriptions.

The API can also retrieve the abilities associated with a Pokémon and its available forms.

### Items — `items.json`

Contains available items and their descriptions.

### Regulations — `rulesets.json`

Contains information about Pokémon Champions competitive regulations, including:

- Regulation name and identifier.
- Current or previous status.
- Start and end dates.
- Selectable Pokémon and forms.
- Mega Evolution availability.
- Regulation changes.
- Restrictions and rules.
- Source information and verification data.

### Metagame — `meta.json`

Contains competitive statistics and usage information collected from different competitive environments.

This database is described in more detail below.

---

## Metagame Data

The metagame database is one of the most important parts of the project.

It allows the AI to understand not only what a Pokémon can do, but also how it is actually used in competitive play.

The database combines information from multiple sources while keeping each source separate.

### Data sources

The current metagame structure supports three source categories:

| Source | Description |
|---|---|
| `official_ladder` | Official Pokémon Champions ladder statistics |
| `tournaments` | Tournament performance and competitive statistics |
| `showdown` | Pokémon Showdown statistics and competitive information |

These sources represent different competitive environments and must not be treated as interchangeable.

For example, official ladder usage does not necessarily reflect tournament success. Similarly, Pokémon Showdown statistics should not automatically be interpreted as Pokémon Champions usage statistics.

### Official ladder

Official ladder data is organized by regulation and battle format.

Supported formats include:

- Doubles
- Singles

Depending on the available source data, the database may contain:

- Pokémon rank.
- Usage statistics.
- Popular moves.
- Popular items.
- Popular abilities.
- Common partners.
- Stat distributions.
- Natures.

Example structure:

```text
pokemon
└── Abomasnow
    └── sources
        └── official_ladder
            └── regulations
                └── M-B
                    └── formats
                        ├── Doubles
                        └── Singles
```

### Tournament statistics

Tournament data focuses on competitive performance rather than general ladder usage.

Depending on the regulation and source availability, it can include:

- Adjusted win rate.
- Popular moves, items and abilities.
- Natures.
- Teammates.
- Common competitive sets.
- Popular team cores.
- Tournament format.
- Data collection period.
- Original source URL.

Tournament statistics are particularly useful for identifying successful combinations and competitive strategies.

### Missing values

Missing values are represented as `null` where appropriate.

A missing statistic must never be interpreted as zero.

For example:

- `percentage: null` means that a percentage is unavailable.
- `percentage: 0` means that a measured percentage is actually zero.

The distinction is important when the AI interprets statistics and compares competitive options.

### Teammate statistics

Teammate percentages must also be interpreted in the context of their source.

For example, a teammate usage percentage may describe the proportion of teams containing a particular Pokémon that also contain another Pokémon.

It does not necessarily represent the global usage percentage of that teammate.

The AI should use the metric definitions and source context rather than assuming that all percentages describe the same thing.

---

## REST API

The project exposes a read-only REST API built with **FastAPI**.

The API provides access to Pokémon information, moves, abilities, items, regulations and competitive metagame data.

### General information

| Property | Value |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn |
| Data storage | JSON files |
| API access | Read-only |
| Default local address | `http://127.0.0.1:8000` |
| OpenAPI documentation | `/docs` |
| Alternative API documentation | `/redoc` |

### Health check

```http
GET /health
```

Returns the API status.

Example:

```json
{
  "status": "ok"
}
```

### Pokémon endpoints

| Endpoint | Parameters | Description |
|---|---|---|
| `GET /pokemon/search` | `query`, `pokemon_type`, `limit` | Search Pokémon by name, form or type |
| `GET /pokemon/details` | `name` | Retrieve detailed Pokémon information |

Example:

```http
GET /pokemon/search?query=garchomp
```

```http
GET /pokemon/details?name=Garchomp
```

### Moves endpoints

| Endpoint | Parameters | Description |
|---|---|---|
| `GET /moves/search` | `query`, `move_type`, `category`, `limit` | Search moves |
| `GET /moves/details` | `name` | Retrieve move details |
| `GET /moves/pokemon` | `pokemon_name`, `move_type`, `category`, `limit` | Retrieve moves learnable by a Pokémon |

Example:

```http
GET /moves/search?move_type=Ground&category=Physical
```

```http
GET /moves/pokemon?pokemon_name=Garchomp
```

### Abilities endpoints

| Endpoint | Parameters | Description |
|---|---|---|
| `GET /abilities/search` | `query`, `limit` | Search abilities |
| `GET /abilities/details` | `name` | Retrieve ability details |
| `GET /abilities/pokemon` | `pokemon_name` | Retrieve abilities available to a Pokémon |

### Items endpoints

| Endpoint | Parameters | Description |
|---|---|---|
| `GET /items/search` | `query`, `limit` | Search items |
| `GET /items/details` | `name` | Retrieve item details |

### Regulation endpoints

| Endpoint | Parameters | Description |
|---|---|---|
| `GET /rulesets/available` | None | List available regulations |
| `GET /rulesets/details` | `name` | Retrieve regulation information |
| `GET /rulesets/pokemon` | `name`, `query`, `limit` | Search selectable Pokémon forms |
| `GET /rulesets/changes` | `name` | Retrieve regulation changes |
| `GET /rulesets/mega-evolutions` | `name`, `query`, `limit` | Search permitted Mega Evolutions |
| `GET /rulesets/rules` | `name`, `category` | Retrieve regulation rules |
| `GET /rulesets/verification` | `name` | Retrieve regulation verification information |

### Metagame endpoints

| Endpoint | Parameters | Description |
|---|---|---|
| `GET /meta/available` | None | Retrieve metagame metadata and available Pokémon |
| `GET /meta/pokemon/search` | `query`, `limit` | Search Pokémon in the metagame database |
| `GET /meta/pokemon/overview` | `pokemon_name` | Retrieve an overview of available metagame information |
| `GET /meta/official-ladder` | `pokemon_name`, `regulation`, `format` | Retrieve official ladder statistics |
| `GET /meta/tournaments` | `pokemon_name`, `regulation` | Retrieve tournament statistics |
| `GET /meta/category` | `pokemon_name`, `source`, `regulation`, `category`, `format` | Retrieve a specific metagame category |
| `GET /meta/tournament-sets` | `pokemon_name`, `regulation` | Retrieve competitive tournament sets |
| `GET /meta/tournament-cores` | `pokemon_name`, `regulation` | Retrieve tournament team cores |

### Example metagame requests

Retrieve available metagame information:

```http
GET /meta/available
```

Search for a Pokémon:

```http
GET /meta/pokemon/search?query=Abomasnow
```

Retrieve a Pokémon's metagame overview:

```http
GET /meta/pokemon/overview?pokemon_name=Abomasnow
```

Retrieve official ladder statistics:

```http
GET /meta/official-ladder?pokemon_name=Abomasnow&regulation=M-B&format=Doubles
```

Retrieve tournament information:

```http
GET /meta/tournaments?pokemon_name=Abomasnow&regulation=M-C
```

Retrieve a specific category:

```http
GET /meta/category?pokemon_name=Abomasnow&source=official_ladder&regulation=M-B&category=moves&format=Doubles
```

Retrieve tournament sets:

```http
GET /meta/tournament-sets?pokemon_name=Abomasnow&regulation=M-C
```

Retrieve tournament cores:

```http
GET /meta/tournament-cores?pokemon_name=Abomasnow&regulation=M-C
```

The API exposes its complete interactive documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## Open WebUI Integration

The API is designed to be consumed by an AI assistant through Open WebUI.

Instead of asking the language model to rely on its internal knowledge, dedicated integration tools allow it to retrieve information directly from the project databases.

This enables more reliable answers to questions such as:

- Which Pokémon are available in the current regulation?
- What moves can Garchomp learn?
- Which abilities are available to a specific Pokémon?
- What are the most common items used by a Pokémon?
- Which Pokémon commonly appear alongside Abomasnow?
- How is a Pokémon performing in official ladder statistics?
- Which sets and team cores have appeared in tournaments?

### Integration architecture

```text
User
 |
 v
Open WebUI
 |
 v
AI Model
 |
 v
Pokémon API Tools
 |
 v
FastAPI
 |
 v
JSON Databases
 |
 v
Structured Results
 |
 v
AI Response
```

The API provides the factual data, while the AI model interprets the information and uses it to answer the user's request.

This separation is intentional: the model should not invent statistics, Pokémon availability or competitive trends when the information can be retrieved from the underlying database.

### Network configuration

When Open WebUI runs inside a separate Docker container, `127.0.0.1` refers to the container itself rather than the host running the API.

The API base URL configured in Open WebUI must therefore be reachable from the Open WebUI container.

---

## Installation and Development

### Requirements

The project uses:

- Python 3
- Nix (for the provided development shell)
- Internet access for data collection
- FastAPI and Uvicorn for the API
- Requests and BeautifulSoup for scraping

The exact Python dependencies are declared in `shell.nix`.

### Clone the repository

```bash
git clone https://github.com/QuantumEspresso/pokemon_ai.git
cd pokemon_ai
```

### Enter the Nix development environment

```bash
nix-shell
```

The development shell provides the required Python packages, including:

- `requests`
- `beautifulsoup4`
- `lxml`
- `tqdm`
- `fastapi`
- `uvicorn`
- `pydantic`
- `httpx`
- `orjson`

The shell also prints useful commands when activated.

---

## Running the API

From the project root, inside the development environment:

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

The API can also be deployed as a systemd service or through another process manager.

For production deployments, use an address and network configuration appropriate for the environment in which the API and its clients run.

---

## Configuration

### Database directory

By default, the API reads JSON databases from:

```text
<project_root>/database/
```

The database directory can be overridden using the environment variable:

```bash
POKEMON_AI_DATABASE_DIR=/path/to/database
```

For example:

```bash
export POKEMON_AI_DATABASE_DIR=/data/pokemon_ai/database
```

This makes it possible to keep the application code and database files in separate locations.

### JSON database caching

The API uses a lightweight read-only JSON database manager implemented in `api/database.py`.

It provides:

- Thread-safe access.
- Lazy loading of database files.
- In-memory caching.
- Automatic cache invalidation when a file's modification time or size changes.
- Manual cache clearing and forced reload support.

The API does not need to parse every JSON file again for every request.

---

## Data Quality and Design Principles

Competitive recommendations are only as reliable as the data behind them.

The project follows several important principles.

### 1. Preserve source separation

Official ladder statistics, tournament statistics and Pokémon Showdown data represent different environments.

They must remain separate and clearly identified.

### 2. Preserve missing values

A missing value must not be silently converted into zero or another assumed value.

`null` means that the information is unavailable or was not provided by the source.

### 3. Preserve regulation context

Competitive restrictions change over time.

Data must be interpreted in the context of its regulation rather than assuming that current rules apply to historical information.

### 4. Keep original source information

Where available, original URLs and source metadata should be retained.

This makes it easier to verify information and investigate discrepancies.

### 5. Separate facts from analysis

The database provides collected information.

Strategic interpretations, matchup assessments and team-building recommendations belong to the analytical AI layer and should be grounded in the available data.

### 6. Avoid assumptions about game mechanics

Pokémon Champions has its own rules and mechanics.

Information from previous Pokémon games should not automatically be applied when it has not been verified for Champions.

The `knowledge/` directory is intended to provide additional game-specific context for the AI.

---

## Roadmap

The project is being developed incrementally.

The following items describe the intended direction, not necessarily functionality already available in the repository.

### Phase 1 — Data and Knowledge Foundations

- [x] Pokémon database generation
- [x] Moves database generation
- [x] Abilities database generation
- [x] Items database generation
- [x] Regulation database generation
- [x] Metagame data collection
- [x] JSON database access layer
- [x] Read-only FastAPI service
- [x] Initial battle rules documentation
- [ ] Expand game mechanics documentation
- [ ] Improve data validation and consistency checks

### Phase 2 — Competitive Knowledge

- [x] Official ladder statistics
- [x] Tournament statistics
- [x] Common moves, items and abilities
- [x] Teammate statistics
- [x] Tournament sets and cores
- [ ] Expand competitive set analysis
- [ ] Develop team archetype information
- [ ] Improve matchup and synergy analysis
- [ ] Expand historical metagame tracking

### Phase 3 — Analytical Tools

- [ ] Damage calculator
- [ ] Stat Points calculator
- [ ] Speed calculator
- [ ] Type coverage analyzer
- [ ] Defensive weakness analyzer
- [ ] Team consistency analyzer
- [ ] Automated team legality validation

### Phase 4 — AI Team Builder

- [ ] Structured team-building workflow
- [ ] Regulation-aware team generation
- [ ] Competitive set recommendations
- [ ] Team synergy and matchup evaluation
- [ ] Automated technical validation
- [ ] Strategic explanations and alternative options

### Long-term goal

The final system should be able to generate complete competitive teams while explaining:

- Why each Pokémon was selected.
- What role it performs.
- Which teammates support it.
- What the team's win conditions are.
- Which opposing strategies may cause problems.
- How the team can respond to important matchups.
- Which alternative Pokémon or sets could improve the composition.

The objective is not simply to generate six Pokémon, but to build a coherent team with a clear strategy.

---

## Data Sources

The project uses external websites and services to collect and validate information.

| Source | Usage |
|---|---|
| [Serebii](https://www.serebii.net/) | Pokémon, moves, abilities and items |
| [Pokémon Champions Battle Data](https://championsbattledata.com/) | Official ladder statistics |
| [INF VGC](https://infovgc.com/) | Tournament statistics and competitive information |
| [ViZukan](https://www.vizukan.app/) | Regulation information |
| [VGC Builder](https://vgc.build/) | Competitive rules and team-building reference |

External sources may change their website structure, data formats or availability.

Consequently, data generators may require maintenance when their upstream sources change.

The project is not affiliated with Nintendo, The Pokémon Company or any of the external data providers.

---

## Disclaimer

Pokémon and Pokémon-related names, characters and assets are trademarks of their respective owners.

This project is an independent fan-made research and development project. It is not an official Pokémon product and is not affiliated with or endorsed by Nintendo, The Pokémon Company or Game Freak.

The collected data is intended for informational, educational and competitive research purposes.

---

**Built to give AI the knowledge it needs to understand competitive Pokémon Champions — not just recognize Pokémon names.**