# Transmission Pusher

[![CI](https://github.com/yourusername/transmission-pusher/workflows/CI/badge.svg)](https://github.com/yourusername/transmission-pusher/actions)
[![PyPI](https://img.shields.io/pypi/v/transmission-pusher)](https://pypi.org/project/transmission-pusher/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://codecov.io/gh/yourusername/transmission-pusher/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/transmission-pusher)

A Python client for Transmission BitTorrent client that provides a simple and efficient way to interact with Transmission via its RPC API, allowing you to add torrents, list existing torrents, and manage your downloads programmatically.

## Features

- ✅ Add local .torrent files
- ✅ Add torrents from URLs
- ✅ List existing torrents with detailed information
- ✅ Process entire folders of .torrent files
- ✅ Authentication support
- ✅ Robust error handling and logging
- ✅ Connection diagnostics
- ✅ Command-line interface
- ✅ Programmatic API

## Installation

### From PyPI (Recommended)

```bash
pip install transmission-pusher
```

### From Source

```bash
git clone https://github.com/yourusername/transmission-pusher.git
cd transmission-pusher
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/yourusername/transmission-pusher.git
cd transmission-pusher
pip install -e ".[dev]"
```

## Quick Start

### Option 1: Direct Usage (Recommended for testing)

```bash
# Clone the repository
git clone https://github.com/yourusername/transmission-pusher.git
cd transmission-pusher

# Set up environment
cp env.example .env
# Edit .env with your Transmission credentials

# Activate virtual environment (if using one)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Test connection
python diagnose_connection.py
# or
./diagnose_connection.py

# List existing torrents
python transmission_client.py --list
# or
./transmission_client.py --list

# Add a torrent file
python transmission_client.py /path/to/file.torrent
# or
./transmission_client.py /path/to/file.torrent
```

### Option 2: Install as Package

```bash
# Install the package
pip install transmission-pusher

# Use the installed commands
transmission-pusher --list
transmission-diagnose
```

### 1. Configure Transmission

Ensure Transmission is configured to accept RPC connections:

1. **Enable web interface**: In Transmission, go to `Preferences` → `Web` and enable "Enable web client"
2. **Configure port**: Default uses port 9091
3. **Configure authentication** (optional): Set username and password in `Preferences` → `Web`

### 2. Set up Environment

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your Transmission credentials:

```bash
TRANSMISSION_URL=http://your-transmission-host:port/transmission
TRANSMISSION_USERNAME=your_username
TRANSMISSION_PASSWORD=your_password
```

### 3. Use the Client

#### Command Line Interface

```bash
# Add a local .torrent file
python transmission_client.py /path/to/file.torrent
# or
./transmission_client.py /path/to/file.torrent

# Add from URL
python transmission_client.py "https://example.com/file.torrent"

# List existing torrents
python transmission_client.py --list

# Process all .torrent files in a folder
python transmission_client.py --folder /path/to/torrents

# Diagnose connection issues
python diagnose_connection.py
# or
./diagnose_connection.py
```

#### Programmatic Usage

```python
# Option 1: If installed as package
from transmission_pusher import TransmissionClient

# Option 2: Direct import from source
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from transmission_pusher.transmission_client import TransmissionClient

# Create client
client = TransmissionClient(
    host="localhost",
    port=9091,
    username="your_username",
    password="your_password"
)

# Add a torrent file
result = client.add_torrent_file("/path/to/file.torrent")

# Add from URL
result = client.add_torrent_url("https://example.com/file.torrent")

# List torrents
torrents = client.get_torrents()
for torrent in torrents:
    print(f"{torrent['name']}: {torrent['percentDone']*100:.1f}%")
```

## Configuration Options

### Environment Variables

- `TRANSMISSION_URL`: Complete base URL of Transmission
- `TRANSMISSION_USERNAME`: Username for authentication
- `TRANSMISSION_PASSWORD`: Password for authentication

### Command Line Options

- `--base-url`: Complete base URL of Transmission
- `--host`: Transmission host (default: localhost)
- `--port`: Transmission port (default: 9091)
- `--username`: Transmission username
- `--password`: Transmission password
- `--folder`: Process all .torrent files in a directory
- `--list`: List existing torrents

## Development

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/test_transmission_client.py
```

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Run all checks
make check
```

### Building

```bash
# Build package
make build

# Create distribution
make dist
```

## Project Structure

```
transmission-pusher/
├── transmission_client.py          # Main CLI script (root level)
├── diagnose_connection.py         # Connection diagnostics (root level)
├── src/
│   └── transmission_pusher/
│       ├── __init__.py
│       ├── transmission_client.py  # Original CLI script
│       └── diagnose_connection.py # Original diagnostics script
├── tests/
│   ├── test_transmission_client.py
│   ├── test_cli.py
│   └── test_diagnose_connection.py
├── scripts/
│   ├── run_tests.py
│   └── setup.sh
├── examples/
│   └── example_usage.py
├── docs/
├── .github/
│   └── workflows/
│       └── ci.yml
├── setup.py
├── pyproject.toml
├── requirements.txt
├── Makefile
├── env.example                     # Environment variables template
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install pre-commit hooks
pre-commit install

# Install development dependencies
make install-dev

# Run all checks before committing
make pre-commit
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://github.com/yourusername/transmission-pusher#readme)
- 🐛 [Issue Tracker](https://github.com/yourusername/transmission-pusher/issues)
- 💬 [Discussions](https://github.com/yourusername/transmission-pusher/discussions)

## Changelog

### v1.0.0
- Initial release
- Basic torrent management functionality
- Command-line interface
- Connection diagnostics
- Comprehensive test suite