# Using Google's LangExtract and Gemma 3 for Unstructured Document Processing

## Context
- Documents like insurance policies, medical records, and compliance reports are notoriously long and tedious to parse. 
- Important details (e.g., coverage limits and obligations in insurance policies) are buried in dense unstructured text that is challenging for the average person to sift through and digest.
- Large language models (LLMs), already known for their versatility, already serve as powerful tools to cut through this complexity, pulling out the key facts and turning messy documents into clear, structured information.
- In this article, we explore Google's LangExtract framework and its open LLM, Gemma 3, which together make extracting structured information from unstructured text more efficient and accurate.
- To bring this to life, we will also walk through a demo on parsing an insurance policy document, showing how details like exclusion clauses can be surfaced effectively.

## References
- https://github.com/google/langextract
- https://deepmind.google/models/gemma/gemma-3/
