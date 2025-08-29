# Using Google's LangExtract and Gemma 3 for Unstructured Document Processing

**Link to article**: https://towardsdatascience.com/using-googles-langextract-and-gemma-for-structured-data-extraction/

## Context
- Documents like insurance policies, medical records, and compliance reports are notoriously long and tedious to parse. 
- Important details (e.g., coverage limits and obligations in insurance policies) are buried in dense unstructured text that is challenging for the average person to sift through and digest.
- Large language models (LLMs), already known for their versatility, already serve as powerful tools to cut through this complexity, pulling out the key facts and turning messy documents into clear, structured information.
- In this article, we explore Google's LangExtract framework and its open LLM, Gemma 3, which together make extracting structured information from unstructured text more efficient and accurate.
- To bring this to life, we will also walk through a demo on parsing an insurance policy document, showing how details like exclusion clauses can be surfaced effectively.

## Files and Folders
- `main.py`: The main script that uses LangExtract and Gemma 3 to process the insurance policy document.
- `data`: Contains the input insurance policy document (`driveshield_specimen_policy_value_plan.pdf`) and the output file (`extraction_results_cleaned.jsonl`) where the extracted information will be saved.
- `utils/parser.py`: Contains utility functions for parsing the PDF document
- `utils/postprocessor.py`: Contains functions for post-processing the extracted data to make it more readable and structured.

## References
- https://github.com/google/langextract
- https://deepmind.google/models/gemma/gemma-3/

