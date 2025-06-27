import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(".")
sys.path.append("..")

from oaim_client import OAIPMHClient, get_arg_parser, main


@pytest.fixture
def mock_scythe():
    with patch("oaim_client.Scythe") as mock:
        yield mock


@pytest.fixture
def mock_etree_tostring():
    with patch("oaim_client.etree.tostring", return_value="<xml>data</xml>") as mock:
        yield mock


def test_fetch_data_from_scythe_calls_func(mock_scythe):
    mock_func = MagicMock(return_value="result")
    mock_instance = mock_scythe.return_value.__enter__.return_value
    result = OAIPMHClient.fetch_data_from_scythe("endpoint", mock_func, 1, a=2)
    mock_func.assert_called_once_with(mock_instance, 1, a=2)
    assert result == "result"


def test_identify_prints_response_and_handles_exception(mock_scythe, mock_etree_tostring, capsys):
    mock_identify = MagicMock()
    mock_identify.xml = "<xml/>"
    mock_scythe.return_value.__enter__.return_value.identify.return_value = mock_identify
    OAIPMHClient.identify("endpoint")
    out = capsys.readouterr().out
    assert "Identify response:" in out
    assert "<xml>data</xml>" in out

    # Test exception handling
    with patch("oaim_client.OAIPMHClient.fetch_data_from_scythe", side_effect=Exception("fail")):
        OAIPMHClient.identify("endpoint")
        err = capsys.readouterr().out
        assert "Exception: fail" in err


def test_list_metadata_formats_prints_formats_and_handles_exception(mock_scythe, mock_etree_tostring, capsys):
    mock_format = MagicMock()
    mock_format.xml = "<xml/>"
    mock_scythe.return_value.__enter__.return_value.list_metadata_formats.return_value = [mock_format]
    OAIPMHClient.list_metadata_formats("endpoint", identifier="id")
    out = capsys.readouterr().out
    assert "Metadata formats:" in out
    assert "<xml>data</xml>" in out

    with patch("oaim_client.OAIPMHClient.fetch_data_from_scythe", side_effect=Exception("fail")):
        OAIPMHClient.list_metadata_formats("endpoint", identifier="id")
        err = capsys.readouterr().out
        assert "Exception: fail" in err


def test_list_identifiers_prints_identifiers_and_handles_exception(mock_scythe, mock_etree_tostring, capsys):
    mock_identifier = MagicMock()
    mock_identifier.xml = "<xml/>"
    mock_scythe.return_value.__enter__.return_value.list_identifiers.return_value = [mock_identifier]
    OAIPMHClient.list_identifiers("endpoint", "prefix", from_date="2020-01-01", until="2020-01-02", set_name="set")
    out = capsys.readouterr().out
    assert "Identifiers:" in out
    assert "<xml>data</xml>" in out

    with patch("oaim_client.OAIPMHClient.fetch_data_from_scythe", side_effect=Exception("fail")):
        OAIPMHClient.list_identifiers("endpoint", "prefix")
        err = capsys.readouterr().out
        assert "Exception: fail" in err


def test_list_sets_prints_sets_and_handles_exception(mock_scythe, mock_etree_tostring, capsys):
    mock_set = MagicMock()
    mock_set.xml = "<xml/>"
    mock_scythe.return_value.__enter__.return_value.list_sets.return_value = [mock_set]
    OAIPMHClient.list_sets("endpoint")
    out = capsys.readouterr().out
    assert "List sets:" in out
    assert "<xml>data</xml>" in out

    with patch("oaim_client.OAIPMHClient.fetch_data_from_scythe", side_effect=Exception("fail")):
        OAIPMHClient.list_sets("endpoint")
        err = capsys.readouterr().out
        assert "Exception: fail" in err


def test_get_record_prints_record_and_handles_exception(mock_scythe, mock_etree_tostring, capsys):
    mock_record = MagicMock()
    mock_record.xml = "<xml/>"
    mock_scythe.return_value.__enter__.return_value.get_record.return_value = mock_record
    OAIPMHClient.get_record("endpoint", "id", "prefix")
    out = capsys.readouterr().out
    assert "Get record:" in out
    assert "<xml>data</xml>" in out

    with patch("oaim_client.OAIPMHClient.fetch_data_from_scythe", side_effect=Exception("fail")):
        OAIPMHClient.get_record("endpoint", "id", "prefix")
        err = capsys.readouterr().out
        assert "Exception: fail" in err


def test_list_records_prints_records_and_handles_exception(mock_scythe, mock_etree_tostring, capsys):
    mock_record = MagicMock()
    mock_record.xml = "<xml/>"
    mock_scythe.return_value.__enter__.return_value.list_records.return_value = [mock_record]
    OAIPMHClient.list_records("endpoint", "prefix", from_date="2020-01-01", until="2020-01-02", set_name="set")
    out = capsys.readouterr().out
    assert "List records:" in out
    assert "<xml>data</xml>" in out

    with patch("oaim_client.OAIPMHClient.fetch_data_from_scythe", side_effect=Exception("fail")):
        OAIPMHClient.list_records("endpoint", "prefix")
        err = capsys.readouterr().out
        assert "Exception: fail" in err


def test_get_arg_parser_returns_parser():
    parser = get_arg_parser()
    assert parser is not None
    args = parser.parse_args(["--im-endpoint", "url", "identify"])
    assert args.command == "identify"
    assert args.im_endpoint == "url"
