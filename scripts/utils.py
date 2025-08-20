import os
import json
import requests

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {
        "instance_url": os.getenv("SN_INSTANCE_URL"),
        "username": os.getenv("SN_USERNAME"),
        "password": os.getenv("SN_PASSWORD"),
        "slack_webhook": os.getenv("SLACK_WEBHOOK")
    }

def send_slack_notification(message):
    config = load_config()
    webhook_url = config.get("slack_webhook")
    if webhook_url:
        payload = {"text": message}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"Slack notification failed: {e}")
