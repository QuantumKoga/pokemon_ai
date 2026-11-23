# this is Open WebUI tool to use this project's databases via API

import os
import json
import requests
from typing import Optional
from pydantic import Field


class Tools:
    """
    Tools for querying the Pokémon Champions API.

    All game data is retrieved from the local Pokémon Champions API.
    The API and its JSON database remain the single source of truth.
    """

    def __init__(self):
        self.api_url = os.getenv("POKEMON_AI_API_URL", "http://127.0.0.1:8000").rstrip(
            "/"
        )

        self.timeout = 30

    def _get(self, endpoint: str, params: Optional[dict] = None) -> str:
        """Send a GET request to the Pokémon Champions API."""

        try:
            response = requests.get(
                f"{self.api_url}{endpoint}", params=params, timeout=self.timeout
            )
            response.raise_for_status()

            return json.dumps(response.json(), ensure_ascii=False, indent=2)

        except requests.RequestException as e:
            return f"Pokémon API request failed: {str(e)}"

        except ValueError:
            return "Pokémon API returned an invalid JSON response."

    # ---------------------------------------------------------
    # POKEMON
    # ---------------------------------------------------------

    def search_pokemon(
        self,
        query: str = Field(
            "", description="Pokemon name or partial name to search for."
        ),
        pokemon_type: str = Field(
            "", description="Optional Pokemon type filter, e.g. Fire, Water, Electric."
        ),
        limit: int = Field(20, description="Maximum number of results."),
    ) -> str:
        """
        Search for Pokemon in the Pokémon Champions database.
        Use this when looking for Pokemon by name or type.
        """

        return self._get(
            "/pokemon/search",
            {"query": query, "pokemon_type": pokemon_type or None, "limit": limit},
        )

    def get_pokemon_details(
        self,
        name: str = Field(
            ...,
            description="Exact or partial Pokemon name, including form if applicable.",
        ),
    ) -> str:
        """
        Get detailed information about a Pokemon.
        Returns available forms, types, base stats, abilities and other details.
        """

        return self._get("/pokemon/details", {"name": name})

    # ---------------------------------------------------------
    # MOVES
    # ---------------------------------------------------------

    def search_moves(
        self,
        query: str = Field("", description="Move name or partial name."),
        move_type: str = Field(
            "", description="Optional move type, e.g. Fire, Water, Electric."
        ),
        category: str = Field(
            "", description="Optional category: Physical, Special or Status."
        ),
        limit: int = Field(20, description="Maximum number of results."),
    ) -> str:
        """
        Search for moves by name, type or category.
        """

        return self._get(
            "/moves/search",
            {
                "query": query,
                "move_type": move_type or None,
                "category": category or None,
                "limit": limit,
            },
        )

    def get_move_details(
        self, name: str = Field(..., description="Exact move name.")
    ) -> str:
        """
        Get complete details about a move, including its effects and properties.
        """

        return self._get("/moves/details", {"name": name})

    def get_moves_for_pokemon(
        self,
        pokemon_name: str = Field(
            ..., description="Pokemon name, including form if needed."
        ),
        move_type: str = Field("", description="Optional move type filter."),
        category: str = Field(
            "", description="Optional category filter: Physical, Special or Status."
        ),
        limit: int = Field(100, description="Maximum number of moves to return."),
    ) -> str:
        """
        Get moves that a specific Pokemon can learn.
        """

        return self._get(
            "/moves/pokemon",
            {
                "pokemon_name": pokemon_name,
                "move_type": move_type or None,
                "category": category or None,
                "limit": limit,
            },
        )

    # ---------------------------------------------------------
    # ABILITIES
    # ---------------------------------------------------------

    def search_abilities(
        self,
        query: str = Field("", description="Ability name or partial name."),
        limit: int = Field(20, description="Maximum number of results."),
    ) -> str:
        """
        Search for Pokemon abilities.
        """

        return self._get("/abilities/search", {"query": query, "limit": limit})

    def get_ability_details(
        self, name: str = Field(..., description="Exact ability name.")
    ) -> str:
        """
        Get detailed information about an ability.
        """

        return self._get("/abilities/details", {"name": name})

    def get_pokemon_abilities(
        self,
        pokemon_name: str = Field(
            ..., description="Pokemon name, including form if needed."
        ),
    ) -> str:
        """
        Get abilities available to a Pokemon and its matching forms.
        """

        return self._get("/abilities/pokemon", {"pokemon_name": pokemon_name})

    # ---------------------------------------------------------
    # ITEMS
    # ---------------------------------------------------------

    def search_items(
        self,
        query: str = Field("", description="Item name or partial name."),
        limit: int = Field(20, description="Maximum number of results."),
    ) -> str:
        """
        Search for items in the Pokémon Champions database.
        """

        return self._get("/items/search", {"query": query, "limit": limit})

    def get_item_details(
        self, name: str = Field(..., description="Exact item name.")
    ) -> str:
        """
        Get detailed information about an item.
        """

        return self._get("/items/details", {"name": name})

    # ---------------------------------------------------------
    # REGULATIONS
    # ---------------------------------------------------------

    def get_available_regulations(self) -> str:
        """
        List all available Pokémon Champions regulations.
        """

        return self._get("/rulesets/available")

    def get_regulation_details(
        self,
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
    ) -> str:
        """
        Get general details about a regulation.
        """

        return self._get("/rulesets/details", {"regulation": regulation})

    def get_regulation_pokemon(
        self,
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
        query: str = Field("", description="Optional Pokemon name or partial name."),
    ) -> str:
        """
        Search for Pokemon forms available in a specific regulation.
        Returns matching forms individually.
        """

        return self._get(
            "/rulesets/pokemon", {"regulation": regulation, "query": query or None}
        )

    def get_regulation_changes(
        self,
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
    ) -> str:
        """
        Get Pokemon additions and removals compared to the previous regulation.
        """

        return self._get("/rulesets/changes", {"regulation": regulation})

    def get_regulation_mega_evolutions(
        self,
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
    ) -> str:
        """
        Get Mega Evolutions available in a specific regulation.
        """

        return self._get("/rulesets/mega-evolutions", {"regulation": regulation})

    def get_regulation_rules(
        self,
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
    ) -> str:
        """
        Get the rules and restrictions for a regulation.
        """

        return self._get("/rulesets/rules", {"regulation": regulation})

    def get_regulation_verification(
        self,
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
    ) -> str:
        """
        Get data verification information for a regulation.
        """

        return self._get("/rulesets/verification", {"regulation": regulation})

    # ---------------------------------------------------------
    # METAGAME
    # ---------------------------------------------------------

    def get_available_meta_data(self) -> str:
        """
        Get metagame database metadata, available regulations,
        formats, sources and Pokemon count.
        """

        return self._get("/meta/available")

    def search_meta_pokemon(
        self,
        query: str = Field(
            "",
            description="Pokemon name or partial name to search in the metagame database.",
        ),
        limit: int = Field(20, description="Maximum number of Pokemon results."),
    ) -> str:
        """
        Search for Pokemon with available metagame data.
        """

        return self._get("/meta/pokemon/search", {"query": query, "limit": limit})

    def get_pokemon_meta_overview(
        self,
        pokemon_name: str = Field(
            ..., description="Pokemon name as stored in the metagame database."
        ),
    ) -> str:
        """
        Get an overview of available metagame data for a Pokemon.
        Shows available sources, regulations, formats and categories.
        """

        return self._get("/meta/pokemon/overview", {"pokemon_name": pokemon_name})

    def get_official_ladder_data(
        self,
        pokemon_name: str = Field(..., description="Pokemon name."),
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
        format: str = Field(..., description="Battle format: Doubles or Singles."),
    ) -> str:
        """
        Get official ladder data for a Pokemon, regulation and format.
        Includes ranking and usage categories.
        This is NOT the tournament win rate source.
        """

        return self._get(
            "/meta/official-ladder",
            {"pokemon_name": pokemon_name, "regulation": regulation, "format": format},
        )

    def get_tournament_data(
        self,
        pokemon_name: str = Field(..., description="Pokemon name."),
        regulation: str = Field(
            "M-C", description="Tournament regulation, currently M-C."
        ),
    ) -> str:
        """
        Get tournament statistics for a Pokemon.

        IMPORTANT:
        Tournament metrics include adjusted_win_rate, games,
        teams, usage_percent, usage_rank and top_8_index.

        Use this tool when the user asks about tournament win rate.
        """

        return self._get(
            "/meta/tournaments",
            {"pokemon_name": pokemon_name, "regulation": regulation},
        )

    def get_meta_category(
        self,
        pokemon_name: str = Field(..., description="Pokemon name."),
        source: str = Field(
            ..., description="Data source: tournaments, official_ladder or showdown."
        ),
        regulation: str = Field(
            ..., description="Regulation identifier, e.g. M-A, M-B or M-C."
        ),
        category: str = Field(
            ...,
            description="Category: metrics, moves, items, abilities, natures, teammates, common_sets or cores.",
        ),
        format: str = Field(
            "",
            description="Required for official_ladder: Doubles or Singles. Leave empty for tournaments.",
        ),
    ) -> str:
        """
        Retrieve a specific metagame data category.

        For tournament win rate use:
        source='tournaments', category='metrics'.

        For official ladder data use:
        source='official_ladder' and specify format.
        """

        return self._get(
            "/meta/category",
            {
                "pokemon_name": pokemon_name,
                "source": source,
                "regulation": regulation,
                "category": category,
                "format": format or None,
            },
        )

    def get_tournament_sets(
        self,
        pokemon_name: str = Field(..., description="Pokemon name."),
        regulation: str = Field(
            "M-C", description="Tournament regulation, currently M-C."
        ),
    ) -> str:
        """
        Get common tournament sets for a Pokemon.
        """

        return self._get(
            "/meta/tournament-sets",
            {"pokemon_name": pokemon_name, "regulation": regulation},
        )

    def get_tournament_cores(
        self,
        pokemon_name: str = Field(..., description="Pokemon name."),
        regulation: str = Field(
            "M-C", description="Tournament regulation, currently M-C."
        ),
    ) -> str:
        """
        Get tournament team cores for a Pokemon.
        """

        return self._get(
            "/meta/tournament-cores",
            {"pokemon_name": pokemon_name, "regulation": regulation},
        )
