import argparse
import os
import re
import csv
from csv_reader import read_subject_csv
from llm_interface import get_concepts_via_llm
# from llm_api import call_anthropic  # Uncomment if using Anthropic in your solution

# ----------------------------------
# User-defined concept mapping per subject
# Keywords should be lowercase; values are formatted concept labels
subject_concept_map = {
    'ancient_history': {
        'indus': 'Indus Valley Civilization',
        'harappan': 'Harappan Civilization',
        'chalcolithic': 'Chalcolithic Cultures',
        'mauryan': 'Mauryan Empire',
        'arthashastra': "Kautilya's Arthashastra",
        'ashokan': 'Ashokan Edicts',
        'burzahom': 'Rock-cut Shrines',
        'chandraketugarh': 'Terracotta Art',
        'ganeshwar': 'Copper Artefacts',
        'gupta': 'Gupta Period Literature',
        'buddhism': 'Buddhist Institutions',
        'jainism': 'Jain Institutions',
        'revenue': 'Revenue and Land Systems',
        'tank': 'Village Tank Systems',
        'brahmins': 'Brahmadeya Institutions',
        'ghatikas': 'Temple-based Education',
        'surgical': 'History of Indian Science',
        'transplant': 'History of Indian Science',
        'sine': 'History of Indian Mathematics',
        'cyclic quadrilateral': 'History of Indian Mathematics'
    },
    'math': {
        'derivative': 'Calculus',
        'integral': 'Calculus',
        'matrix': 'Linear Algebra',
        'vector': 'Linear Algebra',
        'permutation': 'Combinatorics',
        'combination': 'Combinatorics',
        'probability': 'Probability Theory',
        'logarithm': 'Logarithms',
        'quadratic': 'Quadratic Equations',
        'series': 'Sequences and Series',
        'differential': 'Differential Equations',
        'complex': 'Complex Numbers',
        'trigonometry': 'Trigonometry',
        'sine': 'Trigonometry',
        'cosine': 'Trigonometry',
        'equation': 'Equation Solving'
    },
    'physics': {
        'force': 'Classical Mechanics',
        'motion': 'Kinematics',
        'velocity': 'Kinematics',
        'acceleration': 'Kinematics',
        'momentum': 'Dynamics',
        'energy': 'Work and Energy',
        'thermodynamics': 'Thermodynamics',
        'entropy': 'Thermodynamics',
        'optics': 'Optics',
        'wave': 'Wave Phenomena',
        'electric': 'Electromagnetism',
        'magnetic': 'Magnetism',
        'quantum': 'Quantum Mechanics',
        'photoelectric': 'Modern Physics'
    },
    'economics': {
        'gdp': 'Macroeconomic Indicators',
        'cpi': 'Inflation Measures',
        'inflation': 'Inflation Measures',
        'demand': 'Aggregate Demand',
        'supply': 'Aggregate Supply',
        'fiscal': 'Fiscal Policy',
        'monetary': 'Monetary Policy',
        'elasticity': 'Price Elasticity',
        'opportunity cost': 'Opportunity Cost',
        'market structure': 'Market Structures',
        'perfect competition': 'Market Structures',
        'oligopoly': 'Market Structures'
    }
}


def extract_concepts_keyword(question: str, subject: str) -> list:
    """
    Extracts a list of concept labels from the question text for the given subject.
    Combines capitalized noun-phrase extraction with keyword mapping.
    """
    concepts = []
    seen = set()
    # 1. Noun-phrase extraction via capitalized phrases
    noun_phrases = re.findall(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", question)
    for np in noun_phrases:
        key = np.lower()
        if key not in seen:
            concepts.append(np)
            seen.add(key)
    # 2. Keyword-based mapping
    keymap = subject_concept_map.get(subject, {})
    q_lower = question.lower()
    for kw, label in keymap.items():
        if kw in q_lower and label.lower() not in seen:
            concepts.append(label)
            seen.add(label.lower())
    # 3. Fallback: pick up to two of the longest words as placeholder concepts
    if not concepts:
        words = re.findall(r"\w+", q_lower)
        candidates = [w for w in set(words) if len(w) > 6]
        longest = sorted(candidates, key=len, reverse=True)[:2]
        concepts = [w.capitalize() for w in longest] if longest else ['General']
    return concepts


def process_questions(subject: str, use_llm: bool = False):
    data = read_subject_csv(subject)
    print(f"Loaded {len(data)} questions for subject: {subject}")

    outfile = f"output_concepts_{subject}.csv"
    with open(outfile, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(['Question Number', 'Question', 'Concepts'])

        for row in data:
            qnum = row.get('Question Number') or row.get('question_number')
            question = row.get('Question') or row.get('question')

            if use_llm:
                try:
                    concepts = get_concepts_via_llm(question, subject)
                except NotImplementedError:
                    print("LLM call not implemented, falling back to keyword extraction.")
                    concepts = extract_concepts_keyword(question, subject)
            else:
                concepts = extract_concepts_keyword(question, subject)

            concept_str = '; '.join(concepts)
            print(f"Question {qnum}: {concept_str}")
            writer.writerow([qnum, question.strip(), concept_str])

    print(f"Concept mapping complete. Results written to {outfile}")


def main():
    parser = argparse.ArgumentParser(
        description="Question-to-Concept Mapping (LLM-ready)"
    )
    parser.add_argument('--subject', required=True,
                        choices=subject_concept_map.keys())
    parser.add_argument('--use-llm', action='store_true',
                        help='Toggle to use LLM for extraction')
    args = parser.parse_args()

    process_questions(subject=args.subject, use_llm=args.use_llm)


if __name__ == '__main__':
    main()
