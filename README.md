# SmarTest

An advanced AI exam question generator and evaluator built for the "Artificial Intelligence" course. The application generates exam-style questions, evaluates answers, and supports multi-question test creation with PDF export capabilities.

## Features

### Core Capabilities
- ✅ **Generate single questions** - Create questions for any supported AI topic
- ✅ **Multi-question tests** - Build tests combining multiple questions
- ✅ **Topic selection** - Choose from 7 AI topics/chapters
- ✅ **Dynamic generation** - Questions are generated with random parameters
- ✅ **Answer evaluation** - Percentage-based scoring (0-100%)
- ✅ **PDF export** - Generate professional PDF documents
- ✅ **Text export** - Save questions and answers as text files

### Supported Topics
1. **N-Queens Problem** - Backtracking strategies and solutions
2. **Knight's Tour** - Chess board traversal algorithms
3. **Graph Coloring** - Chromatic numbers and CSP
4. **Generalized Hanoi** - Tower of Hanoi variations
5. **Minimax** - Alpha-Beta pruning and game trees
6. **Nash Equilibrium** - Game theory concepts
7. **CSP** - Constraint satisfaction with forward checking

### Question Types
Each topic supports multiple question variants:
- Strategy questions (which algorithm to use)
- Computational questions (calculate specific values)
- Example questions (provide solutions)
- Complexity questions (analyze time/space complexity)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alexnec29/SmarTest.git
cd SmarTest
```

2. Create and activate virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
python main.py
```

This launches the interactive menu where you can:
1. Generate a single question
2. Generate a test (multiple questions)
3. Answer a saved test
4. Exit

### Command-Line Examples

#### Generate a Single Question
```python
from core.question_factory import generate_question_and_answer

question, answer = generate_question_and_answer('n-queens', params={})
print(question)
```

#### Generate a Multi-Question Test
```python
from core.test_builder import TestBuilder

builder = TestBuilder()
questions, answers = builder.generate_test(
    topics=['n-queens', 'minimax', 'csp'],
    num_questions=5
)

# Save to text files
builder.save_questions_to_file('test.txt')
builder.save_answers_to_file('answers.txt')
```

#### Generate PDF Test
```python
from core.test_builder import TestBuilder
from core.pdf_generator import PDFGenerator

builder = TestBuilder()
questions, answers = builder.generate_test(
    topics=['graph-coloring', 'knights-tour'],
    num_questions=3
)

pdf_gen = PDFGenerator()
pdf_gen.generate_questions_pdf(questions, 'test.pdf')
pdf_gen.generate_answers_pdf(answers, 'answers.pdf')
```

#### Evaluate an Answer
```python
from core.evaluator import evaluate_answer

score = evaluate_answer(
    correct_answer="Backtracking is the most suitable strategy for N-Queens.",
    user_answer="Use backtracking"
)
print(f"Score: {score}%")
```

## Architecture

The system uses a modular, handler-based architecture:

- **BaseQuestionHandler** - Common functionality for all question types
- **Specialized Handlers** - One handler per topic type
- **Question Factory** - Coordinates question generation
- **Test Builder** - Manages multi-question test creation
- **PDF Generator** - Creates professional PDF documents
- **Enhanced CLI** - User-friendly interface

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Adding New Question Types

1. Create JSON template in `templates/new_topic.json`
2. Create handler class extending `BaseQuestionHandler`
3. Register in `question_factory.py`
4. Done! The new topic is automatically available.

See ARCHITECTURE.md for a complete guide.

## File Structure

```
SmarTest/
├── core/
│   ├── base_question_handler.py    # Base handler class
│   ├── question_handlers/          # Topic-specific handlers
│   ├── question_factory.py         # Question generation coordinator
│   ├── test_builder.py             # Multi-question test builder
│   ├── pdf_generator.py            # PDF export functionality
│   └── evaluator.py                # Answer evaluation
├── templates/                       # JSON question templates
├── ui/
│   ├── enhanced_client.py          # Full-featured CLI
│   └── client.py                   # Simple CLI
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
├── ARCHITECTURE.md                 # Detailed architecture docs
└── README.md                       # This file
```

## Requirements

- Python 3.7+
- fuzzywuzzy - Answer similarity matching
- unidecode - Text normalization
- reportlab - PDF generation

## Development

The application was developed using advanced conversational AI assistants (GitHub Copilot) to implement:
- Scalable architecture with minimal code repetition
- Dynamic question generation from JSON templates
- Flexible handler system for different question types
- Comprehensive test building and export capabilities

## License

[Add your license here]

## Contributors

[Add contributors here]
