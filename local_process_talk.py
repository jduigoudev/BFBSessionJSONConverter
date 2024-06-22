import json

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
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4, ensure_ascii=False)

print(f"Output written to {output_file_path}")
