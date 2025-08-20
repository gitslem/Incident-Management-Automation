import argparse
import requests
from utils import load_config, send_slack_notification

parser = argparse.ArgumentParser(description="Close ServiceNow Incident")
parser.add_argument("--sys_id", required=True, help="Incident sys_id")
parser.add_argument("--close_notes", default="Resolved", help="Close notes")
args = parser.parse_args()

config = load_config()
url = f"{config['instance_url']}/api/now/table/incident/{args.sys_id}"
auth = (config['username'], config['password'])
payload = {
    "state": "closed",
    "close_notes": args.close_notes
}

response = requests.patch(url, auth=auth, json=payload)
if response.status_code == 200:
    print("Incident closed successfully")
    send_slack_notification(f":white_check_mark: Incident {args.sys_id} closed: {args.close_notes}")
else:
    print(f"Error closing incident: {response.status_code} {response.text}")
