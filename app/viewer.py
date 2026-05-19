import json
from pathlib import Path
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


VIEWER_HTML = Path(__file__).parent.parent / "assets" / "viewer.html"


class ProteinViewer(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 500)
        self.load(QUrl.fromLocalFile(str(VIEWER_HTML.resolve())))
        self._pending_pdb = None
        self._pending_style = "cartoon"
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok):
        if ok and self._pending_pdb:
            self._inject_pdb(self._pending_pdb, self._pending_style)
            self._pending_pdb = None

    def load_structure(self, pdb_path: Path, style: str = "cartoon"):
        pdb_data = pdb_path.read_text()
        self._pending_style = style
        if self.url().isEmpty() or not self.url().isValid():
            self._pending_pdb = pdb_data
        else:
            self._inject_pdb(pdb_data, style)

    def _inject_pdb(self, pdb_data: str, style: str):
        escaped = json.dumps(pdb_data)
        self.page().runJavaScript(f"loadPDB({escaped}, {json.dumps(style)});")

    def set_style(self, style: str):
        self.page().runJavaScript(f"applyStyle({json.dumps(style)});")
