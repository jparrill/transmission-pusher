#!/usr/bin/env python3
"""
Python script to add .torrent files to Transmission
Uses Transmission's REST API to add torrents
"""

import argparse
import base64
import os
from typing import Any

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TransmissionClient:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 9091,
        username: str | None = None,
        password: str | None = None,
        base_url: str | None = None,
    ) -> None:
        """
        Initialize Transmission client

        Args:
            host (str): Transmission host (default: localhost)
            port (int): Transmission port (default: 9091)
            username (str): Transmission username (optional)
            password (str): Transmission password (optional)
            base_url (str): Complete base URL (optional, overrides host/port)
        """
        if base_url:
            # If a complete base URL is provided, use it
            if base_url.endswith("/"):
                base_url = base_url[:-1]
            self.base_url = f"{base_url}/rpc"
        else:
            self.base_url = f"http://{host}:{port}/transmission/rpc"

        self.session = requests.Session()

        if username and password:
            self.session.auth = (username, password)

        # Get session-id on first call
        self._get_session_id()

    def _get_session_id(self) -> None:
        """Gets the session-id required for API calls"""
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 409:  # Conflict - session-id required
                session_id = response.headers.get("X-Transmission-Session-Id")
                if session_id:
                    self.session.headers.update({"X-Transmission-Session-Id": session_id})
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Transmission: {e}")
            raise

    def add_torrent_file(self, torrent_file_path: str) -> Any:
        """
        Add a .torrent file to Transmission

        Args:
            torrent_file_path (str): Path to the .torrent file

        Returns:
            dict: API response
        """
        if not os.path.exists(torrent_file_path):
            raise FileNotFoundError(f"File {torrent_file_path} does not exist")

        # Read and encode the .torrent file in base64
        with open(torrent_file_path, "rb") as f:
            torrent_data = base64.b64encode(f.read()).decode("utf-8")

        # Prepare data for the API
        data = {
            "method": "torrent-add",
            "arguments": {"metainfo": torrent_data},
        }

        try:
            response = self.session.post(self.base_url, json=data)
            response.raise_for_status()

            result = response.json()

            if result.get("result") == "success":
                torrent_info = result.get("arguments", {}).get("torrent-added", {})
                if torrent_info:
                    print(f"✅ Torrent added successfully: {torrent_info.get('name', 'N/A')}")
                    print(f"   ID: {torrent_info.get('id')}")
                    print(f"   Hash: {torrent_info.get('hashString')}")
                else:
                    print("✅ Torrent added successfully")
                return result
            else:
                print(f"❌ Error adding torrent: {result}")
                return result

        except requests.exceptions.RequestException as e:
            print(f"❌ Error communicating with Transmission: {e}")
            raise

    def add_torrent_url(self, torrent_url: str) -> Any:
        """
        Add a torrent from a URL

        Args:
            torrent_url (str): URL of the .torrent file

        Returns:
            dict: API response
        """
        data = {
            "method": "torrent-add",
            "arguments": {"filename": torrent_url},
        }

        try:
            response = self.session.post(self.base_url, json=data)
            response.raise_for_status()

            result = response.json()

            if result.get("result") == "success":
                torrent_info = result.get("arguments", {}).get("torrent-added", {})
                if torrent_info:
                    print(f"✅ Torrent added successfully: {torrent_info.get('name', 'N/A')}")
                else:
                    print("✅ Torrent added successfully")
                return result
            else:
                print(f"❌ Error adding torrent: {result}")
                return result

        except requests.exceptions.RequestException as e:
            print(f"❌ Error communicating with Transmission: {e}")
            raise

    def get_torrents(self) -> list[dict[str, Any]]:
        """
        Get the list of torrents

        Returns:
            list of dicts: List of torrents
        """
        data = {
            "method": "torrent-get",
            "arguments": {
                "fields": [
                    "id",
                    "name",
                    "status",
                    "percentDone",
                    "downloadDir",
                ]
            },
        }

        try:
            response = self.session.post(self.base_url, json=data)
            response.raise_for_status()

            result = response.json()
            torrents = result.get("arguments", {}).get("torrents", [])
            if not isinstance(torrents, list):
                return []
            return [t for t in torrents if isinstance(t, dict)]

        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting torrents: {e}")
            raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Add torrents to Transmission")
    parser.add_argument("torrent", nargs="?", help="Path to .torrent file or URL")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Transmission host (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9091,
        help="Transmission port (default: 9091)",
    )
    parser.add_argument(
        "--base-url",
        help=("Complete base URL of Transmission " "(e.g., http://192.168.1.127:29091/transmission/web)"),
    )
    parser.add_argument("--username", help="Transmission username")
    parser.add_argument("--password", help="Transmission password")
    parser.add_argument("--folder", help="Process all .torrent files in a folder")
    parser.add_argument("--list", action="store_true", help="List existing torrents")

    args = parser.parse_args()

    try:
        # Get credentials from environment variables if not provided
        username = args.username or os.getenv("TRANSMISSION_USERNAME")
        password = args.password or os.getenv("TRANSMISSION_PASSWORD")
        base_url = args.base_url or os.getenv("TRANSMISSION_URL")

        # Create Transmission client
        client = TransmissionClient(
            host=args.host,
            port=args.port,
            username=username,
            password=password,
            base_url=base_url,
        )

        if args.list:
            print("📋 Listing existing torrents:")
            torrents = client.get_torrents()
            for torrent in torrents:
                status = "⏸️" if torrent.get("status") == 4 else "▶️"
                percent = torrent.get("percentDone", 0) * 100
                print(f"   {status} {torrent.get('name', 'N/A')} - {percent:.1f}%")
        elif args.folder:
            # Process all .torrent files in a folder
            folder_path = args.folder
            if not os.path.exists(folder_path):
                print(f"❌ Folder does not exist: {folder_path}")
                return 1

            if not os.path.isdir(folder_path):
                print(f"❌ Path is not a directory: {folder_path}")
                return 1

            print(f"📁 Processing folder: {folder_path}")

            # Find all .torrent files in the folder
            torrent_files = []
            for file in os.listdir(folder_path):
                if file.lower().endswith(".torrent"):
                    torrent_files.append(os.path.join(folder_path, file))

            if not torrent_files:
                print("❌ No .torrent files found in the folder")
                return 1

            print(f"📦 Found {len(torrent_files)} .torrent files")

            # Process each .torrent file
            success_count = 0
            for torrent_file in torrent_files:
                try:
                    print(f"\n📁 Adding: {os.path.basename(torrent_file)}")
                    client.add_torrent_file(torrent_file)
                    success_count += 1
                except Exception as e:
                    print(f"❌ Error adding {os.path.basename(torrent_file)}: {e}")

            print(f"\n✅ Successfully added {success_count}/{len(torrent_files)} torrents")

        elif args.torrent:
            # Determine if it's a local file or URL
            if os.path.exists(args.torrent):
                print(f"📁 Adding local file: {args.torrent}")
                client.add_torrent_file(args.torrent)
            elif args.torrent.startswith(("http://", "https://")):
                print(f"🌐 Adding from URL: {args.torrent}")
                client.add_torrent_url(args.torrent)
            else:
                print("❌ File does not exist and is not a valid URL")
                return 1
        else:
            print(
                "❌ You must specify a .torrent file, use --folder to process a directory, "
                "or use --list to see existing torrents"
            )
            parser.print_help()
            return 1

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
