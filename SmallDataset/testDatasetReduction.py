import json
import os
from collections import defaultdict
import random

def process_json_files():
    # Dictionary to store all matching videos, grouped by subject_name
    videos_by_subject = defaultdict(dict)

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
                videos_by_subject[subject_name][video_id] = video_info

        print(f"Processed {json_file}")

    # Create a new dictionary with 10 or fewer entries per subject
    reduced_videos = {}
    for subject, videos in videos_by_subject.items():
        video_ids = list(videos.keys())
        selected_ids = random.sample(video_ids, min(10, len(video_ids)))
        for video_id in selected_ids:
            reduced_videos[video_id] = videos[video_id]
            reduced_videos[video_id]['subject_name'] = subject

    # Create a single JSON file with reduced matching videos
    output_filename = "Minutes_matchingVideosReduced.json"
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(reduced_videos, outfile, indent=2)

    print(f"\nTotal subjects: {len(videos_by_subject)}")
    print(f"Total videos in reduced set: {len(reduced_videos)}")
    print(f"Created {output_filename}")

# Run the function
process_json_files()
