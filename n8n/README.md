# Transmission Standalone Script

This script is a completely independent version of the `transmission_client` that doesn't require any external libraries from the repository. It only uses Python standard library modules.

## Features

- ✅ **Completely independent**: Doesn't require `requests`, `python-dotenv` or other external dependencies
- ✅ **Standard library only**: Uses only Python standard library modules (`urllib`, `json`, `os`, etc.)
- ✅ **Full functionality**: Includes all functions from the original `transmission_client`
- ✅ **n8n compatible**: Perfect for use in isolated environments like n8n

## Functionality

- Add local .torrent files
- Add torrents from URLs
- Process complete folders of .torrent files
- List existing torrents
- Basic authentication
- .env file support

## Usage

### Basic setup

1. Copy the `env.example` file to `.env`:
```bash
cp env.example .env
```

2. Edit the `.env` file with your Transmission credentials:
```bash
TRANSMISSION_URL=http://your-server:port/transmission
TRANSMISSION_USERNAME=your-username
TRANSMISSION_PASSWORD=your-password
```

### Usage examples

#### Add a local .torrent file
```bash
python transmission_standalone.py /path/to/file.torrent
```

#### Add from URL
```bash
python transmission_standalone.py "https://example.com/file.torrent"
```

#### Process a complete folder
```bash
python transmission_standalone.py --folder /path/to/folder/with/torrents
```

#### List existing torrents
```bash
python transmission_standalone.py --list
```

#### Use specific parameters
```bash
python transmission_standalone.py file.torrent --host 192.168.1.100 --port 9091 --username user --password password
```

#### Use complete URL
```bash
python transmission_standalone.py file.torrent --base-url "http://192.168.1.100:9091/transmission"
```

## Available parameters

- `torrent`: Path to .torrent file or URL
- `--host`: Transmission host (default: localhost)
- `--port`: Transmission port (default: 9091)
- `--base-url`: Complete Transmission URL
- `--username`: Transmission username
- `--password`: Transmission password
- `--folder`: Process all .torrent files in a folder
- `--list`: List existing torrents
- `--env-file`: Path to .env file (default: .env)

## Environment variables

The script can read the following environment variables:

- `TRANSMISSION_URL`: Complete Transmission URL
- `TRANSMISSION_USERNAME`: Transmission username
- `TRANSMISSION_PASSWORD`: Transmission password

## Usage in n8n

To use this script in n8n, simply run the script as a system command:

```bash
python /path/to/script/transmission_standalone.py file.torrent
```

The script will return appropriate exit codes:
- `0`: Success
- `1`: Error

## CLI Installation

You can install a global CLI command that automatically loads the .env file from this repository:

### Quick Installation

```bash
# Run the installation script
./n8n/install-cli.sh
```

This will:
1. Copy the CLI script to `~/bin/transmission-pusher`
2. Make it executable
3. Check if `~/bin` is in your PATH

### Manual Installation

If you prefer to install manually:

```bash
# Copy the CLI script to ~/bin
cp n8n/transmission-cli ~/bin/transmission-pusher
chmod +x ~/bin/transmission-pusher

# Make sure ~/bin is in your PATH (add to .bashrc, .zshrc, etc.)
export PATH="$HOME/bin:$PATH"
```

### Usage

After installation, you can use the CLI from anywhere:

```bash
# Show help
transmission-pusher --help

# List existing torrents
transmission-pusher --list

# Add a torrent file
transmission-pusher /path/to/file.torrent

# Add from URL
transmission-pusher "https://example.com/file.torrent"

# Process a folder
transmission-pusher --folder /path/to/torrents/
```

The CLI automatically loads the `.env` file from this repository, so you don't need to specify credentials each time.

## Advantages over the original script

1. **No external dependencies**: Doesn't need to install `requests` or `python-dotenv`
2. **Portability**: Works in any standard Python environment
3. **Isolation**: Perfect for containers and isolated environments
4. **Compatibility**: Works with older Python versions

## Technical notes

- Uses `urllib` instead of `requests` for HTTP requests
- Implements its own .env file parser without external dependencies
- Handles basic authentication and Transmission session IDs
- Compatible with Python 3.6+