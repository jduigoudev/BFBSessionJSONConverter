import json
import requests
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Suppress NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# URL of the JSON data
url = "https://www.breizhcamp.org/json/talks.json"

# Fetch the JSON data from the URL
response = requests.get(url)
input_data = response.json()

# Initialize the output data structure
output_data = {
    "sessions": {},
    "speakers": {}
}

# Function to generate a unique speaker ID
def generate_speaker_id(name):
    return name.lower().replace(" ", "_")

# Process each session in the input data
for session in input_data:
    session_id = session["id"]
    speaker_name = session["speakers"]

    # Generate speaker ID
    speaker_id = generate_speaker_id(speaker_name)

    # Add session details to output data
    output_data["sessions"][session_id] = {
        "speakers": [speaker_id],
        "tags": [session["format"]],
        "title": session["name"],
        "id": session_id,
        "startTime": session["event_start"],
        "endTime": session["event_end"],
        "trackTitle": session["venue"]
    }

    # Add speaker details to output data, even all set to nullity 
    if speaker_id not in output_data["speakers"]:
        output_data["speakers"][speaker_id] = {
            "name": speaker_name,
            "photoUrl": None,
            "socials": None,
            "id": speaker_id
        }

# Write the JSON output to a file formatted for OpenFeedback
with open('openfeedback_output.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4, ensure_ascii=False)
