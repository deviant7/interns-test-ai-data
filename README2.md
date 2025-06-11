# Intern Test Task: Question to Concept Mapping

This template makes it easy to run and evaluate submissions for a question-to-concept mapping task using CSV data and (optionally) the Anthropic LLM API.

## Folder Structure

```
.
├── main.py                 # Entry point, handles CLI and user code
├── llm_api.py              # Handles Anthropic API calls, loads API key from .env
├── csv_reader.py           # Reads CSV from resources/ and returns data
├── resources/              # Folder containing subject CSVs (ancient_history.csv, math.csv, etc.)
├── .env                    # Stores Anthropic API key
├── requirements.txt        # Python dependencies
├── Makefile                # Run commands
└── README.md               # Instructions
└── llm_interface.py        # Stub for LLM integration
```

## Setup Instructions

1. **Clone** the repository and navigate to the project folder.
2. **Install dependencies:**

   ```bash
   make install
   ```
3. **(Optional) Add your Anthropic API key:**

   ```bash
   # .env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Usage

* **Makefile**:

  ```bash
  make run SUBJECT=math
  ```
* **Direct**:

  ```bash
  python main.py --subject=ancient_history
  ```

After running, you’ll see console output like:

```
Loaded 27 questions for subject: ancient_history
Question 1: Indus Valley Civilization; Harappan Civilization
Question 2: Mauryan Empire; Rock-cut Shrines
...
Concept mapping complete. Results written to output_concepts_ancient_history.csv
```

## Simulated LLM Prompt Examples

During development, we simulated LLM outputs by manually prompting a model and hard-coding the results. Below are sample prompts and their corresponding simulated outputs.

### Ancient History

**Prompt:**

```
Given the question: "Which of the following was a feature of the Harappan civilization?", identify the historical concept(s) this question is based on.
```

**Simulated Output:**

```
Harappan Civilization; Urban Planning
```

**Prompt:**

```
Given the question: "Consider the following pairs: Burzahom – Rock-cut shrines; Chandraketugarh – Terracotta art. Which are correctly matched?", identify the concept(s).
```

**Simulated Output:**

```
Archaeological Site–Artifact Mapping; Material Culture of Chalcolithic & Harappan Sites
```

### Mathematics

**Prompt:**

```
Given the question: "A merchant can buy goods at Rs.20 each. If the price for B is more than A and is x% of sum of A and B. What is x?", identify the mathematical concept(s).
```

**Simulated Output:**

```
Percentage Calculations; Basic Algebra
```

### Economics

**Prompt:**

```
Given the question: "If the United States runs a current account deficit, it must run what?", identify the economic concept(s).
```

**Simulated Output:**

```
Balance of Payments; Current Account Deficit
```

### Physics

**Prompt:**

```
Given the question: "What happens when a glass rod is rubbed with silk?", identify the physical concept(s).
```

**Simulated Output:**

```
Electrostatics; Charge Transfer
```

## Extending to a Real LLM

1. Implement `call_anthropic(prompt: str) -> str` in `llm_api.py`.
2. In `main.py`, replace or augment `extract_concepts(...)` with an LLM call:

   ```python
   prompt = f"Given the question: \"{question}\", identify the concept(s)."
   labels = call_anthropic(prompt)
   ```
3. Ensure your `.env` has `ANTHROPIC_API_KEY` set.

---
