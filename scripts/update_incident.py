import argparse
import requests
from utils import load_config, send_slack_notification

parser = argparse.ArgumentParser(description="Update ServiceNow Incident")
parser.add_argument("--sys_id", required=True, help="Incident sys_id")
parser.add_argument("--state", default="in_progress", help="State")
parser.add_argument("--work_notes", default="", help="Work notes")
args = parser.parse_args()

config = load_config()
url = f"{config['instance_url']}/api/now/table/incident/{args.sys_id}"
auth = (config['username'], config['password'])
payload = {
    "state": args.state,
    "work_notes": args.work_notes
}

response = requests.patch(url, auth=auth, json=payload)
if response.status_code == 200:
    print("Incident updated successfully")
    send_slack_notification(f":memo: Incident {args.sys_id} updated: {args.state}")
else:
    print(f"Error updating incident: {response.status_code} {response.text}")
