#!/usr/bin/env python3
"""
Tests for diagnose_connection functionality
"""

from io import StringIO
from unittest.mock import Mock, patch

import requests

from transmission_pusher.diagnose_connection import check_rpc_endpoint, main


class TestDiagnoseConnection:
    """Test cases for diagnose_connection functionality"""

    def test_rpc_endpoint_success(self) -> None:
        """Test successful RPC endpoint test"""
        with patch("transmission_pusher.diagnose_connection.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 409
            mock_response.headers = {"X-Transmission-Session-Id": "test-session-id"}
            mock_get.return_value = mock_response

            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                result = check_rpc_endpoint("http://test:9091/transmission")

                assert result is True
                output = mock_stdout.getvalue()
                assert "Testing RPC endpoint" in output
                assert "Session ID: test-session-id" in output

    def test_rpc_endpoint_200_status(self) -> None:
        """Test RPC endpoint with 200 status"""
        with patch("transmission_pusher.diagnose_connection.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {}
            mock_get.return_value = mock_response

            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                result = check_rpc_endpoint("http://test:9091/transmission")

                assert result is True
                output = mock_stdout.getvalue()
                assert "RPC endpoint accessible" in output

    def test_rpc_endpoint_failure(self) -> None:
        """Test RPC endpoint with failure"""
        with patch("transmission_pusher.diagnose_connection.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.headers = {}
            mock_get.return_value = mock_response

            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                result = check_rpc_endpoint("http://test:9091/transmission")

                assert result is False
                output = mock_stdout.getvalue()
                assert "Unexpected status: 404" in output

    def test_rpc_endpoint_connection_error(self) -> None:
        """Test RPC endpoint with connection error"""
        with patch("transmission_pusher.diagnose_connection.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                result = check_rpc_endpoint("http://test:9091/transmission")

                assert result is False
                output = mock_stdout.getvalue()
                assert "Error: Connection failed" in output

    def test_main_successful_configuration(self) -> None:
        """Test main function with successful configuration"""
        with patch("transmission_pusher.diagnose_connection.check_rpc_endpoint", return_value=True):
            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                with patch.dict(
                    "os.environ",
                    {
                        "TRANSMISSION_URL": "http://test:9091/transmission",
                        "TRANSMISSION_USERNAME": "test_user",
                        "TRANSMISSION_PASSWORD": "test_pass",
                    },
                ):
                    main()

                    output = mock_stdout.getvalue()
                    assert "Current configuration works!" in output

    def test_main_failed_configuration(self) -> None:
        """Test main function with failed configuration"""
        with patch("transmission_pusher.diagnose_connection.check_rpc_endpoint", return_value=False):
            with patch("transmission_pusher.diagnose_connection.requests.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 404
                mock_get.return_value = mock_response

                with patch("sys.stdout", new=StringIO()) as mock_stdout:
                    with patch.dict(
                        "os.environ",
                        {
                            "TRANSMISSION_URL": "http://test:9091/transmission",
                            "TRANSMISSION_USERNAME": "test_user",
                            "TRANSMISSION_PASSWORD": "test_pass",
                        },
                    ):
                        main()

                        output = mock_stdout.getvalue()
                        assert "Current configuration failed" in output
                        assert "Testing common Transmission configurations" in output
