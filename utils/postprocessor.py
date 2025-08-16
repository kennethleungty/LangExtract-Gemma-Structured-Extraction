import json
import os

def postprocess_extractions(filename):
    with open(filename, "r") as f:
        content = f.read().strip()
    
    # Try parsing as a JSON array
    try:
        data = json.loads(content)
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
    except json.JSONDecodeError:
        # Fallback: parse concatenated JSON objects
        entries = []
        decoder = json.JSONDecoder()
        idx = 0
        while idx < len(content):
            obj, offset = decoder.raw_decode(content[idx:])
            entries.append(obj)
            idx += offset
            while idx < len(content) and content[idx].isspace():
                idx += 1
    
    # Process each entry and filter for exclusion extractions only
    simplified_entries = []
    for entry in entries:
        simplified_entry = {
            k: v for k, v in entry.items() if k != "extractions"
        }
        
        simplified_extractions = []
        for extraction in entry.get("extractions", []):
            # Only keep extractions with extraction_class "exclusion"
            if extraction.get("extraction_class") == "exclusion":
                simplified = {
                    "extraction_class": extraction.get("extraction_class"),
                    "extraction_text": extraction.get("extraction_text"),
                }
                
                attributes = extraction.get("attributes", {})
                if isinstance(attributes, dict):
                    simplified.update(attributes)
                
                simplified_extractions.append(simplified)
        
        # Only add the entry if it has exclusion extractions
        if simplified_extractions:
            simplified_entry["extractions"] = simplified_extractions
            simplified_entries.append(simplified_entry)
    
    # Write to new file
    base, _ = os.path.splitext(filename)
    output_file = f"{base}_cleaned.jsonl"
    
    with open(output_file, "w") as f:
        for entry in simplified_entries:
            json.dump(entry, f, indent=4)
            f.write("\n")
    
    print(f"Exclusion-only entries saved to: {output_file}")
    print(f"Found {len(simplified_entries)} entries with exclusion extractions")
