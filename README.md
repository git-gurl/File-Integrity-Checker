# File Integrity Checker 

A Python-based File Integrity Monitoring (FIM) tool that detects unauthorized
file changes using SHA-256 cryptographic hashing.

This tool helps identify file modification, deletion, addition, and baseline
tampering, making it suitable for cybersecurity monitoring and educational use.

---

##  Features

- Recursive directory scanning
- SHA-256 hashing (memory-safe)
- Baseline creation
- Integrity verification
- Detects:
  - Modified files
  - Deleted files
  - Newly added files
- Baseline tamper detection using lock file
- No external dependencies

---

##  Requirements

- Python 3.x
- Works on Windows, Linux, and macOS

---

##  Project Structure
File-Integrity-Checker/

│
├── IC.py

└── baselines/

    ├── <directory_name>.hash
    
    └── <directory_name>.lock
    

---

##  Usage

### 1️ Create Baseline
Creates a baseline of all files in the target directory.

```bash
python IC.py baseline <directory_path>
```

### 2️ Check File Integrity

Compares current files with the stored baseline.


```bash
python IC.py check <directory_path>
```

## Use Cases

Malware detection

System integrity monitoring

Digital forensics

Cybersecurity lab experiments
