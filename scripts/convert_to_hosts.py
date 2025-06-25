import sys
from datetime import datetime, timedelta, timezone

def convert(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    domains = set()
    for line in lines:
        line = line.strip()
        if line.startswith("+."):
            domain = line[2:]
            if domain:
                domains.add(domain)

    domains = sorted(domains)
    count = len(domains)

    # 获取北京时间（UTC+8）
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
        print("Usage: python3 convert_to_hosts.py <input> <output>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
