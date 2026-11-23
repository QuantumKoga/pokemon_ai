
from copy import deepcopy
from typing import Any

from .database import db


# Categories available in each data source.
LADDER_CATEGORIES = {
    "moves",
    "items",
    "abilities",
    "partners",
    "stat_spreads",
    "natures",
}

TOURNAMENT_CATEGORIES = {
    "metrics",
    "moves",
    "items",
    "abilities",
    "natures",
    "teammates",
    "common_sets",
    "cores",
}

META_SOURCES = {"official_ladder", "tournaments", "showdown"}


def _get_meta_data() -> dict[str, Any]:
    """Load the metagame database."""
    data = db.get("meta")
    if not isinstance(data, dict):
        return {}
    return data


def _get_pokemon_records() -> dict[str, dict[str, Any]]:
    data = _get_meta_data()
    pokemon = data.get("pokemon", [])

    if isinstance(pokemon, dict):
        records = {}

        for key, entry in pokemon.items():
            if not isinstance(entry, dict):
                continue

            name = entry.get("pokemon") or entry.get("name") or key

            if isinstance(name, str) and name.strip():
                records[name] = entry

        return records

    if isinstance(pokemon, list):
        records = {}

        for entry in pokemon:
            if not isinstance(entry, dict):
                continue

            name = entry.get("pokemon") or entry.get("name")

            if isinstance(name, str) and name.strip():
                records[name] = entry

        return records

    return {}


def _find_pokemon(name: str) -> tuple[str, dict[str, Any]] | None:
    """Find a Pokémon by exact name, ignoring letter case."""
    query = name.strip().casefold()

    if not query:
        return None

    records = _get_pokemon_records()

    for pokemon_name, entry in records.items():
        if pokemon_name.casefold() == query:
            return pokemon_name, entry

    return None


def _find_regulation(
    regulations: Any,
    name: str,
) -> tuple[str, dict[str, Any]] | None:
    """Find a regulation by key or common display name."""
    if not isinstance(regulations, dict):
        return None

    query = name.strip().casefold()

    for regulation_name, entry in regulations.items():
        if not isinstance(regulation_name, str):
            continue

        if not isinstance(entry, dict):
            continue

        candidates = {
            regulation_name.casefold(),
            f"regulation {regulation_name}".casefold(),
        }

        display_name = entry.get("name")

        if isinstance(display_name, str):
            candidates.add(display_name.casefold())

        if query in candidates:
            return regulation_name, entry

    return None


