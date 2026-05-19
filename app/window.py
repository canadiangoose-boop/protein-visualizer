from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from app.viewer import ProteinViewer
from app.pdb_fetcher import fetch_pdb
from app.structure_info import get_structure_summary


class FetchThread(QThread):
    done = pyqtSignal(Path)
    error = pyqtSignal(str)

    def __init__(self, pdb_id: str):
        super().__init__()
        self.pdb_id = pdb_id

    def run(self):
        try:
            path = fetch_pdb(self.pdb_id)
            self.done.emit(path)
        except Exception as e:
            self.error.emit(str(e))


EXAMPLES = [
    ("— Examples —", ""),
    ("Hemoglobin (1HHO)", "1HHO"),
    ("Insulin (1GZX)", "1GZX"),
    ("TIM Barrel (1TIM)", "1TIM"),
    ("Lysozyme (2LYZ)", "2LYZ"),
    ("DNA Double Helix (1BNA)", "1BNA"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protein Structure Visualizer")
        self.resize(1000, 700)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # --- Controls row ---
        controls = QHBoxLayout()
        self.pdb_input = QLineEdit()
        self.pdb_input.setPlaceholderText("Enter PDB ID (e.g. 1HHO)")
        self.pdb_input.setFixedWidth(180)
        self.pdb_input.returnPressed.connect(self._on_load)

        self.load_btn = QPushButton("Load Structure")
        self.load_btn.clicked.connect(self._on_load)

        examples_label = QLabel("Examples:")
        self.examples_combo = QComboBox()
        self.examples_combo.setFixedWidth(200)
        for label, _ in EXAMPLES:
            self.examples_combo.addItem(label)
        self.examples_combo.currentIndexChanged.connect(self._on_example_selected)

        style_label = QLabel("Style:")
        self.style_combo = QComboBox()
        self.style_combo.addItems(["cartoon", "stick", "sphere", "surface"])
        self.style_combo.currentTextChanged.connect(self._on_style_change)

        controls.addWidget(self.pdb_input)
        controls.addWidget(self.load_btn)
        controls.addSpacing(20)
        controls.addWidget(examples_label)
        controls.addWidget(self.examples_combo)
        controls.addSpacing(20)
        controls.addWidget(style_label)
        controls.addWidget(self.style_combo)
        controls.addStretch()
        layout.addLayout(controls)

        # --- Info bar ---
        self.info_label = QLabel("Enter a PDB ID and click Load Structure.")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.info_label)

        # --- 3D viewer ---
        self.viewer = ProteinViewer()
        layout.addWidget(self.viewer, stretch=1)

        self.setStatusBar(QStatusBar())

    def _on_load(self):
        pdb_id = self.pdb_input.text().strip()
        if not pdb_id:
            return
        self.load_btn.setEnabled(False)
        self.statusBar().showMessage(f"Fetching {pdb_id.upper()}...")
        self._thread = FetchThread(pdb_id)
        self._thread.done.connect(self._on_fetch_done)
        self._thread.error.connect(self._on_fetch_error)
        self._thread.start()

    def _on_fetch_done(self, path: Path):
        self.load_btn.setEnabled(True)
        style = self.style_combo.currentText()
        self.viewer.load_structure(path, style)
        summary = get_structure_summary(path)
        self.info_label.setText(
            f"PDB: {summary['pdb_id']}  |  "
            f"Chains: {summary['chains']} ({', '.join(summary['chain_ids'])})  |  "
            f"Residues: {summary['residues']}  |  "
            f"Atoms: {summary['atoms']}"
        )
        self.statusBar().showMessage("Loaded successfully.", 3000)

    def _on_fetch_error(self, message: str):
        self.load_btn.setEnabled(True)
        self.statusBar().showMessage("Error.")
        QMessageBox.critical(self, "Error", message)

    def _on_example_selected(self, index: int):
        _, pdb_id = EXAMPLES[index]
        if pdb_id:
            self.pdb_input.setText(pdb_id)
            self._on_load()
            self.examples_combo.setCurrentIndex(0)

    def _on_style_change(self, style: str):
        self.viewer.set_style(style)
