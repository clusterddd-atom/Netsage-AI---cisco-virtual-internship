# NetSage AI 

A Flask-based network troubleshooting dashboard for diagnosing  network issues from simulated command output and audit logs.

## Features

- Upload or enter a network symptom and raw log output
- Run rule-based diagnosis for common  issues
- Review AI or deterministic engine output with confidence and next steps
- Accept, edit, or reject diagnosis results
- View audit metrics and governance telemetry in a dashboard UI

## Project structure

- `app.py` - Flask app and diagnosis logic
- `cases.csv` - sample  troubleshooting cases
- `templates/index.html` - dashboard interface
- `diagnose_prompt.md` - prompt used for AI-style diagnostics

## Prerequisites

- Python 3.9+
- Flask

## Installation

```bash
pip install flask
```

## Run locally

```bash
python app.py
```

Then open:

```text
http://localhost:8080/
```

## Notes

This project is designed as a  networking troubleshooting assistant and demo dashboard for an AI-assisted operations workflow.
