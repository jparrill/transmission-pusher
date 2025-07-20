#!/usr/bin/env python3
"""
Diagnostic script to help find the correct Transmission configuration
"""

import os

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_url(url: str, description: str) -> bool:
    """Test a specific URL"""
    print(f"\n🔍 Testing: {description}")
    print(f"   URL: {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"   Error: {e}")
        return False


def check_rpc_endpoint(base_url: str, username: str | None = None, password: str | None = None) -> bool:
    """Test the RPC endpoint"""
    rpc_url = f"{base_url}/rpc"
    print(f"\n🔍 Testing RPC endpoint: {rpc_url}")

    try:
        auth = None
        if username and password:
            auth = (username, password)

        response = requests.get(rpc_url, auth=auth, timeout=5)
        print(f"   Status: {response.status_code}")

        if response.status_code == 409:
            session_id = response.headers.get("X-Transmission-Session-Id")
            print(f"   Session ID: {session_id}")
            return True
        elif response.status_code == 200:
            print("   ✅ RPC endpoint accessible")
            return True
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"   Error: {e}")
        return False


def main() -> None:
    print("🔧 Transmission Connection Diagnostic")
    print("=" * 50)

    # Get current configuration
    current_url = os.getenv("TRANSMISSION_URL")
    current_username = os.getenv("TRANSMISSION_USERNAME")
    current_password = os.getenv("TRANSMISSION_PASSWORD")

    print("Current configuration:")
    print(f"  URL: {current_url}")
    print(f"  Username: {current_username}")
    print(f"  Password: {'*' * len(current_password) if current_password else 'None'}")

    # Test current configuration
    if current_url:
        print("\n📋 Testing current configuration...")
        success = check_rpc_endpoint(current_url, current_username, current_password)

        if success:
            print("✅ Current configuration works!")
            return
        else:
            print("❌ Current configuration failed")

    # Test common configurations
    print("\n🔍 Testing common Transmission configurations...")

    # Common ports
    ports = [9091, 29091, 8080, 8081]
    paths = ["/transmission/web", "/transmission", ""]

    for port in ports:
        for path in paths:
            base_url = f"http://192.168.1.127:{port}{path}"
            if check_rpc_endpoint(base_url, current_username, current_password):
                print("\n🎉 Found working configuration!")
                print(f"   URL: {base_url}")
                print(f"   Username: {current_username}")
                print(f"   Password: {current_password}")
                print("\n💡 Update your .env file with:")
                print(f"   TRANSMISSION_URL={base_url}")
                return

    print("\n❌ No working configuration found")
    print("\n💡 Suggestions:")
    print("1. Verify Transmission is running")
    print("2. Check if Transmission is configured for web access")
    print("3. Verify the IP address is correct")
    print("4. Try different ports (9091, 8080, etc.)")
    print("5. Check if authentication is required")


if __name__ == "__main__":
    main()
