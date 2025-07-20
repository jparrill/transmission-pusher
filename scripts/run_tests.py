#!/usr/bin/env python3
"""
Script to run tests with coverage
"""

import subprocess
import sys


def run_tests():
    """Run all tests"""
    print("🧪 Running Transmission Client Tests")
    print("=" * 50)

    # Check if pytest is installed
    try:
        import pytest  # noqa: F401
    except ImportError:
        print("❌ pytest is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"])

    # Run tests with coverage
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=src/transmission_pusher",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v",
    ]

    print("📋 Running tests...")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
