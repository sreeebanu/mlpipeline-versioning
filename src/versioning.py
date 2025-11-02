import re
from typing import Tuple

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def read_version(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            v = f.read().strip()
            if SEMVER_RE.match(v):
                return v
    except FileNotFoundError:
        pass
    return "0.0.0"


def parse_version(v: str) -> Tuple[int, int, int]:
    m = SEMVER_RE.match(v)
    if not m:
        return 0, 0, 0
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def bump_version_file(path: str, part: str = "patch") -> str:
    """Bump semantic version in the given file. part in ('patch','minor','major').
    Returns new version string.
    """
    major, minor, patch = parse_version(read_version(path))
    if part == "patch":
        patch += 1
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError("part must be 'patch', 'minor' or 'major'")

    new_v = f"{major}.{minor}.{patch}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_v + "\n")
    return new_v
