import json

def find_titles_with_minutes(json_file):
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # List to store matching titles
    matching_titles = []

    # Search through the videos
    for video_id, video_info in data['videos'].items():
        title = video_info['title']
        if ' Min ' in title or ' Mins ' in title or ' Minutes ' in title:
            matching_titles.append(title)

    # Print the matching titles
    print("Titles containing 'Min', 'Mins', or 'Minutes':")
    for title in matching_titles:
        print(f"- {title}")

    # Print the total count
    print(f"\nTotal matching titles: {len(matching_titles)}")

# Usage
json_file = '_OFFICIALTHENXSTUDIOS_VideosObject.json'  # Replace with your JSON file name if different
find_titles_with_minutes(json_file)
