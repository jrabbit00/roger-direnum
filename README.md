# Roger DirEnum 🐰

[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Fast, multi-threaded directory and file enumeration for bug bounty hunting and penetration testing.**

Part of the [Roger Toolkit](https://github.com/jrabbit00/roger-recon) - 14 free security tools for bug bounty hunters.

🔥 **[Get the complete toolkit on Gumroad](https://jrabbit00.gumroad.com)** - Support future development!

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

## 🐰 Part of the Roger Toolkit

| Tool | Purpose |
|------|---------|
| [roger-recon](https://github.com/jrabbit00/roger-recon) | All-in-one recon suite |
| [roger-direnum](https://github.com/jrabbit00/roger-direnum) | Directory enumeration |
| [roger-jsgrab](https://github.com/jrabbit00/roger-jsgrab) | JavaScript analysis |
| [roger-sourcemap](https://github.com/jrabbit00/roger-sourcemap) | Source map extraction |
| [roger-paramfind](https://github.com/jrabbit00/roger-paramfind) | Parameter discovery |
| [roger-wayback](https://github.com/jrabbit00/roger-wayback) | Wayback URL enumeration |
| [roger-cors](https://github.com/jrabbit00/roger-cors) | CORS misconfigurations |
| [roger-jwt](https://github.com/jrabbit00/roger-jwt) | JWT security testing |
| [roger-headers](https://github.com/jrabbit00/roger-headers) | Security header scanner |
| [roger-xss](https://github.com/jrabbit00/roger-xss) | XSS vulnerability scanner |
| [roger-sqli](https://github.com/jrabbit00/roger-sqli) | SQL injection scanner |
| [roger-redirect](https://github.com/jrabbit00/roger-redirect) | Open redirect finder |
| [roger-idor](https://github.com/jrabbit00/roger-idor) | IDOR detection |
| [roger-ssrf](https://github.com/jrabbit00/roger-ssrf) | SSRF vulnerability scanner |

## ☕ Support

If Roger DirEnum helps you find bugs, consider [supporting the project](https://github.com/sponsors/jrabbit00)!

## License

MIT License - Created by [Ashlee (Jessica Rabbit)](https://github.com/jrabbit00)