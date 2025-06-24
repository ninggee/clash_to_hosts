import sys

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

    with open(output_path, 'w', encoding='utf-8') as out:
        for domain in sorted(domains):
            out.write(f"127.0.0.1 {domain}\n")
            out.write(f"::1 {domain}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python3 convert_to_hosts.py 输入路径 输出路径")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
