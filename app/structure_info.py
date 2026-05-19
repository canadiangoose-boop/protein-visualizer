from pathlib import Path
from Bio import PDB
from Bio.PDB.DSSP import dssp_dict_from_pdb_file


def get_structure_summary(pdb_path: Path) -> dict:
    """Return a summary dict with basic structural info from a PDB file."""
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("protein", str(pdb_path))

    chains = list(structure.get_chains())
    residues = [r for r in structure.get_residues() if PDB.is_aa(r)]
    atoms = list(structure.get_atoms())

    return {
        "pdb_id": pdb_path.stem,
        "chains": len(chains),
        "chain_ids": [c.id for c in chains],
        "residues": len(residues),
        "atoms": len(atoms),
    }
