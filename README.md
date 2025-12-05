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
