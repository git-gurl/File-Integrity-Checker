# File Integrity Checker 

A Python-based File Integrity Monitoring (FIM) tool that detects unauthorized
file changes using SHA-256 cryptographic hashing.

##  Features
- Baseline creation for directories
- Detects:
  - Modified files
  - Deleted files
  - Newly added files
- Protects baseline from tampering
- Lightweight and dependency-free

##  Requirements
- Python 3.x

##  Usage

### Create Baseline
```bash
python IC.py baseline <directory_path>
