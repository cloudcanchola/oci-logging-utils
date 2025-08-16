# OCI Logging Utils (IAM Audit Reports)
Repository to upload OCI scripts to extend logging limitations.


## Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Environment Configuration](#-environment-configuration)
- [Usage](#-usage)

---

## 🚀 Features

---


- [Audit Reports](https://docs.oracle.com/en/learn/generating-iam-reports-from-oci-audit/index.html) – Generates OCI IAM audit reports based with a 92 max limit.

---

## 📂 Project Structure
```
project-root/
├── scripts/ 
├── utils/ 
├── .env
├── README.md # Project documentation
└── requirements.txt # Dependencies (Python example)
```

---

## ⚙️ Environment Configuration

In case you would like to configure .env and create config from those variables 

```bash
USER=ocid1.user.oc1..xxxxx
FINGERPRINT=xx:xx:xx:xx
TENANCY=ocid1.tenancy.oc1..xxxxx
REGION=us-ashburn-1
KEY_FILE=path_to_key_file
```

---

## ▶️ Usage

Run the script as module using -m

```bash
 python -m scripts.audit_reports \
 --time-start 2025-01-01 \
 --time-end 2025-03-30 --type roles \
 ```


```bash
usage: audit_reports.py [-h] --time-start TIME_START --time-end TIME_END --type
                        {Report.audit,Report.roles,Report.access,Report.fail,Report.success,Report.delivery_failure}
                        [-o OUTPUT_DIR] [--log-level LOG_LEVEL] [--compartment COMPARTMENT]

options:
  -h, --help            show this help message and exit
  --time-start TIME_START
  --time-end TIME_END
  --type {Report.audit,Report.roles,Report.access,Report.fail,Report.success,Report.delivery_failure}
                        Report type
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output folder for the CSV file (default: ./reports).
  --log-level LOG_LEVEL
                        Log level: DEBUG|INFO|WARNING|ERROR|CRITICAL (default: INFO).
  --compartment COMPARTMENT
                        Specify the compartment where an identity domain exists.
```
---

