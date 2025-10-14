import json
import re

# Input and output file paths
input_file = "input/items-4-3-8.txt"
output_file = "output/items-4-3-8.json"

data = {}

# Read and parse lines
with open(input_file, "r") as f:
    for line in f:
        # Match lines like: { 1000, "Splatbat" },
        match = re.match(r'\s*\{\s*(\d+)\s*,\s*"((?:[^"\\]|\\.)*)"\s*\},?', line)
        if match:
            key, value = match.groups()
            data[key] = value
        else:
            raise ValueError("could not parse line: " + line)

# Write to JSON
with open(output_file, "w") as f:
    json.dump(data, f, indent=4)

print(f"Converted {len(data)} entries to {output_file}")

