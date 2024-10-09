import json
import os

def process_json_files():
    # Dictionary to store all matching videos
    all_matching_videos = {}

    # Get all *_VideosObject.json files in the current directory
    json_files = [f for f in os.listdir('.') if f.endswith('_VideosObject.json')]

    for json_file in json_files:
        # Extract subject name from the filename and replace leading "_" with "@"
        subject_name = json_file.replace('_VideosObject.json', '')
        if subject_name.startswith('_'):
            subject_name = '@' + subject_name[1:]

        # Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Search through the videos
        for video_id, video_info in data['videos'].items():
            title = video_info['title']
            if ' Min ' in title or ' Mins ' in title or ' Minutes ' in title:
                all_matching_videos[video_id] = {
                    "title": title,
                    "webpage_url": video_info['webpage_url'],
                    "subject_name": subject_name
                }

        print(f"Processed {json_file}")

    # Create a single JSON file with all matching videos
    output_filename = "Minutes_matchingVideosTest.json"
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(all_matching_videos, outfile, indent=2)

    print(f"\nTotal matching videos found: {len(all_matching_videos)}")
    print(f"Created {output_filename}")

# Run the function
process_json_files()
