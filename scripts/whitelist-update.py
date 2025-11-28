from pathlib import Path
from datetime import datetime, timezone
import re


def load_domains(path: Path) -> set:
    domains = set()
    for txt_file in path.rglob("*.txt"):
        with txt_file.open("r", encoding="utf-8") as f:
            for line in f:
                # Пропустити порожні та закоментовані рядки.
                if (
                    not line
                    or line.startswith("!")
                    or line.startswith("[")
                    or line.startswith("#")
                ):
                    continue

                # Вилучити домен з формату "0.0.0.0 domain.com"
                if line.startswith("0.0.0.0 "):
                    domain = line[8:].strip()
                    if domain and " " not in domain:
                        domains.add(domain.rstrip("\n"))
                else:
                    # Перевірка на валідність домену
                    if re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}$", line):
                        domains.add(line.rstrip("\n"))
    return domains


def write_whitelist(domains, out_path):
    print(str(len(domains)))
    print(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("#------------------------[UPDATE]------------------------\n")
        f.write("# Title: Whitelist\n")
        f.write(
            f'# Updated:: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}\n'
        )
        f.write(f"# Total number of whitelist urls: {str(len(domains))}\n")
        f.write("# -------------------------[URL]-------------------------\n")
        for d in sorted(domains):
            f.write(f"{d}\n")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    whitelist = sorted(load_domains(Path.joinpath(base_dir, "whitelist-src")))
    # Path.joinpath(base_dir, "release").mkdir(exist_ok=True)
    whitelist_path = str(Path.joinpath(base_dir, "whitelist.txt"))
    write_whitelist(whitelist, whitelist_path)
