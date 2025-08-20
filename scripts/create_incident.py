import argparse
import requests
from utils import load_config, send_slack_notification

parser = argparse.ArgumentParser(description="Create ServiceNow Incident")
parser.add_argument("--short", required=True, help="Short description")
parser.add_argument("--category", default="software", help="Category")
parser.add_argument("--priority", type=int, default=3, help="Priority (1-5)")
args = parser.parse_args()

config = load_config()
url = f"{config['instance_url']}/api/now/table/incident"
auth = (config['username'], config['password'])
payload = {
    "short_description": args.short,
    "category": args.category,
    "priority": args.priority
}

response = requests.post(url, auth=auth, json=payload)
if response.status_code == 201:
    sys_id = response.json().get("result", {}).get("sys_id")
    print(f"Incident created successfully: {sys_id}")
    send_slack_notification(f":rotating_light: Incident Created: {args.short} (Priority {args.priority})")
else:
    print(f"Error creating incident: {response.status_code} {response.text}")
