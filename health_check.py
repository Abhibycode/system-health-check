#!/usr/bin/env python3
"""
system-health-check/health_check.py
Run periodic checks and generate JSON reports. Uses psutil.
"""

import os
import json
import socket
import argparse
from datetime import datetime
import psutil
from collections import OrderedDict
from alerter import send_email_alert, send_webhook_alert

DEFAULT_CONFIG = "config.json"

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def get_hostname():
    return socket.gethostname()

def check_cpu():
    return psutil.cpu_percent(interval=1)

def check_memory():
    mem = psutil.virtual_memory()
    return mem.percent, mem.total, mem.available

def check_disk():
    parts = []
    for p in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            continue
        parts.append({
            "mountpoint": p.mountpoint,
            "fstype": p.fstype,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent
        })
    return parts

def top_processes(n=5):
    procs = []
    for p in psutil.process_iter(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        info = p.info
        procs.append(info)
    procs_sorted = sorted(procs, key=lambda x: (x.get('cpu_percent',0) or 0)+(x.get('memory_percent',0) or 0), reverse=True)
    return procs_sorted[:n]

def network_stats():
    io = psutil.net_io_counters(pernic=False)
    return {"bytes_sent": io.bytes_sent, "bytes_recv": io.bytes_recv, "packets_sent": io.packets_sent, "packets_recv": io.packets_recv}

def check_services(service_names):
    status = {}
    names_lower = [s.lower() for s in service_names]
    for s in names_lower:
        found = False
        for p in psutil.process_iter(attrs=['name']):
            try:
                if p.info['name'] and s in p.info['name'].lower():
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        status[s] = "running" if found else "stopped"
    return status

def build_report(cfg):
    report = OrderedDict()
    report['timestamp'] = datetime.utcnow().isoformat() + "Z"
    report['hostname'] = get_hostname()
    report['cpu_percent'] = check_cpu()
    mem_percent, mem_total, mem_avail = check_memory()
    report['memory'] = {"percent": mem_percent, "total_bytes": mem_total, "available_bytes": mem_avail}
    report['disk'] = check_disk()
    report['top_processes'] = top_processes(cfg.get("thresholds", {}).get("top_process_count", 5))
    report['network'] = network_stats()
    report['services'] = check_services(cfg.get("services_to_check", []))
    return report

def evaluate_alerts(report, cfg):
    alerts = []
    thr = cfg.get("thresholds", {})
    if report['cpu_percent'] >= thr.get("cpu_percent", 85):
        alerts.append(f"CPU usage high: {report['cpu_percent']}%")

    if report['memory']['percent'] >= thr.get("memory_percent", 80):
        alerts.append(f"Memory usage high: {report['memory']['percent']}%")

    for d in report['disk']:
        if d['percent'] >= thr.get("disk_percent", 90):
            alerts.append(f"Disk {d['mountpoint']} usage high: {d['percent']}%")

    stopped_services = [s for s, st in report['services'].items() if st != "running"]
    if stopped_services:
        alerts.append(f"Stopped services: {', '.join(stopped_services)}")

    return alerts

def save_report(report, report_dir):
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)
    fname = datetime.utcnow().strftime("health_report_%Y-%m-%dT%H-%M-%SZ.json")
    path = os.path.join(report_dir, fname)
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return path

def main(config_path):
    cfg = load_config(config_path)
    report = build_report(cfg)
    report_path = save_report(report, cfg.get("report_dir", "sample_reports"))
    alerts = evaluate_alerts(report, cfg)

    if alerts:
        body = f"Health check alerts for {report['hostname']} at {report['timestamp']}:\n\n" + "\n".join(alerts)
        if cfg.get("email_alert", {}).get("enabled", False):
            send_email_alert(cfg["email_alert"], subject=f"[ALERT] {report['hostname']}", body=body)
        if cfg.get("webhook_alert", {}).get("enabled", False):
            send_webhook_alert(cfg["webhook_alert"], title=f"[ALERT] {report['hostname']}", text=body)

    print(f"Report saved: {report_path}")
    if alerts:
        print("Alerts:", alerts)
    else:
        print("No alerts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run system health check")
    parser.add_argument("--config", "-c", default=DEFAULT_CONFIG, help="Path to config.json")
    args = parser.parse_args()
    main(args.config)
