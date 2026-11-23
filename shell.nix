{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = with pkgs; [
    python3
    python3Packages.requests
    python3Packages.beautifulsoup4
    python3Packages.lxml
    python3Packages.tqdm
    # Pokémon AI API
    python3Packages.fastapi
    python3Packages.uvicorn
    python3Packages.pydantic
    python3Packages.httpx
    python3Packages.orjson
  ];
  shellHook = ''
    echo "Pokémon Champions scraper"
    echo "To generate databases run: python generate/run_all.py"
    echo "To enable the API, run: python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload"
  '';
}
