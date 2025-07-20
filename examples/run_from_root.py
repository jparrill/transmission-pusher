#!/usr/bin/env python3
"""
Example: Running Transmission client from project root
This script shows how to use the client without installing the package
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def main() -> None:
    """Main example function"""
    print("🚀 Transmission Client Example - Running from project root")
    print("=" * 60)

    # Load environment variables
    from dotenv import load_dotenv

    from transmission_pusher.diagnose_connection import main as diagnose_connection
    from transmission_pusher.transmission_client import TransmissionClient

    load_dotenv()

    # Get credentials from environment
    base_url = os.getenv("TRANSMISSION_URL")
    username = os.getenv("TRANSMISSION_USERNAME")
    password = os.getenv("TRANSMISSION_PASSWORD")

    if not all([base_url, username, password]):
        print("❌ Missing environment variables!")
        print("Please set TRANSMISSION_URL, TRANSMISSION_USERNAME, and " "TRANSMISSION_PASSWORD in your .env file")
        print("\nExample .env file:")
        print("TRANSMISSION_URL=http://localhost:9091/transmission")
        print("TRANSMISSION_USERNAME=your_username")
        print("TRANSMISSION_PASSWORD=your_password")
        return

    print("✅ Configuration loaded:")
    print(f"   URL: {base_url}")
    print(f"   Username: {username}")
    print("=" * 60)

    # Test connection first
    print("\n🔍 Testing connection...")
    try:
        diagnose_connection()
        print("✅ Connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Create client
    client = TransmissionClient(base_url=base_url, username=username, password=password)

    # List existing torrents
    print("\n📋 Listing existing torrents...")
    try:
        torrents = client.get_torrents()
        if torrents:
            print(f"Found {len(torrents)} torrents:")
            for torrent in torrents:
                status = "⏸️" if torrent.get("status") == 4 else "▶️"
                percent = torrent.get("percentDone", 0) * 100
                name = torrent.get("name", "N/A")
                print(f"   {status} {name} - {percent:.1f}%")
        else:
            print("No torrents found.")
    except Exception as e:
        print(f"❌ Error listing torrents: {e}")

    print("\n💡 Usage examples:")
    print("1. Add local file: python transmission_client.py /path/to/file.torrent")
    print("2. Add from URL: python transmission_client.py " "'https://example.com/file.torrent'")
    print("3. List torrents: python transmission_client.py --list")
    print("4. Diagnose connection: python diagnose_connection.py")
    print("\n📝 Note: Make sure to activate your virtual environment first:")
    print("   source .venv/bin/activate  # On Unix/Mac")
    print("   .venv\\Scripts\\activate     # On Windows")


if __name__ == "__main__":
    main()
