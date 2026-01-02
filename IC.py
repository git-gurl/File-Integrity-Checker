# Usage:
# 1) python IC.py baseline <directory_path>
# 2) python IC.py check <directory_path>

import os
import sys
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASELINE_DIR = os.path.join(BASE_DIR, "baselines")

os.makedirs(BASELINE_DIR, exist_ok=True)

def sha256(filepath):
    """Compute SHA-256 hash (memory-safe)."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None

def safe_name(path):
    """Create safe filename from directory path."""
    return os.path.basename(os.path.abspath(path)).replace(" ", "_")

def scan_directory(directory):
    files = {}
    for root, _, filenames in os.walk(directory):
        for name in filenames:
            path = os.path.join(root, name)

            # Skip scanner & baselines
            if BASE_DIR in os.path.abspath(path):
                continue

            h = sha256(path)
            if h:
                files[path] = h
    return files

def baseline_files(directory):
    name = safe_name(directory)
    return (
        os.path.join(BASELINE_DIR, f"{name}.hash"),
        os.path.join(BASELINE_DIR, f"{name}.lock")
    )

def create_baseline(directory):
    basefile, lockfile = baseline_files(directory)
    files = scan_directory(directory)

    with open(basefile, "w") as f:
        for p, h in files.items():
            f.write(f"{p}|{h}\n")

    with open(lockfile, "w") as f:
        f.write(sha256(basefile))

    print(f"[OK] Baseline created for '{directory}'")
    print(f"     Files monitored: {len(files)}")

def check_integrity(directory):
    basefile, lockfile = baseline_files(directory)

    if not os.path.exists(basefile) or not os.path.exists(lockfile):
        print("[ERROR] No baseline found. Run baseline first.")
        return

    if sha256(basefile) != open(lockfile).read().strip():
        print("[CRITICAL] Baseline has been tampered with!")
        return

    baseline = {}
    with open(basefile) as f:
        for line in f:
            path, h = line.strip().split("|")
            baseline[path] = h

    current = scan_directory(directory)

    print("\n--- Integrity Check Results ---")

    for p in baseline:
        if p not in current:
            print(f"[MISSING]  {p}")
        elif baseline[p] != current[p]:
            print(f"[MODIFIED] {p}")

    for p in current:
        if p not in baseline:
            print(f"[NEW]      {p}")

    print("\n[OK] Scan completed.")

# ---------------- MAIN ----------------

if len(sys.argv) != 3 or sys.argv[1] not in ("baseline", "check"):
    print("Usage:")
    print("  python IC.py baseline <directory_path>")
    print("  python IC.py check <directory_path>")
    sys.exit()

mode, target_dir = sys.argv[1], sys.argv[2]

if not os.path.isdir(target_dir):
    print("[ERROR] Target directory does not exist.")
    sys.exit()

if mode == "baseline":
    create_baseline(target_dir)
else:
    check_integrity(target_dir)
