#!/usr/bin/env python3
import smtplib
import json
import requests
from email.mime.text import MIMEText

def send_email_alert(cfg, subject, body):
    try:
        smtp_server = cfg["smtp_server"]
        port = cfg.get("smtp_port", 587)
        user = cfg.get("smtp_user")
        pwd = cfg.get("smtp_password")
        sender = cfg.get("from")
        to_list = cfg.get("to", [])
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(to_list)

        server = smtplib.SMTP(smtp_server, port, timeout=10)
        server.starttls()
        if user and pwd:
            server.login(user, pwd)
        server.sendmail(sender, to_list, msg.as_string())
        server.quit()
        print("Email alert sent.")
    except Exception as e:
        print("Failed to send email alert:", str(e))

def send_webhook_alert(cfg, title="", text=""):
    try:
        url = cfg.get("url")
        if not url:
            print("Webhook URL missing in config.")
            return
        payload = {"text": f"{title}\n\n{text}"}
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, json=payload, headers=headers, timeout=5)
        r.raise_for_status()
        print("Webhook alert sent.")
    except Exception as e:
        print("Failed to send webhook alert:", str(e))
