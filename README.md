# Protein Structure Visualizer

An interactive desktop application for visualizing 3D protein structures, built as an educational tool for undergraduate students studying biochemistry and structural biology.

## Features

- **Interactive 3D viewer** — rotate, zoom, and pan any protein structure
- **Multiple rendering styles** — Cartoon, Stick, Sphere, and Surface views
- **Live PDB lookup** — enter any PDB ID to fetch structures directly from [RCSB PDB](https://www.rcsb.org/)
- **Built-in examples** — one-click loading of key proteins including Hemoglobin, Insulin, Lysozyme, and more
- **Structure summary** — instant display of chain count, residue count, and atom count

## Demo

| Cartoon (Hemoglobin 1HHO) | Surface view |
|---|---|
| ![Hemoglobin 1HHO](assets/Screenshot%202026-05-19%20at%206.03.07%20PM.png) | |

## Built With

- [PyQt6](https://pypi.org/project/PyQt6/) — desktop GUI framework
- [PyQt6-WebEngine](https://pypi.org/project/PyQt6-WebEngine/) — embedded browser for 3D rendering
- [3Dmol.js](https://3dmol.csb.pitt.edu/) — WebGL-based molecular visualization
- [Biopython](https://biopython.org/) — PDB file parsing and structure analysis
- [RCSB PDB API](https://www.rcsb.org/docs/programmatic-access/web-services-overview) — protein structure database

## Getting Started

### Prerequisites

- Python 3.10+
- pip3

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/protein-visualizer.git
cd protein-visualizer
pip3 install -r requirements.txt
```

### Run

```bash
python3 main.py
```

## Usage

1. Type a PDB ID (e.g. `1HHO`) into the search bar and click **Load Structure**, or
2. Pick a protein from the **Examples** dropdown
3. Switch between rendering styles using the **Style** dropdown

### Example PDB IDs to try

| PDB ID | Protein | Why it's interesting |
|--------|---------|----------------------|
| `1HHO` | Hemoglobin | Classic oxygen-carrier; 4-subunit quaternary structure |
| `1GZX` | Insulin | Small hormone; good intro to disulfide bonds |
| `1TIM` | Triosephosphate isomerase | Textbook TIM-barrel fold |
| `2LYZ` | Lysozyme | Well-studied enzyme; great for surface visualization |
| `1BNA` | DNA double helix | Shows nucleic acid structure for contrast |

## Project Structure

```
protein_visualizer/
├── main.py                 # Entry point
├── requirements.txt
├── app/
│   ├── pdb_fetcher.py      # Downloads & caches PDB files from RCSB
│   ├── structure_info.py   # Parses structural info via Biopython
│   ├── viewer.py           # PyQt6 widget wrapping the 3Dmol.js viewer
│   └── window.py           # Main application window and UI
├── assets/
│   ├── viewer.html         # HTML/JS template for 3D rendering
│   └── 3Dmol-min.js        # Bundled 3Dmol.js (offline support)
└── tests/
    └── test_pdb_fetcher.py
```

## License

MIT
