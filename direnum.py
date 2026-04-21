#!/usr/bin/env python3
"""
Roger DirEnum - Directory enumeration tool for bug bounty hunting.
"""

import argparse
import concurrent.futures
import requests
import sys
import time
import urllib3
from urllib.parse import urljoin, urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Default mini wordlist
DEFAULT_WORDLIST = [
    # Common directories
    "admin", "administrator", "login", "wp-admin", "adminpanel",
    "backup", "backups", "bak", "old", "archive", "archives",
    "api", "apis", "v1", "v2", "v3",
    "cgi", "cgi-bin",
    "config", "configuration", "conf",
    "dashboard", "panel", "control", "controlpanel",
    "data", "database", "db", "sql",
    "dev", "development", "test", "staging", "stage",
    "files", "download", "downloads", "uploads", "upload",
    "images", "img", "static", "assets",
    "include", "includes", "inc",
    "logs", "log",
    "media",
    "private",
    "public", "pub",
    "resources",
    "server", "server-status",
    "src", "source",
    "tmp", "temp", "cache",
    "tools", "utils",
    # Admin panels
    "phpmyadmin", "pma", "adminer",
    "admin/login", "administrator/login",
    "cpanel",
    "wp-login", "wp-admin",
    "admin.php", "login.php", "admin.html",
    # Files
    "robots.txt", "sitemap.xml", "sitemap.xml.gz",
    ".git/config", ".env", ".htaccess",
    "info.php", "phpinfo.php", "info.php",
    # API paths
    "api/", "api/v1/", "api/v2/",
    "rest/", "graphql",
    "swagger", "docs", "documentation",
    # Common files
    "index.html", "index.php", "index.js",
    "main.html", "main.php",
    "home.html", "home.php",
    "about.html", "about.php",
    "contact.html", "contact.php",
    "login.html", "login.php",
    "register.html", "register.php",
]

# Common extensions
DEFAULT_EXTENSIONS = ["php", "html", "htm", "js", "txt", "bak", "old", "json", "xml", "yaml", "yml", "md", "csv"]

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101",
]