def _get_source_regulations(
    pokemon_entry: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    sources = pokemon_entry.get("sources", {})

    if not isinstance(sources, dict):
        return {}

    source_data = sources.get(source, {})

    if not isinstance(source_data, dict):
        return {}

    regulations = source_data.get("regulations", {})

    return regulations if isinstance(regulations, dict) else {}


def _get_ladder_formats(
    regulation_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Return formats from an official ladder regulation.

    Current structure:
        regulation_data["formats"]["Doubles"]

    Also supports the older flat structure where formats were stored
    directly inside regulation_data.
    """
    formats = regulation_data.get("formats")

    if isinstance(formats, dict):
        return formats

    if formats is not None:
        return {}

    return regulation_data


def _find_format(
    formats: dict[str, Any],
    format_name: str,
) -> tuple[str, dict[str, Any]] | None:
    """Find a format by name, ignoring letter case."""
    query = format_name.strip().casefold()

    for name, data in formats.items():
        if (
            isinstance(name, str)
            and name.casefold() == query
            and isinstance(data, dict)
        ):
            return name, data

    return None


def _available_categories(
    data: dict[str, Any],
    known: set[str],
) -> list[str]:
    """List categories that contain data."""
    return sorted(
        category
        for category in known
        if category in data and data[category] is not None
    )


def _not_found(message: str) -> dict[str, Any]:
    return {"error": message}


def get_available_meta_data() -> dict[str, Any]:
    """
    Return general metagame database information.

    Does not return individual Pokémon statistics.
    """
    data = _get_meta_data()
    metadata = data.get("metadata", {})

    if not isinstance(metadata, dict):
        metadata = {}

    records = _get_pokemon_records()

    return {
        "metadata": deepcopy(metadata),
        "pokemon_count": len(records),
        "available_pokemon": sorted(records.keys()),
    }


def search_meta_pokemon(
    query: str = "",
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    Search Pokémon in the metagame database.

    Searches Pokémon names. An empty query returns the first results.
    """
    query = query.strip().casefold()
    max_results = max(1, min(limit, 100))

    results = []

    for name, entry in _get_pokemon_records().items():
        if query and query not in name.casefold():
            continue

        sources = entry.get("sources", {})

        if not isinstance(sources, dict):
            sources = {}

        results.append({
            "name": name,
            "available_sources": sorted(
                source
                for source in META_SOURCES
                if isinstance(sources.get(source), dict)
            ),
        })

        if len(results) >= max_results:
            break

    return results


def get_pokemon_meta_overview(
    pokemon_name: str,
) -> dict[str, Any]:
    """
    Return a short overview of available metagame data for one Pokémon.

    This function does not return detailed moves, items, spreads or metrics.
    """
    result = _find_pokemon(pokemon_name)

    if result is None:
        return _not_found(
            f"Pokémon '{pokemon_name}' was not found in the metagame database."
        )

    name, entry = result

    ladder_regulations = _get_source_regulations(
        entry, "official_ladder"
    )
    tournament_regulations = _get_source_regulations(
        entry, "tournaments"
    )
    showdown_regulations = _get_source_regulations(
        entry, "showdown"
    )

    ladder = []

    for regulation, regulation_data in ladder_regulations.items():
        if not isinstance(regulation_data, dict):
            continue

        formats = _get_ladder_formats(regulation_data)
        available_formats = []

        for format_name, format_data in formats.items():
            if not isinstance(format_data, dict):
                continue

            categories = _available_categories(
                format_data,
                LADDER_CATEGORIES,
            )

            if categories:
                available_formats.append({
                    "format": format_name,
                    "categories": categories,
                })

        if available_formats:
            ladder.append({
                "regulation": regulation,
                "formats": available_formats,
            })

    tournaments = []

    for regulation, tournament_data in tournament_regulations.items():
        if not isinstance(tournament_data, dict):
            continue

        categories = _available_categories(
            tournament_data,
            TOURNAMENT_CATEGORIES,
        )

        if categories:
            tournaments.append({
                "regulation": regulation,
                "format": tournament_data.get("format"),
                "period": tournament_data.get("period"),
                "categories": categories,
            })

    return {
        "pokemon": name,
        "available_data": {
            "official_ladder": ladder,
            "tournaments": tournaments,
            "showdown": sorted(showdown_regulations.keys()),
        },
        "hint": (
            "Use get_official_ladder_data or get_tournament_data "
            "to retrieve detailed data for a specific regulation."
        ),
    }


def get_official_ladder_data(
    pokemon_name: str,
    regulation: str,
    format: str,
) -> dict[str, Any]:
    """
    Return official ladder data for one Pokémon, regulation and format.

    Example:
        get_official_ladder_data("Abomasnow", "M-B", "Doubles")
    """
    result = _find_pokemon(pokemon_name)

    if result is None:
        return _not_found(
            f"Pokémon '{pokemon_name}' was not found in the metagame database."
        )

    name, entry = result

    regulations = _get_source_regulations(
        entry, "official_ladder"
    )

    found = _find_regulation(regulations, regulation)

    if found is None:
        return _not_found(
            f"No official ladder data for {name} in regulation {regulation}."
        )

    regulation_name, regulation_data = found

    formats = _get_ladder_formats(regulation_data)
    found_format = _find_format(formats, format)

    if found_format is None:
        available = [
            key
            for key, value in formats.items()
            if isinstance(value, dict)
        ]

        return _not_found(
            f"No {format} ladder data for {name} in {regulation_name}. "
            f"Available formats: {available}"
        )

    format_name, format_data = found_format

    return {
        "pokemon": name,
        "source": "official_ladder",
        "regulation": regulation_name,
        "format": format_name,
        "data": deepcopy(format_data),
    }


def get_tournament_data(
    pokemon_name: str,
    regulation: str = "M-C",
) -> dict[str, Any]:
    """
    Return tournament data for one Pokémon and regulation.

    Tournament data is separate from official ladder statistics.
    """
    result = _find_pokemon(pokemon_name)

    if result is None:
        return _not_found(
            f"Pokémon '{pokemon_name}' was not found in the metagame database."
        )

    name, entry = result

    regulations = _get_source_regulations(
        entry, "tournaments"
    )

    found = _find_regulation(regulations, regulation)

    if found is None:
        return _not_found(
            f"No tournament data for {name} in regulation {regulation}."
        )

    regulation_name, tournament_data = found

    return {
        "pokemon": name,
        "source": "tournaments",
        "regulation": regulation_name,
        "data": deepcopy(tournament_data),
        "metric_notes": {
            "null_values": "A missing value is not equivalent to zero.",
            "teammates_usage_percent": (
                "Percentage of teams containing this Pokémon that also "
                "contain the listed teammate. It is not global usage."
            ),
        },
    }


def get_meta_category(
    pokemon_name: str,
    source: str,
    regulation: str,
    category: str,
    format: str = "",
) -> dict[str, Any]:
    """
    Retrieve one data category from a selected source.

    Sources:
      - official_ladder
      - tournaments
      - showdown

    Ladder categories:
      moves, items, abilities, partners, stat_spreads, natures

    Tournament categories:
      metrics, moves, items, abilities, natures, teammates,
      common_sets, cores
    """
    source = source.strip().casefold()
    category = category.strip().casefold()

    if source not in META_SOURCES:
        return _not_found(
            f"Unknown source '{source}'. Available sources: "
            f"{sorted(META_SOURCES)}"
        )

    result = _find_pokemon(pokemon_name)

    if result is None:
        return _not_found(
            f"Pokémon '{pokemon_name}' was not found in the metagame database."
        )

    name, entry = result

    regulations = _get_source_regulations(entry, source)
    found = _find_regulation(regulations, regulation)

    if found is None:
        return _not_found(
            f"No {source} data for {name} in regulation {regulation}."
        )

    regulation_name, regulation_data = found

    if source == "official_ladder":
        if category not in LADDER_CATEGORIES:
            return _not_found(
                f"Unknown ladder category '{category}'. "
                f"Available categories: {sorted(LADDER_CATEGORIES)}"
            )

        formats = _get_ladder_formats(regulation_data)
        found_format = _find_format(formats, format)

        if found_format is None:
            available = [
                key
                for key, value in formats.items()
                if isinstance(value, dict)
            ]

            return _not_found(
                f"No {format} data for {name} in {regulation_name}. "
                f"Available formats: {available}"
            )

        format_name, format_data = found_format
        selected_data = format_data.get(category)

    elif source == "tournaments":
        if category not in TOURNAMENT_CATEGORIES:
            return _not_found(
                f"Unknown tournament category '{category}'. "
                f"Available categories: {sorted(TOURNAMENT_CATEGORIES)}"
            )

        selected_data = regulation_data.get(category)
        format_name = None

    else:
        return _not_found(
            "Showdown data is not currently exposed by this tool."
        )

    if selected_data is None:
        return _not_found(
            f"No '{category}' data for {name} in {regulation_name}."
        )

    return {
        "pokemon": name,
        "source": source,
        "regulation": regulation_name,
        "format": format_name,
        "category": category,
        "data": deepcopy(selected_data),
    }


def get_tournament_sets(
    pokemon_name: str,
    regulation: str = "M-C",
) -> dict[str, Any]:
    """Return tournament common sets for one Pokémon."""
    return get_meta_category(
        pokemon_name,
        source="tournaments",
        regulation=regulation,
        category="common_sets",
    )


def get_tournament_cores(
    pokemon_name: str,
    regulation: str = "M-C",
) -> dict[str, Any]:
    """Return tournament cores (pairs and trios) for one Pokémon."""
    return get_meta_category(
        pokemon_name,
        source="tournaments",
        regulation=regulation,
        category="cores",
    )
