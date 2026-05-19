import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from app.pdb_fetcher import fetch_pdb


def test_fetch_pdb_caches_file(tmp_path, monkeypatch):
    monkeypatch.setattr("app.pdb_fetcher.CACHE_DIR", tmp_path)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "ATOM      1  N   ALA A   1"

    with patch("app.pdb_fetcher.requests.get", return_value=mock_response):
        result = fetch_pdb("1abc")
        assert result.exists()
        assert result.name == "1ABC.pdb"


def test_fetch_pdb_raises_on_404(tmp_path, monkeypatch):
    monkeypatch.setattr("app.pdb_fetcher.CACHE_DIR", tmp_path)
    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("app.pdb_fetcher.requests.get", return_value=mock_response):
        with pytest.raises(ValueError, match="not found"):
            fetch_pdb("XXXX")
