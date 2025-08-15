import langextract as lx
import textwrap

from utils.parser import PDFProcessor

prompt = textwrap.dedent("""\
    Extract all entities, roles, clauses, and conditions from this insurance policy in the order they appear.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    For each, add brief attributes such as:
        - Role / Type (party, coverage clause, exclusion, condition)
        - Trigger / Event (what activates it)
        - Limitations (restrictions, caps, time limits)
    """)

examples = [
    lx.data.ExampleData(
        text="The Insurer agrees to indemnify the Insured against loss or damage to the Property caused by Fire, subject to the exclusions set forth in Section 5.",
        extractions=[
            lx.data.Extraction(
                extraction_class="entity",
                extraction_text="The Insurer",
                attributes={"role": "party", "description": "Provides coverage"}
            ),
            lx.data.Extraction(
                extraction_class="entity",
                extraction_text="the Insured",
                attributes={"role": "party", "description": "Receives coverage"}
            ),
            lx.data.Extraction(
                extraction_class="clause",
                extraction_text="indemnify the Insured against loss or damage to the Property",
                attributes={"type": "coverage", "trigger_event": "loss or damage to the Property"}
            ),
            lx.data.Extraction(
                extraction_class="condition",
                extraction_text="caused by Fire",
                attributes={"type": "trigger", "cause": "Fire"}
            ),
            lx.data.Extraction(
                extraction_class="limitation",
                extraction_text="subject to the exclusions set forth in Section 5",
                attributes={"type": "exclusion_reference", "location": "Section 5"}
            ),
        ]
    )
]

if __name__ == "__main__":
    file_path = "data/driveshield_specimen_policy_value_plan.pdf"
    processor = PDFProcessor(file_path)

    # Create visualizations (stored in images/)
    processor.visualize_all_pages()

    # Get concatenated text
    input_text = processor.get_all_text()

    # result = lx.extract(
    #     text_or_documents=input_text,
    #     prompt_description=prompt,
    #     examples=examples,
    #     model_id="gemini-2.5-flash"
    # )

    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        model_id="gemma3:4b",  # Automatically selects Ollama provider
        model_url="http://localhost:11434",
        fence_output=False,
        use_schema_constraints=False
    )

    # Save results to file
    with open("extracted_entities.txt", "w", encoding="utf-8") as f:
        f.write(f"Extracted {len(result.extractions)} entities:\n\n")
        for extraction in result.extractions:
            f.write(f"• {extraction.extraction_class}: '{extraction.extraction_text}'\n")
            if extraction.attributes:
                for key, value in extraction.attributes.items():
                    f.write(f"  - {key}: {value}\n")

    print("Extraction results saved to extracted_entities.txt")