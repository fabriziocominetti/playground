from pathlib import Path

import pandas as pd
import pytest

from py_epl_results.main import load_data


@pytest.fixture
def tmp_csv_file(tmp_path):
    """Create a temporary CSV file for testing."""
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test_data.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv(p, index=False)
    return p


def test_load_data_success(tmp_csv_file):
    """Test loading data from a valid CSV file."""
    df = load_data(tmp_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df["col1"].to_list() == [1, 2]


def test_load_data_file_not_found():
    """Test loading data from a non-existent file."""
    fake_path = Path("non_existent_file.csv")
    df = load_data(fake_path)
    assert df is None
