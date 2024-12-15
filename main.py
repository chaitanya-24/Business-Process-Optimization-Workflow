import requests
import json

# Replace with your API Gateway endpoint
api_endpoint = "[API_ENDPOINT]"

# Sample input data
payload = {
    "process_data": "The sales process includes lead generation, qualification, proposal, negotiation, and closing. Currently, leads are not being followed up on promptly, and there are delays in proposal generation due to manual processes"
}

# Send POST request to API
response = requests.post(api_endpoint, json=payload)

# Print the response
if response.status_code == 200:
    print("Workflow Suggestions:\n", json.dumps(response.json(), indent=4))
else:
    print(f"Failed with status code: {response.status_code}, Response: {response.text}")
