import langextract as lx
import textwrap

from utils.parser import PDFProcessor
from utils.postprocessor import postprocess_extractions


prompt = textwrap.dedent("""\
    Extract key insurance information and explain it in customer-friendly terms.
    
    Focus solely on EXCLUSIONS i.e., what is NOT covered by the policy.

    Use exact text for extractions. Do not paraphrase or overlap entities.

    Provide meaningful relevant attributes for each entity to add context.
                         
    Where appropriate, include a plain english explanation that layman can understand. Do not hallucinate and make up fake information.

    Return your answer as a JSON object with this format:
    {
        "extractions": [
            {
                "extraction_class": "exclusion",
                "extraction_text": "exact text from the policy document",
                "attributes": {...}
            }
        ]
    }
    """)

examples = [
    lx.data.ExampleData(
        text="This policy does not cover damage caused by floods, earthquakes, or nuclear accidents.",
        extractions=[
            lx.data.Extraction(
                extraction_class="exclusion",
                extraction_text="floods",
                attributes={
                    "plain_english": "Flood damage is not covered - you need separate flood insurance",
                },
            ),
            lx.data.Extraction(
                extraction_class="exclusion",
                extraction_text="earthquakes",
                attributes={
                    "plain_english": "Earthquake damage is not covered - you need separate earthquake insurance",
                },
            ),
            lx.data.Extraction(
                extraction_class="exclusion",
                extraction_text="nuclear accidents",
                attributes={
                    "plain_english": "Nuclear accident damage is not covered - you need separate nuclear accident insurance",
                }
            ),
        ]
    ),
]


if __name__ == "__main__":
    file_path = "data/input/driveshield_specimen_policy_value_plan.pdf"
    # file_path = "data/input/driveshield_specimen_policy_value_plan-3.pdf"
    output_filename = "data/output/extraction_results.jsonl"
    processor = PDFProcessor(file_path)

    # Create visualizations (stored in images/)
    processor.visualize_all_pages()

    # Get concatenated text
    input_text = processor.get_all_text()

    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        model_id="gemma3:4b",  
        model_url="http://localhost:11434",  # Endpoint URL for self-hosted model. Default Ollama server URL is used here.
        fence_output=False,  # Whether to expect/generate fenced output (```json or ```yaml). When True, model is prompted to generate fenced output and the resolver expects it. When False, raw JSON/YAML is expected.
        use_schema_constraints=False,  # Whether to generate schema constraints for models. LangExtract doesn't implement schema constraints for Ollama models yet
        max_char_buffer=2000,  # Max number of characters for inference
        extraction_passes=2,  # Number of sequential extraction attempts to improve recall and find additional entities. Defaults to 1 (standard single extraction). When > 1, the system performs multiple independent extractions and merges non-overlapping results.
        temperature=0.0
    )

    print(f"Extraction results saved to extracted_entities.json")
    lx.io.save_annotated_documents([result], 
                                   output_name=output_filename, 
                                   output_dir=".")

    # Generate simplified JSON output
    postprocess_extractions(output_filename)
