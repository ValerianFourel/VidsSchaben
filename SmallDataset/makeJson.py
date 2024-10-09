import json
import re

def parse_entry(entry):
    pattern = r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(\d+|\w+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*([\w-]+)\s*\|\s*(https?://\S+)\s*\|\s*(.*?)\s*\_/'
    match = re.match(pattern, entry, re.DOTALL)
    if not match:
        print(f"Failed to parse entry: {entry}...")  # Print first 100 chars of failed entry
        return None

    return {
        "upload_date": match.group(1),
        "duration": match.group(2),
        "view_count": match.group(3),
        "like_count": match.group(4),
        "title": match.group(5),
        "id": match.group(6),
        "webpage_url": match.group(7),
        "description": match.group(8).strip()
    }

def process_file(filename):
    data = {"videos": {}, "urls": {}}

    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        print(f"File content length: {len(content)} characters")
        entries = content.split('\_/')
        print(f"Number of entries after split: {len(entries)}")

        for i, entry in enumerate(entries):
            entry = entry.strip()
            if entry:
                parsed_entry = parse_entry(entry + ' \_/')  # Add back the separator for parsing
                if parsed_entry:
                    video_id = parsed_entry["id"]
                    webpage_url = parsed_entry["webpage_url"]

                    data["videos"][video_id] = parsed_entry
                    data["urls"][webpage_url] = video_id
            else:
                print(f"Empty entry at index {i}")

    print(f"Processed videos: {len(data['videos'])}")
    print(f"Processed URLs: {len(data['urls'])}")
    return data

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Usage
input_file = 'list_OFFICIALTHENXSTUDIOS_VideosSmallDataset.txt'
output_file = '_OFFICIALTHENXSTUDIOS_VideosObject.json'

data = process_file(input_file)
save_json(data, output_file)

print(f"JSON file has been created: {output_file}")
