#!/usr/bin/env python3
"""
Tests for command line interface functionality
"""

import pytest
import os
import tempfile
import shutil
import sys
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from transmission_pusher.transmission_client import main


class TestCLI:
    """Test cases for command line interface"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TransmissionClient"""
        mock = Mock()
        mock.get_torrents.return_value = [
            {
                "id": 1,
                "name": "Test Torrent 1",
                "status": 4,
                "percentDone": 0.5,
                "downloadDir": "/downloads"
            },
            {
                "id": 2,
                "name": "Test Torrent 2",
                "status": 6,
                "percentDone": 1.0,
                "downloadDir": "/downloads"
            }
        ]
        return mock

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_list_torrents(self, mock_client_class, mock_client):
        """Test --list functionality"""
        mock_client_class.return_value = mock_client

        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', '--list']):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 0
                output = mock_stdout.getvalue()
                assert "Test Torrent 1" in output
                assert "Test Torrent 2" in output
                assert "50.0%" in output
                assert "100.0%" in output

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_add_local_file(self, mock_client_class, mock_client):
        """Test adding a local torrent file"""
        mock_client_class.return_value = mock_client
        mock_client.add_torrent_file.return_value = {"result": "success"}

        # Create a temporary torrent file
        with tempfile.NamedTemporaryFile(suffix='.torrent', delete=False) as f:
            f.write(b"d8:announce35:http://example.com/announce4:info...")
            torrent_file = f.name

        try:
            # Mock sys.argv
            with patch('sys.argv', ['transmission_client.py', torrent_file]):
                with patch('sys.stdout', new=StringIO()) as mock_stdout:
                    result = main()

                    assert result == 0
                    mock_client.add_torrent_file.assert_called_once_with(torrent_file)
                    output = mock_stdout.getvalue()
                    assert "Adding local file" in output

        finally:
            os.unlink(torrent_file)

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_add_url(self, mock_client_class, mock_client):
        """Test adding a torrent from URL"""
        mock_client_class.return_value = mock_client
        mock_client.add_torrent_url.return_value = {"result": "success"}

        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', 'https://example.com/test.torrent']):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 0
                mock_client.add_torrent_url.assert_called_once_with('https://example.com/test.torrent')
                output = mock_stdout.getvalue()
                assert "Adding from URL" in output

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_process_folder(self, mock_client_class, mock_client, temp_dir):
        """Test --folder functionality"""
        mock_client_class.return_value = mock_client
        mock_client.add_torrent_file.return_value = {"result": "success"}

        # Create test torrent files
        torrent_files = []
        for i in range(3):
            torrent_file = os.path.join(temp_dir, f"test{i}.torrent")
            with open(torrent_file, 'wb') as f:
                f.write(b"d8:announce35:http://example.com/announce4:info...")
            torrent_files.append(torrent_file)

        # Create a non-torrent file
        non_torrent_file = os.path.join(temp_dir, "test.txt")
        with open(non_torrent_file, 'w') as f:
            f.write("This is not a torrent file")

        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', '--folder', temp_dir]):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 0
                # Should be called 3 times (one for each .torrent file)
                assert mock_client.add_torrent_file.call_count == 3
                output = mock_stdout.getvalue()
                assert "Found 3 .torrent files" in output
                assert "Successfully added 3/3 torrents" in output

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_process_folder_no_torrents(self, mock_client_class, mock_client, temp_dir):
        """Test --folder functionality with no torrent files"""
        mock_client_class.return_value = mock_client

        # Create a non-torrent file
        non_torrent_file = os.path.join(temp_dir, "test.txt")
        with open(non_torrent_file, 'w') as f:
            f.write("This is not a torrent file")

        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', '--folder', temp_dir]):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 1
                output = mock_stdout.getvalue()
                assert "No .torrent files found" in output

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_process_folder_nonexistent(self, mock_client_class, mock_client):
        """Test --folder functionality with non-existent folder"""
        mock_client_class.return_value = mock_client

        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', '--folder', '/non/existent/path']):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 1
                output = mock_stdout.getvalue()
                assert "Folder does not exist" in output

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_process_folder_not_directory(self, mock_client_class, mock_client, temp_dir):
        """Test --folder functionality with file instead of directory"""
        mock_client_class.return_value = mock_client

        # Create a file
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("This is a file")

        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', '--folder', test_file]):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 1
                output = mock_stdout.getvalue()
                assert "Path is not a directory" in output

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_process_folder_partial_failure(self, mock_client_class, mock_client, temp_dir):
        """Test --folder functionality with some failures"""
        mock_client_class.return_value = mock_client

        # Create test torrent files
        torrent_files = []
        for i in range(3):
            torrent_file = os.path.join(temp_dir, f"test{i}.torrent")
            with open(torrent_file, 'wb') as f:
                f.write(b"d8:announce35:http://example.com/announce4:info...")
            torrent_files.append(torrent_file)

        # Make the second call fail
        mock_client.add_torrent_file.side_effect = [
            {"result": "success"},  # First call succeeds
            Exception("API Error"),  # Second call fails
            {"result": "success"}    # Third call succeeds
        ]

        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', '--folder', temp_dir]):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 0  # Should still return 0 even with partial failures
                assert mock_client.add_torrent_file.call_count == 3
                output = mock_stdout.getvalue()
                assert "Successfully added 2/3 torrents" in output

    def test_no_arguments(self):
        """Test running without arguments"""
        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py']):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 1
                output = mock_stdout.getvalue()
                assert "You must specify" in output

    def test_file_not_found(self):
        """Test adding non-existent file"""
        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', '/non/existent/file.torrent']):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 1
                output = mock_stdout.getvalue()
                assert "File does not exist" in output

    def test_invalid_url(self):
        """Test adding invalid URL"""
        # Mock sys.argv
        with patch('sys.argv', ['transmission_client.py', 'not-a-url']):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                result = main()

                assert result == 1
                output = mock_stdout.getvalue()
                assert "File does not exist and is not a valid URL" in output

    @patch('transmission_pusher.transmission_client.TransmissionClient')
    def test_environment_variables(self, mock_client_class, mock_client):
        """Test that environment variables are used when command line args are not provided"""
        mock_client_class.return_value = mock_client
        mock_client.get_torrents.return_value = []

        # Mock environment variables
        env_vars = {
            'TRANSMISSION_URL': 'http://test:9091/transmission',
            'TRANSMISSION_USERNAME': 'env_user',
            'TRANSMISSION_PASSWORD': 'env_pass'
        }

        with patch.dict('os.environ', env_vars):
            with patch('sys.argv', ['transmission_client.py', '--list']):
                with patch('sys.stdout', new=StringIO()):
                    main()

                    # Verify TransmissionClient was called with environment variables
                    mock_client_class.assert_called_once()
                    call_args = mock_client_class.call_args
                    assert call_args[1]['base_url'] == 'http://test:9091/transmission'
                    assert call_args[1]['username'] == 'env_user'
                    assert call_args[1]['password'] == 'env_pass'