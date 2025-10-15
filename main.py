import json
import re

# file paths
file_4_3_8_txt = "input/items-4-3-8.txt"
file_4_3_8_json = "output/items-4-3-8.json"
file_4_8_6_json = "input/items-4-8-6.json"
manual_item_mappings_json = "input/manual-item-mappings.json"
mapped_item_ids_json = "output/mapped-item-ids.json"
missed_item_ids_json = "output/missed-item-ids.json"
total_mapped_item_ids_json = "output/total-mapped-item-ids.json"

def convert_input_text_to_json(input_file, output_file):
    data = {}
    # Read and parse lines
    with open(input_file, "r") as f:
        for line in f:
            # Match lines like: { 1000, "Splatbat" },
            match = re.match(r'\s*\{\s*(\d+)\s*,\s*"((?:[^"\\]|\\.)*)"\s*\},?', line)
            if match:
                key, raw_value = match.groups()
                value = bytes(raw_value, "utf-8").decode("unicode_escape")
                data[key] = value
            else:
                raise ValueError("could not parse line: " + line)

    # Write to JSON
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Converted {len(data)} entries to {output_file}")
    return data

def get_4_8_6_data(file):
    with open(file, "r") as f:
        return json.load(f)
    
def map_item_ids(data_4_3_8, data_4_8_6):
    mapped_item_ids = {}

    items_list_4_8_6 = []
    for key, value in data_4_8_6.items():
        if isinstance(value, list):
            items_list_4_8_6.extend(value)

    for item_id_4_3_8, item_name_4_3_8 in data_4_3_8.items():
        for item_4_8_6 in items_list_4_8_6:
            if item_4_8_6["Name"] == item_name_4_3_8:
                mapped_item_ids[item_id_4_3_8] = item_4_8_6["ID"]

    with open(mapped_item_ids_json, "w") as f:
        json.dump(mapped_item_ids, f, indent=4)
    print(f"Automatically mapped {len(mapped_item_ids)} item ids from 4.3.8 to 4.8.6, written to {mapped_item_ids_json}")

    missed_item_ids = {}
    for key in data_4_3_8.keys():
        if key not in mapped_item_ids:
            missed_item_ids[key] = 0

    with open(missed_item_ids_json, "w") as f:
        json.dump(missed_item_ids, f, indent=4)
    print(f"Missed {len(missed_item_ids)} item ids from 4.3.8 to 4.8.6, written to {missed_item_ids_json}")

    return mapped_item_ids, missed_item_ids

def add_automatically_with_manual_mapped_item_ids(mapped_item_ids, manual_mapped_item_ids):
    total_mapped_item_ids = {}
    total_mapped_item_ids = mapped_item_ids | manual_mapped_item_ids

    with open(total_mapped_item_ids_json, "w") as f:
        json.dump(total_mapped_item_ids, f, indent=4)
    print(f"Total mapped item ids: {len(total_mapped_item_ids)}, written to {total_mapped_item_ids_json}")

def get_manual_mapped_item_ids(file):
    with open(file, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    data_4_3_8 = convert_input_text_to_json(file_4_3_8_txt, file_4_3_8_json)
    data_4_8_6 = get_4_8_6_data(file_4_8_6_json)
    mapped_item_ids, missed_item_ids = map_item_ids(data_4_3_8, data_4_8_6)
    manual_mapped_item_ids = get_manual_mapped_item_ids(manual_item_mappings_json)
    add_automatically_with_manual_mapped_item_ids(mapped_item_ids, manual_mapped_item_ids)

