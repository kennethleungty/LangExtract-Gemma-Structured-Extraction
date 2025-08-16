import json
import os

def prettify_and_filter_jsonl_file(filename):
    with open(filename, "r") as f:
        content = f.read().strip()

    # Try parsing as a JSON array
    try:
        data = json.loads(content)
        if isinstance(data, list):
            objects = data
        else:
            objects = [data]
    except json.JSONDecodeError:
        # Fallback: parse concatenated JSON objects
        objects = []
        decoder = json.JSONDecoder()
        idx = 0
        while idx < len(content):
            obj, offset = decoder.raw_decode(content[idx:])
            objects.append(obj)
            idx += offset
            while idx < len(content) and content[idx].isspace():
                idx += 1

    # Extract and filter fields
    simplified_objects = []
    for obj in objects:
        if "extractions" in obj and isinstance(obj["extractions"], list):
            for extraction in obj["extractions"]:
                simplified = {
                    "extraction_class": extraction.get("extraction_class"),
                    "extraction_text": extraction.get("extraction_text"),
                }
                attributes = extraction.get("attributes", {})
                if isinstance(attributes, dict):
                    simplified.update(attributes)
                simplified_objects.append(simplified)

    # Determine output filename
    base, ext = os.path.splitext(filename)
    output_file = f"{base}_simplified.jsonl"

    # Write simplified and prettified output
    with open(output_file, "w") as f:
        for obj in simplified_objects:
            json.dump(obj, f, indent=4)
            f.write("\n")

    print(f"Simplified output saved to: {output_file}")

# Example usage
prettify_and_filter_jsonl_file("extraction_results.jsonl")
