import json
import unidecode

# Input and output file paths
input_file_path = 'talks.json'
output_file_path = 'openfeedback_output.json'

# Read the JSON data from the input file
with open(input_file_path, 'r', encoding='utf-8') as infile:
    input_data = json.load(infile)

# Initialize the output data structure
output_data = {
    "sessions": {},
    "speakers": {}
}

# Default photo URL and social links for speakers
default_photo_url = "https://www.breizhcamp.org/img/logo.png"
default_socials = [
    {
        "name": "twitter",
        "link": "https://x.com/i/flow/login?redirect_after_login=%2Fbreizhcamp"
    }
]

# Function to generate a unique speaker ID for each session
def generate_speaker_id(name, session_id):
    # Normalize the name and append session ID to ensure uniqueness
    normalized_name = unidecode.unidecode(name)
    return f"{normalized_name.lower().replace(' ', '_')}_{session_id}"

# Process each session in the input data
for session in input_data:
    session_id = session["id"]
    speaker_name = session["speakers"]

    # Generate a unique speaker ID for each session
    speaker_id = generate_speaker_id(speaker_name, session_id)

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

    # Add speaker details to output data
    output_data["speakers"][speaker_id] = {
        "name": speaker_name,
        "photoUrl": default_photo_url,
        "socials": default_socials,
        "id": speaker_id
    }

# Write the JSON output to a file formatted for OpenFeedback
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4, ensure_ascii=False)

# Print the number of sessions and speakers
num_sessions = len(output_data["sessions"])
num_speakers = len(output_data["speakers"])

print(f"Output written to {output_file_path}")
print(f"Number of sessions: {num_sessions}")
print(f"Number of speakers: {num_speakers}")

# Explanation:
# For OpenFeedback, we need to have a one-to-one mapping between sessions and speakers.
# This is why each session gets a unique speaker entry, even if the speaker is the same.
# This ensures that every session has a corresponding speaker entry, meeting OpenFeedback's requirements.
# Each speaker entry now includes a default 'photoUrl' and 'socials' to avoid any potential issues 
# during the data import process into OpenFeedback.