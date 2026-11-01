"""Find files with identical SHA-256 hashes. Never deletes files."""
import argparse
import hashlib
import json
import os
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("folder", type=Path)
a = p.parse_args()
if not a.folder.is_dir():
    p.error("folder must be an existing directory")

groups, errors = {}, []

def walk_error(error):
    errors.append(str(error))

for directory, dirs, files in os.walk(
    a.folder, onerror=walk_error, followlinks=False
):
    dirs[:] = sorted(
        d for d in dirs if not Path(directory, d).is_symlink()
    )
    for name in sorted(files):
        path = Path(directory, name)
        if path.is_symlink() or not path.is_file():
            continue
        try:
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1048576), b""):
                    digest.update(chunk)
            groups.setdefault(digest.hexdigest(), []).append(str(path))
        except OSError as error:
            errors.append(f"{path}: {error}")

print(json.dumps({
    "duplicates": [v for v in groups.values() if len(v) > 1],
    "errors": errors
}, indent=2))
raise SystemExit(2 if errors else 0)