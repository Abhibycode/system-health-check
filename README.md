# System Health Check

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/abhishek-kongari/system-health-check/actions/workflows/ci.yml/badge.svg)](https://github.com/abhishek-kongari/system-health-check/actions)

## Overview
A lightweight system health checker designed for support, SRE and cloud engineers. It collects CPU, memory, disk, network, and service status, produces timestamped JSON reports, and sends alerts via SMTP or webhooks if thresholds are exceeded.

This project demonstrates automation, monitoring, and production-readiness — matching typical responsibilities for Application/Cloud Support roles.

## Features
- CPU, memory, disk, network, and top process checks
- Service presence checks
- Threshold-based alerts (email & webhook)
- JSON report outputs (timestamped)
- Docker image & docker-compose for demo
- systemd service + timer example to schedule runs
- GitHub Actions CI for smoke runs

## Quick start

### 1. Clone
```bash
git clone https://github.com/abhishek-kongari/system-health-check.git
cd system-health-check



2️⃣ Create & Activate Virtual Environment
Windows:
python -m venv .venv
.venv\Scripts\activate

Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Configure the Tool

Copy the example config:

cp config.example.json config.json


Now edit the config file:

nano config.json

You can configure:

Thresholds (CPU %, Memory %, Disk %, top N processes)

Services to check

Enable/disable email alerts

Enable/disable webhook alerts

Tip: Keep alerts disabled during first run.

5️⃣ Run Health Check Locally
python health_check.py --config config.json

Output:

A JSON file inside sample_reports/

Alerts printed on console (if thresholds exceeded)

Email/Webhook alerts sent (if enabled)

Example output location:

sample_reports/health_report_2025-12-05T06-35-22Z.json

🎯 Optional: View the Report
cat sample_reports/*.json | jq


(jq is optional but formats JSON nicely.)

🐳 Run Using Docker
Build Image:
docker build -t system-health-check -f docker/Dockerfile .

Run Container:
docker run --rm \
  -v $(pwd)/sample_reports:/app/sample_reports \
  -v $(pwd)/config.json:/app/config.json \
  system-health-check

🔄 Run Automatically via systemd (Linux Server)

Copy files:

sudo cp systemd/health-check.service /etc/systemd/system/
sudo cp systemd/health-check.timer /etc/systemd/system/


Edit paths inside the files:

/opt/system-health-check/


Reload & enable timer:

sudo systemctl daemon-reload
sudo systemctl enable --now health-check.timer


Check logs:

journalctl -u health-check.service -f

📁 Project Structure
system-health-check/
├── health_check.py
├── alerter.py
├── config.example.json
├── requirements.txt
├── sample_reports/
├── docker/
│   └── Dockerfile
├── systemd/
│   ├── health-check.service
│   └── health-check.timer
└── .github/workflows/ci.yml
