# Roger DirEnum 🐰

Directory and file enumeration tool for bug bounty reconnaissance.

## Features

- Fast directory fuzzing with multiple wordlists
- File extension scanning (.php, .js, .bak, .txt, etc.)
- Recursive directory crawling
- Response code filtering (200, 301, 302, 403, 500)
- Multi-threaded for speed
- Custom user-agent rotation
- Proxy support

## Installation

```bash
git clone https://github.com/jrabbit00/roger-direnum.git
cd roger-direnum
pip install -r requirements.txt
```

## Usage

```bash
# Basic directory scan
python3 direnum.py https://target.com

# Scan with wordlist
python3 direnum.py https://target.com -w /usr/share/wordlists/dirb/common.txt

# Scan with extensions
python3 direnum.py https://target.com -e php,js,bak,txt

# Recursive scan
python3 direnum.py https://target.com --recursive

# Filter only found pages (200 OK)
python3 direnum.py https://target.com --filter 200

# Custom threads
python3 direnum.py https://target.com -t 20
```

## Options

| Flag | Description |
|------|-------------|
| `-w, --wordlist` | Path to wordlist (default: built-in mini wordlist) |
| `-e, --extensions` | File extensions to scan (comma-separated) |
| `-t, --threads` | Number of threads (default: 10) |
| `-r, --recursive` | Enable recursive crawling |
| `-f, --filter` | Filter by HTTP status code |
| `-o, --output` | Output results to file |
| `-p, --proxy` | Proxy URL |
| `-ua, --user-agent` | Custom user-agent |
| `--depth` | Max crawl depth for recursive mode |

## Examples

```bash
# Find admin panels
python3 direnum.py https://target.com -w wordlists/admin.txt

# Find APIs
python3 direnum.py target.com -e php,js,json,api

# Quiet mode (only show found)
python3 direnum.py target.com -f 200,403 -o results.txt
```

## Wordlists

The tool includes a built-in mini wordlist for quick scans. For comprehensive testing, use:

- [SecLists](https://github.com/danielmiessler/SecLists)
- [dirb wordlists](https://github.com/v0re/dirb)
- [Assetnote](https://wordlists.assetnote.io/)

## License

MIT License