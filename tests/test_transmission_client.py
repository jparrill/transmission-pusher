#!/usr/bin/env python3
"""
Tests for TransmissionClient class
"""

import base64
import os
import shutil
import tempfile
from typing import Generator
from unittest.mock import Mock, patch

import pytest

from transmission_pusher.transmission_client import TransmissionClient


class TestTransmissionClient:
    """Test cases for TransmissionClient class"""

    @pytest.fixture
    def mock_session(self) -> Mock:
        """Create a mock session for testing"""
        mock = Mock()
        mock.auth = None
        mock.headers = {}
        return mock

    @pytest.fixture
    def client(self, mock_session: Mock) -> TransmissionClient:
        """Create a TransmissionClient instance for testing"""
        with patch("transmission_pusher.transmission_client.requests.Session", return_value=mock_session):
            client = TransmissionClient(host="localhost", port=9091, username="test_user", password="test_pass")
            return client

    def test_init_with_host_port(self, mock_session: Mock) -> None:
        """Test client initialization with host and port"""
        with patch("transmission_pusher.transmission_client.requests.Session", return_value=mock_session):
            test_client = TransmissionClient(host="192.168.1.100", port=9091)
            assert test_client.base_url == "http://192.168.1.100:9091/transmission/rpc"
            assert mock_session.auth is None  # No auth provided

    def test_init_with_base_url(self, mock_session: Mock) -> None:
        """Test client initialization with base URL"""
        with patch("transmission_pusher.transmission_client.requests.Session", return_value=mock_session):
            test_client = TransmissionClient(base_url="http://192.168.1.127:29091/transmission")
            assert test_client.base_url == "http://192.168.1.127:29091/transmission/rpc"

    def test_init_with_auth(self, mock_session: Mock) -> None:
        """Test client initialization with authentication"""
        with patch("transmission_pusher.transmission_client.requests.Session", return_value=mock_session):
            TransmissionClient(username="test_user", password="test_pass")
            assert mock_session.auth == ("test_user", "test_pass")

    def test_get_session_id_success(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test successful session ID retrieval"""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.headers = {"X-Transmission-Session-Id": "test-session-id"}
        mock_session.get.return_value = mock_response

        client._get_session_id()

        assert mock_session.headers["X-Transmission-Session-Id"] == "test-session-id"
        # The method is called twice: once in __init__ and once in _get_session_id
        assert mock_session.get.call_count == 2
        assert mock_session.get.call_args_list[0][0][0] == client.base_url
        assert mock_session.get.call_args_list[1][0][0] == client.base_url

    def test_get_session_id_no_session_id(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test session ID retrieval when no session ID is returned"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_session.get.return_value = mock_response

        client._get_session_id()

        # Should not update headers if no session ID
        assert "X-Transmission-Session-Id" not in mock_session.headers

    def test_get_session_id_connection_error(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test session ID retrieval with connection error"""
        mock_session.get.side_effect = Exception("Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            client._get_session_id()

    def test_add_torrent_file_success(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test successful torrent file addition"""
        # Create a temporary torrent file
        with tempfile.NamedTemporaryFile(suffix=".torrent", delete=False) as f:
            f.write(b"d8:announce35:http://example.com/announce4:info...")
            torrent_file = f.name

        try:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "result": "success",
                "arguments": {"torrent-added": {"id": 1, "name": "Test Torrent", "hashString": "abc123"}},
            }
            mock_session.post.return_value = mock_response

            result = client.add_torrent_file(torrent_file)

            assert result["result"] == "success"
            mock_session.post.assert_called_once()

            # Verify the request data
            call_args = mock_session.post.call_args
            assert call_args[0][0] == client.base_url
            assert "metainfo" in call_args[1]["json"]["arguments"]

        finally:
            os.unlink(torrent_file)

    def test_add_torrent_file_file_not_found(self, client: TransmissionClient) -> None:
        """Test torrent file addition with non-existent file"""
        with pytest.raises(FileNotFoundError):
            client.add_torrent_file("/non/existent/file.torrent")

    def test_add_torrent_file_api_error(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test torrent file addition with API error"""
        # Create a temporary torrent file
        with tempfile.NamedTemporaryFile(suffix=".torrent", delete=False) as f:
            f.write(b"d8:announce35:http://example.com/announce4:info...")
            torrent_file = f.name

        try:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": "error", "arguments": {}}
            mock_session.post.return_value = mock_response

            result = client.add_torrent_file(torrent_file)

            assert result["result"] == "error"

        finally:
            os.unlink(torrent_file)

    def test_add_torrent_url_success(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test successful torrent URL addition"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "arguments": {"torrent-added": {"name": "Test Torrent"}},
        }
        mock_session.post.return_value = mock_response

        result = client.add_torrent_url("https://example.com/test.torrent")

        assert result["result"] == "success"
        mock_session.post.assert_called_once()

        # Verify the request data
        call_args = mock_session.post.call_args
        assert call_args[0][0] == client.base_url
        assert call_args[1]["json"]["arguments"]["filename"] == "https://example.com/test.torrent"

    def test_add_torrent_url_api_error(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test torrent URL addition with API error"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "error", "arguments": {}}
        mock_session.post.return_value = mock_response

        result = client.add_torrent_url("https://example.com/test.torrent")

        assert result["result"] == "error"

    def test_get_torrents_success(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test successful torrent list retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "arguments": {
                "torrents": [
                    {"id": 1, "name": "Test Torrent 1", "status": 4, "percentDone": 0.5, "downloadDir": "/downloads"},
                    {"id": 2, "name": "Test Torrent 2", "status": 6, "percentDone": 1.0, "downloadDir": "/downloads"},
                ]
            }
        }
        mock_session.post.return_value = mock_response

        torrents = client.get_torrents()

        assert len(torrents) == 2
        assert torrents[0]["name"] == "Test Torrent 1"
        assert torrents[1]["name"] == "Test Torrent 2"

    def test_get_torrents_empty(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test torrent list retrieval with empty result"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"arguments": {"torrents": []}}
        mock_session.post.return_value = mock_response

        torrents = client.get_torrents()

        assert len(torrents) == 0

    def test_get_torrents_connection_error(self, client: TransmissionClient, mock_session: Mock) -> None:
        """Test torrent list retrieval with connection error"""
        mock_session.post.side_effect = Exception("Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            client.get_torrents()


class TestTransmissionClientIntegration:
    """Integration tests for TransmissionClient"""

    @pytest.fixture
    def temp_dir(self) -> Generator[str, None, None]:
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_base64_encoding(self, temp_dir: str) -> None:
        """Test that torrent files are properly base64 encoded"""
        # Create a test torrent file
        torrent_content = b"d8:announce35:http://example.com/announce4:info..."
        torrent_file = os.path.join(temp_dir, "test.torrent")

        with open(torrent_file, "wb") as f:
            f.write(torrent_content)

        # Mock the session
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success", "arguments": {}}
        mock_session.post.return_value = mock_response
        mock_session.auth = None
        mock_session.headers = {}

        with patch("transmission_pusher.transmission_client.requests.Session", return_value=mock_session):
            client = TransmissionClient()
            client.add_torrent_file(torrent_file)

            # Verify the request was made with base64 encoded data
            call_args = mock_session.post.call_args
            request_data = call_args[1]["json"]["arguments"]["metainfo"]

            # Decode and verify
            decoded_data = base64.b64decode(request_data)
            assert decoded_data == torrent_content
