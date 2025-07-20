"""
Transmission Pusher - A Python client for Transmission BitTorrent client

This package provides a simple and efficient way to interact with Transmission
via its RPC API, allowing you to add torrents, list existing torrents,
and manage your downloads programmatically.

Example:
    >>> from transmission_pusher import TransmissionClient
    >>> client = TransmissionClient(host='localhost', port=9091)
    >>> client.add_torrent_file('/path/to/file.torrent')
"""

from .diagnose_connection import check_rpc_endpoint
from .diagnose_connection import main as diagnose_connection
from .transmission_client import TransmissionClient

__version__ = "1.0.0"
__author__ = "Transmission Pusher Team"
__email__ = "contact@transmission-pusher.com"

__all__ = ["TransmissionClient", "check_rpc_endpoint", "diagnose_connection"]
