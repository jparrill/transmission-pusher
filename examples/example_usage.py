#!/usr/bin/env python3
"""
Example usage of the Transmission client
Configured to use environment variables
"""

import os

from transmission_pusher.transmission_client import TransmissionClient


def example_list_torrents() -> None:
    """Example: List existing torrents"""
    print("📋 Example: Listing existing torrents...")

    # Get credentials from environment
    base_url = os.getenv("TRANSMISSION_URL")
    username = os.getenv("TRANSMISSION_USERNAME")
    password = os.getenv("TRANSMISSION_PASSWORD")

    if not all([base_url, username, password]):
        print("❌ Missing environment variables!")
        print("Please set TRANSMISSION_URL, TRANSMISSION_USERNAME, and " "TRANSMISSION_PASSWORD in your .env file")
        return

    client = TransmissionClient(base_url=base_url, username=username, password=password)

    try:
        torrents = client.get_torrents()
        print(f"Found {len(torrents)} torrents:")
        for torrent in torrents:
            status = "⏸️" if torrent.get("status") == 4 else "▶️"
            percent = torrent.get("percentDone", 0) * 100
            print(f"   {status} {torrent.get('name', 'N/A')} - {percent:.1f}%")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_add_local_file() -> None:
    """Example: Add local .torrent file"""
    print("📁 Example: Adding local file...")

    # Replace with the path to your .torrent file
    torrent_file = "/path/to/your/file.torrent"

    # Get credentials from environment
    base_url = os.getenv("TRANSMISSION_URL")
    username = os.getenv("TRANSMISSION_USERNAME")
    password = os.getenv("TRANSMISSION_PASSWORD")

    if not all([base_url, username, password]):
        print("❌ Missing environment variables!")
        return

    client = TransmissionClient(base_url=base_url, username=username, password=password)

    try:
        client.add_torrent_file(torrent_file)
    except Exception as e:
        print(f"❌ Error: {e}")


def example_add_from_url() -> None:
    """Example: Add torrent from URL"""
    print("🌐 Example: Adding from URL...")

    # Replace with the URL of your .torrent file
    torrent_url = "https://example.com/file.torrent"

    # Get credentials from environment
    base_url = os.getenv("TRANSMISSION_URL")
    username = os.getenv("TRANSMISSION_USERNAME")
    password = os.getenv("TRANSMISSION_PASSWORD")

    if not all([base_url, username, password]):
        print("❌ Missing environment variables!")
        return

    client = TransmissionClient(base_url=base_url, username=username, password=password)

    try:
        client.add_torrent_url(torrent_url)
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 Example usage of the Transmission client")
    print("=" * 50)

    # Get credentials from environment
    base_url = os.getenv("TRANSMISSION_URL")
    username = os.getenv("TRANSMISSION_USERNAME")

    if base_url and username:
        print(f"URL: {base_url}")
        print(f"Username: {username}")
    else:
        print("⚠️  Environment variables not set")

    print("=" * 50)

    # Uncomment the function you want to test:

    example_list_torrents()
    # example_add_local_file()
    # example_add_from_url()

    print("\n💡 To use this script:")
    print("1. Set your credentials in the .env file")
    print("2. Uncomment the function you want to test")
    print("3. Run: python example_usage.py")
