import sys
from datetime import datetime, timedelta, timezone
import re
import requests
import os

def read_lines(path):
    if path.startswith("http://") or path.startswith("https://"):
        try:
            response = requests.get(path)
            response.encoding = 'utf-8'
            return response.text.splitlines()
        except Exception as e:
            print(f"Error fetching {path}: {e}")
            return []
    elif os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()
    else:
        print(f"Invalid path: {path}")
        return []

def convert(sources_file, output_path):
    domains = set()

    # 读取源列表文件
    with open(sources_file, 'r', encoding='utf-8') as f:
        source_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for url in source_urls:
        lines = read_lines(url)
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue

            if line.startswith("+."):
                domain = line[2:]
            elif line.startswith("address=/"):
                match = re.match(r"address=/([^/]+)/", line)
                domain = match.group(1) if match else None
            elif line.startswith("||"):
                domain = line.split("^")[0][2:]
            elif re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]+$", line):
                domain = line
            else:
                domain = None

            if domain:
                domains.add(domain)

    domains = sorted(domains)
    count = len(domains)

    now = datetime.now(timezone.utc) + timedelta(hours=8)
    update_time = now.strftime("# Update: %Y-%m-%d %H:%M:%S (GMT+8)")
    stat_line = f"# Total domains: {count}"

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(update_time + '\n')
        out.write(stat_line + '\n\n')
        for domain in domains:
            out.write(f"127.0.0.1 {domain}\n")
            out.write(f"::1 {domain}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_to_hosts.py <sources.txt> <output>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
