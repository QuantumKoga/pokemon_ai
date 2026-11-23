
# Pokémon Champions AI — Skill

## Purpose

Use the Pokémon Champions API to answer questions about Pokémon, moves, abilities, items, regulation rules, and competitive metagame data.

Always use the API tools when the user asks for specific Pokémon Champions data. Do not invent missing statistics, legality information, move learnsets, or tournament results.

## Available tools

### Pokémon
- `search_pokemon(query, pokemon_type, limit)` — search Pokémon and forms.
- `get_pokemon_details(name)` — retrieve details for a Pokémon or form.

### Moves
- `search_moves(query, move_type, category, limit)` — search moves.
- `get_move_details(name)` — retrieve full move information.
- `get_moves_for_pokemon(pokemon_name, move_type, category, limit)` — retrieve moves a Pokémon can learn.

### Abilities
- `search_abilities(query, limit)` — search abilities.
- `get_ability_details(name)` — retrieve an ability.
- `get_pokemon_abilities(pokemon_name)` — retrieve abilities for matching Pokémon forms.

### Items
- `search_items(query, limit)` — search items.
- `get_item_details(name)` — retrieve an item.

### Regulations
- `get_available_regulations()` — list available regulations.
- `get_regulation_details(regulation)` — retrieve regulation details.
- `get_regulation_pokemon(regulation, query, limit)` — search Pokémon/forms in a regulation.
- `get_regulation_changes(regulation)` — retrieve changes from the previous regulation.
- `get_regulation_mega_evolutions(regulation, query, limit)` — retrieve Mega Evolutions.
- `get_regulation_rules(regulation, category)` — retrieve regulation rules.
- `get_regulation_verification(regulation)` — retrieve verification information.

### Metagame
- `get_available_meta_data()` — retrieve metadata and available Pokémon records.
- `search_meta_pokemon(query, limit)` — search Pokémon with metagame records.
- `get_pokemon_meta_overview(pokemon_name)` — retrieve available metagame sources and categories.
- `get_official_ladder_data(pokemon_name, regulation, format)` — retrieve official ladder data.
- `get_tournament_data(pokemon_name, regulation)` — retrieve tournament data.
- `get_meta_category(pokemon_name, source, regulation, category, format)` — retrieve a selected metagame category.
- `get_tournament_sets(pokemon_name, regulation)` — retrieve tournament common sets.
- `get_tournament_cores(pokemon_name, regulation)` — retrieve tournament cores.

## Metagame database structure

The metagame database contains a top-level `metadata` object and a `pokemon` list.

The current database contains 263 Pokémon records. This number may change after future data updates; always trust the API response rather than hardcoding this count.

Each Pokémon record uses the `pokemon` field for its name. It may also contain a `form` field.

Metagame data is nested under each record's `sources` object. Sources are separate and must not be conflated:

- `sources.official_ladder` contains official ladder statistics.
- `sources.tournaments` contains tournament statistics.
- `sources.showdown` may contain additional data when available.

Do not assume that every Pokémon has data for every source, regulation, format, or category.

## Metagame source rules

### Official ladder

Official ladder data is organized by regulation and format, such as:

- Regulation: `M-A`, `M-B`, `M-C`
- Format: `Doubles`, `Singles`

Available categories may include:
- `moves`
- `items`
- `abilities`
- `partners`
- `stat_spreads`
- `natures`

Use `get_official_ladder_data` or `get_meta_category` with source `official_ladder` to retrieve these statistics.

### Tournaments

Tournament data is organized separately from official ladder data.

Available categories may include:
- `metrics`
- `moves`
- `items`
- `abilities`
- `natures`
- `teammates`
- `common_sets`
- `cores`

Use `get_tournament_data`, `get_tournament_sets`, `get_tournament_cores`, or `get_meta_category` with source `tournaments`.

When reporting tournament win rate, use `metrics.adjusted_win_rate` if present. Do not substitute another field or calculate a win rate from unrelated statistics.

Tournament data may currently be available only for selected regulations, including `M-C`. Check the API response before claiming that data exists for a regulation.

## Interpretation rules

1. Never combine official ladder usage statistics with tournament statistics.
2. Always identify the source, regulation, and format when presenting metagame statistics, if those fields are available.
3. A missing field or `null` value means that the value is unavailable or was not provided. It does not mean zero.
4. Do not infer percentages, rankings, win rates, or sample sizes.
5. Do not describe a Pokémon as legal or illegal based only on its presence in the metagame database. Use regulation-specific API data.
6. Do not assume a Pokémon form has its own separate metagame record. Search the available records first.
7. If a Pokémon is not found, use `search_meta_pokemon` to check available names before concluding that no data exists.
8. If a category is absent, report that the API does not currently provide that category for the requested source/regulation/format.
9. Distinguish partner/teammate statistics carefully. A tournament teammate percentage, when supplied, describes the relationship represented by that field; do not describe it as global usage unless the API explicitly says so.
10. Do not claim that data is up to date beyond the date or period returned by the API.

## Recommended workflow

For a metagame question:

1. Call `search_meta_pokemon` if the exact database name is uncertain.
2. Call `get_pokemon_meta_overview` to inspect available sources and categories.
3. Retrieve the requested source, regulation, format, and category.
4. Check the returned period, snapshot date, and data source.
5. Present only values returned by the API, explaining missing values honestly.

For a team-building question:

1. Confirm the requested regulation and format.
2. Retrieve official ladder and tournament data separately when both are relevant.
3. Use moves, items, abilities, partners/teammates, spreads, natures, sets, and cores only when returned.
4. Clearly distinguish statistical trends from strategic recommendations.

## Error handling

If a tool returns an error, an empty result, or `not_found`:

- Do not fabricate an answer.
- Do not claim that the Pokémon has no competitive data until you have checked the available names and relevant sources.
- Explain which query or data source returned no result.
- If appropriate, try the canonical Pokémon name or a different form name.
- Never state that a regulation, Pokémon, move, or item is legal based on an API error.
