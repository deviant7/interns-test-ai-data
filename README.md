## Hybrid Concept Extraction Strategy in `main.py`

The `main.py` script implements a domain-flexible, hybrid strategy for extracting concepts from textual data. The process includes the following key components:

### 1. Capitalized Phrase Detection
- Identifies multi-word proper noun sequences.
- Example: `"Harappan Civilization"`, `"Mauryan Empire"`.

### 2. Keyword-to-Concept Mapping
- Utilizes a subject-specific dictionary to map known terms to canonical concept labels.

### 3. Fallback Heuristic
- If neither of the above methods returns a result:
  - Selects up to **two of the longest words** in the question as placeholder concepts.

### Execution Details

- The script accepts a `--subject` argument.
- Processes an input CSV file.
- Prints the extracted concept mappings to the console in a specified format.
- Outputs the results to a file named:

```plaintext
output_concepts_<subject>.csv
```




### I’ve provided two modular, LLM-ready files:

llm_interface.py: A stub with get_concepts_via_llm(question, subject) ready for your real LLM calls.

main.py :

Separates keyword-based extraction into extract_concepts_keyword().

Introduces a --use-llm flag; if set, it attempts an LLM call, falling back to keywords if unimplemented.

Encapsulates processing into process_questions(), keeping I/O and extraction logic cleanly separated.

This structure makes integrating any LLM (Anthropic, OpenAI, etc.) straightforward: just implement llm_interface.get_concepts_via_llm() and uncomment the import.