class RogerDirEnum:
    def __init__(self, target, wordlist=None, extensions=None, threads=10, 
                 recursive=False, filter_codes=None, output=None, proxy=None,
                 user_agent=None, depth=3):
        self.target = target.rstrip('/')
        self.wordlist = wordlist or DEFAULT_WORDLIST
        self.extensions = extensions or DEFAULT_EXTENSIONS
        self.threads = threads
        self.recursive = recursive
        self.filter_codes = filter_codes or []
        self.output = output
        self.proxy = proxy
        self.user_agent = user_agent or USER_AGENTS[0]
        self.depth = depth
        self.found = []
        self.session = requests.Session()
        
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}
        
        self.session.headers.update({"User-Agent": self.user_agent})
        
    def load_wordlist(self, path):
        """Load wordlist from file."""
        try:
            with open(path, 'r') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"[!] Wordlist not found: {path}")
            return DEFAULT_WORDLIST
    
    def build_urls(self):
        """Build list of URLs to scan."""
        urls = []
        
        # Add base URL
        urls.append(self.target)
        
        # Add wordlist paths
        for word in self.wordlist:
            # Direct path
            urls.append(f"{self.target}/{word}")
            
            # With extensions
            if self.extensions:
                for ext in self.extensions:
                    if not ext.startswith('.'):
                        ext = f".{ext}"
                    urls.append(f"{self.target}/{word}{ext}")
        
        return list(set(urls))
    
    def check_url(self, url):
        """Check a single URL."""
        try:
            response = self.session.get(url, timeout=10, verify=False, allow_redirects=False)
            status = response.status_code
            
            # Skip if filtering
            if self.filter_codes and status not in self.filter_codes:
                return None
            
            # Check for interesting responses
            if status in [200, 201, 301, 302, 303, 307, 308, 401, 403, 500]:
                content_length = len(response.content)
                title = self.extract_title(response.text) if status == 200 else ""
                
                result = {
                    "url": url,
                    "status": status,
                    "length": content_length,
                    "title": title,
                    "redirect": response.headers.get('Location', '') if status in [301, 302, 307, 308] else ''
                }
                return result
                
        except requests.exceptions.Timeout:
            return {"url": url, "status": "timeout", "error": "Timeout"}
        except requests.exceptions.RequestException as e:
            return {"url": url, "status": "error", "error": str(e)}
        
        return None
    
    def extract_title(self, html):
        """Extract page title from HTML."""
        import re
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if match:
            return match.group(1).strip()[:100]
        return ""
    
    def scan(self):
        """Run the directory enumeration."""
        print(f"[*] Starting directory enumeration on: {self.target}")
        print(f"[*] Using {len(self.wordlist)} paths x {len(self.extensions)} extensions")
        print(f"[*] Threads: {self.threads}")
        print("=" * 60)
        
        # Load custom wordlist if path provided
        if isinstance(self.wordlist, str) and not self.wordlist == DEFAULT_WORDLIST:
            self.wordlist = self.load_wordlist(self.wordlist)
        
        urls = self.build_urls()
        print(f"[*] Total URLs to check: {len(urls)}")
        print()
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_url, url): url for url in urls}
            
            for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                result = future.result()
                if result and result.get("status"):
                    status = result["status"]
                    
                    if isinstance(status, int):
                        # Print progress every 100 requests
                        if i % 100 == 0:
                            print(f"[*] Progress: {i}/{len(urls)}")
                        
                        # Always show 200s and 403s, others optional
                        if status in [200, 403, 401] or not self.filter_codes:
                            print(f"[{status}] {result['url']}")
                            if result.get('redirect'):
                                print(f"  -> {result['redirect']}")
                            if result.get('title'):
                                print(f"  -> {result['title']}")
                            
                            self.found.append(result)
                            
                            # Save to file
                            if self.output:
                                with open(self.output, 'a') as f:
                                    f.write(f"{result['url']} [{status}]\n")
        
        elapsed = time.time() - start_time
        
        print()
        print("=" * 60)
        print(f"[*] Scan complete!")
        print(f"[*] Time: {elapsed:.2f}s")
        print(f"[*] Found: {len(self.found)} URLs")
        
        if self.found:
            print()
            print("[+] Results:")
            for f in self.found:
                status = f["status"]
                if isinstance(status, int):
                    print(f"  [{status}] {f['url']}")
        
        return self.found


def main():
    parser = argparse.ArgumentParser(
        description="Roger DirEnum - Directory enumeration for bug bounty hunting"
    )
    parser.add_argument("target", help="Target URL (e.g., https://target.com)")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file")
    parser.add_argument("-e", "--extensions", help="Comma-separated file extensions")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive crawling")
    parser.add_argument("-f", "--filter", help="Filter by HTTP status codes (comma-separated)")
    parser.add_argument("-o", "--output", help="Output results to file")
    parser.add_argument("-p", "--proxy", help="Proxy URL")
    parser.add_argument("-ua", "--user-agent", help="Custom user-agent")
    parser.add_argument("--depth", type=int, default=3, help="Max crawl depth for recursive mode")
    
    args = parser.parse_args()
    
    # Parse extensions
    extensions = None
    if args.extensions:
        extensions = [e.strip() for e in args.extensions.split(',')]
    
    # Parse filter codes
    filter_codes = []
    if args.filter:
        filter_codes = [int(c.strip()) for c in args.filter.split(',')]
    
    # Run scan
    scanner = RogerDirEnum(
        target=args.target,
        wordlist=args.wordlist,
        extensions=extensions,
        threads=args.threads,
        recursive=args.recursive,
        filter_codes=filter_codes,
        output=args.output,
        proxy=args.proxy,
        user_agent=args.user_agent,
        depth=args.depth
    )
    
    scanner.scan()


if __name__ == "__main__":
    main()