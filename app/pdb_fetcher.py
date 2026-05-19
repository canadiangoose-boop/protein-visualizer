import requests
from pathlib import Path

RCSB_URL = "https://files.rcsb.org/download/{pdb_id}.pdb"
CACHE_DIR = Path(__file__).parent.parent / "cache"


def fetch_pdb(pdb_id: str) -> Path:
    """Download a PDB file by ID and cache it locally. Returns the local path."""
    pdb_id = pdb_id.upper().strip()
    CACHE_DIR.mkdir(exist_ok=True)
    local_path = CACHE_DIR / f"{pdb_id}.pdb"

    if not local_path.exists():
        url = RCSB_URL.format(pdb_id=pdb_id)
        response = requests.get(url, timeout=15)
        if response.status_code == 404:
            raise ValueError(f"PDB ID '{pdb_id}' not found in RCSB.")
        response.raise_for_status()
        local_path.write_text(response.text)

    return local_path
