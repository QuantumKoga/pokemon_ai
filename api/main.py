
from fastapi import FastAPI, Query

from .pokemon import search_pokemon, get_pokemon_details
from .moves import search_moves, get_move_details, get_moves_for_pokemon
from .abilities import search_abilities, get_ability_details, get_pokemon_abilities
from .items import search_items, get_item_details
from .rulesets import (
    get_available_regulations,
    get_regulation_details,
    get_regulation_pokemon,
    get_regulation_changes,
    get_regulation_mega_evolutions,
    get_regulation_rules,
    get_regulation_verification,
)
from .meta import (
    get_available_meta_data,
    search_meta_pokemon,
    get_pokemon_meta_overview,
    get_official_ladder_data,
    get_tournament_data,
    get_meta_category,
    get_tournament_sets,
    get_tournament_cores,
)


app = FastAPI(
    title="Pokémon Champions API",
    description=(
        "Read-only API providing Pokémon Champions data, "
        "moves, abilities, items, regulations and metagame information."
    ),
    version="1.0.0",
)


@app.get("/health", operation_id="health_check")
def health_check():
    return {"status": "ok"}


# ============================================================
# POKEMON
# ============================================================

@app.get("/pokemon/search", operation_id="search_pokemon")
def pokemon_search(
    query: str = "",
    pokemon_type: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
):
    return search_pokemon(query, pokemon_type, limit)


@app.get("/pokemon/details", operation_id="get_pokemon_details")
def pokemon_details(name: str):
    return get_pokemon_details(name)


# ============================================================
# MOVES
# ============================================================

@app.get("/moves/search", operation_id="search_moves")
def moves_search(
    query: str = "",
    move_type: str | None = None,
    category: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
):
    return search_moves(query, move_type, category, limit)


@app.get("/moves/details", operation_id="get_move_details")
def move_details(name: str):
    return get_move_details(name)


@app.get("/moves/pokemon", operation_id="get_moves_for_pokemon")
def moves_for_pokemon(
    pokemon_name: str,
    move_type: str | None = None,
    category: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
):
    return get_moves_for_pokemon(
        pokemon_name, move_type, category, limit
    )


# ============================================================
# ABILITIES
# ============================================================

@app.get("/abilities/search", operation_id="search_abilities")
def abilities_search(
    query: str = "",
    limit: int = Query(default=20, ge=1, le=100),
):
    return search_abilities(query, limit)


@app.get("/abilities/details", operation_id="get_ability_details")
def ability_details(name: str):
    return get_ability_details(name)


@app.get("/abilities/pokemon", operation_id="get_pokemon_abilities")
def pokemon_abilities(pokemon_name: str):
    return get_pokemon_abilities(pokemon_name)


# ============================================================
# ITEMS
# ============================================================

@app.get("/items/search", operation_id="search_items")
def items_search(
    query: str = "",
    limit: int = Query(default=20, ge=1, le=100),
):
    return search_items(query, limit)


@app.get("/items/details", operation_id="get_item_details")
def item_details(name: str):
    return get_item_details(name)


# ============================================================
# RULESETS
# ============================================================

@app.get("/rulesets/available", operation_id="get_available_regulations")
def available_regulations():
    return get_available_regulations()


@app.get("/rulesets/details", operation_id="get_regulation_details")
def regulation_details(name: str):
    return get_regulation_details(name)


@app.get("/rulesets/pokemon", operation_id="get_regulation_pokemon")
def regulation_pokemon(
    name: str,
    query: str,
    limit: int = Query(default=100, ge=1, le=500),
):
    return get_regulation_pokemon(name, query, limit)


@app.get("/rulesets/changes", operation_id="get_regulation_changes")
def regulation_changes(name: str):
    return get_regulation_changes(name)


@app.get(
    "/rulesets/mega-evolutions",
    operation_id="get_regulation_mega_evolutions",
)
def regulation_mega_evolutions(
    name: str,
    query: str = "",
    limit: int = Query(default=100, ge=1, le=500),
):
    return get_regulation_mega_evolutions(name, query, limit)


@app.get("/rulesets/rules", operation_id="get_regulation_rules")
def regulation_rules(
    name: str,
    category: str = "",
):
    return get_regulation_rules(name, category)


@app.get(
    "/rulesets/verification",
    operation_id="get_regulation_verification",
)
def regulation_verification(name: str):
    return get_regulation_verification(name)


# ============================================================
# METAGAME
# ============================================================

@app.get("/meta/available", operation_id="get_available_meta_data")
def available_meta_data():
    return get_available_meta_data()


@app.get("/meta/pokemon/search", operation_id="search_meta_pokemon")
def meta_pokemon_search(
    query: str = "",
    limit: int = Query(default=20, ge=1, le=100),
):
    return search_meta_pokemon(query, limit)


@app.get(
    "/meta/pokemon/overview",
    operation_id="get_pokemon_meta_overview",
)
def pokemon_meta_overview(pokemon_name: str):
    return get_pokemon_meta_overview(pokemon_name)


@app.get(
    "/meta/official-ladder",
    operation_id="get_official_ladder_data",
)
def official_ladder_data(
    pokemon_name: str,
    regulation: str,
    format: str,
):
    return get_official_ladder_data(
        pokemon_name, regulation, format
    )


@app.get("/meta/tournaments", operation_id="get_tournament_data")
def tournament_data(
    pokemon_name: str,
    regulation: str = "M-C",
):
    return get_tournament_data(pokemon_name, regulation)


@app.get("/meta/category", operation_id="get_meta_category")
def meta_category(
    pokemon_name: str,
    source: str,
    regulation: str,
    category: str,
    format: str = "",
):
    return get_meta_category(
        pokemon_name, source, regulation, category, format
    )


@app.get("/meta/tournament-sets", operation_id="get_tournament_sets")
def tournament_sets(
    pokemon_name: str,
    regulation: str = "M-C",
):
    return get_tournament_sets(pokemon_name, regulation)


@app.get("/meta/tournament-cores", operation_id="get_tournament_cores")
def tournament_cores(
    pokemon_name: str,
    regulation: str = "M-C",
):
    return get_tournament_cores(pokemon_name, regulation)
