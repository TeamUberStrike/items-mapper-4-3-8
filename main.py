import json
import re

# file paths
file_4_3_8_txt = "input/items-4-3-8.txt"
file_4_3_8_json = "output/items-4-3-8.json"
file_4_8_6_json = "input/items-4-8-6.json"

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

if __name__ == "__main__":
    data_4_3_8 = convert_input_text_to_json(file_4_3_8_txt, file_4_3_8_json)
    data_4_8_6 = get_4_8_6_data(file_4_8_6_json)
