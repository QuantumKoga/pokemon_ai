"""
title: Pokémon Champions API
description: Search Pokémon Champions data, moves, abilities, items, regulations and metagame statistics.
"""

import json
import requests
from typing import Optional
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        API_BASE_URL: str = Field(
            default="http://127.0.0.1:8000",
            description="Base URL of the Pokémon Champions API, reachable from Open WebUI.",
        )
        REQUEST_TIMEOUT: int = Field(
            default=30, description="HTTP request timeout in seconds."
        )

    def __init__(self):
        self.valves = self.Valves()

    def _get(self, endpoint: str, params: Optional[dict] = None) -> str:
        """Send a GET request to the Pokémon Champions API."""
        base_url = self.valves.API_BASE_URL.rstrip("/")
        url = f"{base_url}{endpoint}"

        clean_params = {
            key: value for key, value in (params or {}).items() if value is not None
        }

        try:
            response = requests.get(
                url, params=clean_params, timeout=self.valves.REQUEST_TIMEOUT
            )
            response.raise_for_status()

            try:
                return json.dumps(response.json(), ensure_ascii=False, indent=2)
            except ValueError:
                return response.text

        except requests.HTTPError as exc:
            try:
                details = exc.response.json()
            except Exception:
                details = exc.response.text if exc.response is not None else str(exc)

            return json.dumps(
                {
                    "error": "HTTP request failed",
                    "status_code": (
                        exc.response.status_code if exc.response is not None else None
                    ),
                    "details": details,
                },
                ensure_ascii=False,
                indent=2,
            )

        except requests.RequestException as exc:
            return json.dumps(
                {"error": "API connection failed", "details": str(exc)},
                ensure_ascii=False,
                indent=2,
            )

    # ---------------------------------------------------------
    # POKÉMON
    # ---------------------------------------------------------

    def search_pokemon(
        self, query: str = "", pokemon_type: Optional[str] = None, limit: int = 20
    ) -> str:
        """
        Search Pokémon by name, form or type.
        Returns matching Pokémon forms from the Pokémon database.
        """
        return self._get(
            "/pokemon/search",
            {"query": query, "pokemon_type": pokemon_type, "limit": limit},
        )

    def get_pokemon_details(self, name: str) -> str:
        """Get detailed information about a Pokémon or a specific form."""
        return self._get("/pokemon/details", {"name": name})

    # ---------------------------------------------------------
    # MOVES
    # ---------------------------------------------------------

    def search_moves(
        self,
        query: str = "",
        move_type: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """Search moves by name, type or category."""
        return self._get(
            "/moves/search",
            {
                "query": query,
                "move_type": move_type,
                "category": category,
                "limit": limit,
            },
        )

    def get_move_details(self, name: str) -> str:
        """Get full details for a move."""
        return self._get("/moves/details", {"name": name})

    def get_moves_for_pokemon(
        self,
        pokemon_name: str,
        move_type: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100,
    ) -> str:
        """Get moves that a Pokémon can learn."""
        return self._get(
            "/moves/pokemon",
            {
                "pokemon_name": pokemon_name,
                "move_type": move_type,
                "category": category,
                "limit": limit,
            },
        )

    # ---------------------------------------------------------
    # ABILITIES
    # ---------------------------------------------------------

    def search_abilities(self, query: str = "", limit: int = 20) -> str:
        """Search Pokémon abilities."""
        return self._get("/abilities/search", {"query": query, "limit": limit})

    def get_ability_details(self, name: str) -> str:
        """Get details and description for an ability."""
        return self._get("/abilities/details", {"name": name})

    def get_pokemon_abilities(self, pokemon_name: str) -> str:
        """Get abilities for all matching forms of a Pokémon."""
        return self._get("/abilities/pokemon", {"pokemon_name": pokemon_name})

    # ---------------------------------------------------------
    # ITEMS
    # ---------------------------------------------------------

    def search_items(self, query: str = "", limit: int = 20) -> str:
        """Search Pokémon items."""
        return self._get("/items/search", {"query": query, "limit": limit})

    def get_item_details(self, name: str) -> str:
        """Get details and description for an item."""
        return self._get("/items/details", {"name": name})

    # ---------------------------------------------------------
    # REGULATIONS
    # ---------------------------------------------------------

    def get_available_regulations(self) -> str:
        """List all regulations available in the API."""
        return self._get("/rulesets/available")

    def get_regulation_details(self, regulation: str) -> str:
        """Get general details for a regulation such as M-A, M-B or M-C."""
        return self._get("/rulesets/details", {"name": regulation})

    def get_regulation_pokemon(
        self, regulation: str, query: str = "", limit: int = 100
    ) -> str:
        """Search Pokémon and forms available in a regulation."""
        return self._get(
            "/rulesets/pokemon", {"name": regulation, "query": query, "limit": limit}
        )

    def get_regulation_changes(self, regulation: str) -> str:
        """Get Pokémon and rule changes from the previous regulation."""
        return self._get("/rulesets/changes", {"name": regulation})

    def get_regulation_mega_evolutions(
        self, regulation: str, query: Optional[str] = None, limit: int = 100
    ) -> str:
        """Get Mega Evolutions available in a regulation."""
        return self._get(
            "/rulesets/mega-evolutions",
            {"name": regulation, "query": query, "limit": limit},
        )

    def get_regulation_rules(
        self, regulation: str, category: Optional[str] = None
    ) -> str:
        """Get rules for a regulation, optionally filtered by category."""
        return self._get("/rulesets/rules", {"name": regulation, "category": category})

    def get_regulation_verification(self, regulation: str) -> str:
        """Get verification information for a regulation."""
        return self._get("/rulesets/verification", {"name": regulation})

    # ---------------------------------------------------------
    # METAGAME
    # ---------------------------------------------------------

    def get_available_meta_data(self) -> str:
        """
        Get metagame metadata and available Pokémon record names.

        The database stores Pokémon records in a top-level list.
        Each record uses the 'pokemon' field for its Pokémon name.
        """
        return self._get("/meta/available")

    def search_meta_pokemon(self, query: str = "", limit: int = 20) -> str:
        """
        Search Pokémon that have metagame records.

        Search the available records if the exact database name is uncertain.
        """
        return self._get("/meta/pokemon/search", {"query": query, "limit": limit})

    def get_pokemon_meta_overview(self, pokemon_name: str) -> str:
        """
        Get the available metagame sources and categories for a Pokémon.

        Metagame records are keyed by the Pokémon name stored in the
        record's 'pokemon' field. The source data is nested under 'sources'.
        """
        return self._get("/meta/pokemon/overview", {"pokemon_name": pokemon_name})

    def get_official_ladder_data(
        self, pokemon_name: str, regulation: str = "M-C", format: str = "Doubles"
    ) -> str:
        """
        Get official ladder data for a Pokémon, regulation and format.

        This is official ladder data, not tournament data.
        """
        return self._get(
            "/meta/official-ladder",
            {"pokemon_name": pokemon_name, "regulation": regulation, "format": format},
        )

    def get_tournament_data(self, pokemon_name: str, regulation: str = "M-C") -> str:
        """
        Get tournament data for a Pokémon and regulation.

        Tournament statistics are separate from official ladder statistics.
        If adjusted_win_rate is present, use that field for tournament
        adjusted win rate. Do not substitute another metric.
        """
        return self._get(
            "/meta/tournaments",
            {"pokemon_name": pokemon_name, "regulation": regulation},
        )

    def get_meta_category(
        self,
        pokemon_name: str,
        source: str,
        regulation: str,
        category: str,
        format: str = "",
    ) -> str:
        """
        Get one metagame category from a selected source.

        source should be official_ladder, tournaments or showdown.
        For official_ladder, format is usually Doubles or Singles.
        """
        return self._get(
            "/meta/category",
            {
                "pokemon_name": pokemon_name,
                "source": source,
                "regulation": regulation,
                "category": category,
                "format": format,
            },
        )

    def get_tournament_sets(self, pokemon_name: str, regulation: str = "M-C") -> str:
        """Get common tournament sets for a Pokémon."""
        return self._get(
            "/meta/tournament-sets",
            {"pokemon_name": pokemon_name, "regulation": regulation},
        )

    def get_tournament_cores(self, pokemon_name: str, regulation: str = "M-C") -> str:
        """Get tournament cores associated with a Pokémon."""
        return self._get(
            "/meta/tournament-cores",
            {"pokemon_name": pokemon_name, "regulation": regulation},
        )
