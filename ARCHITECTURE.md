# SmarTest - Architecture Documentation

## Overview

SmarTest is a scalable AI exam question generator and evaluator that supports multiple question types, dynamic question generation, and comprehensive test building capabilities.

## New Architecture

### Core Components

#### 1. **BaseQuestionHandler** (`core/base_question_handler.py`)
Base class that provides common functionality for all question handlers:
- Question variant selection from multiple questions in JSON
- Parameter preparation with defaults
- Template-based text formatting
- Separation between simple template questions and computed questions

#### 2. **Question Handlers** (`core/question_handlers/`)
Specialized handlers for each question type that extend BaseQuestionHandler:
- `NQueensHandler` - Handles N-Queens problems
- `KnightsTourHandler` - Handles Knight's Tour problems
- `GraphColoringHandler` - Handles graph coloring problems
- `GeneralisedHanoiHandler` - Handles generalized Hanoi tower problems
- `MinimaxHandler` - Handles minimax with alpha-beta pruning
- `NashEquilibriumHandler` - Handles Nash equilibrium problems
- `CSPHandler` - Handles constraint satisfaction problems

Each handler:
- Implements `generate_custom()` for computed questions
- Handles dynamic data generation (e.g., random trees, CSP problems)
- Provides topic-specific answer computation

#### 3. **Question Factory** (`core/question_factory.py`)
Centralized question generation:
- Maps topics to handlers
- Loads JSON templates
- Delegates generation to appropriate handlers
- Provides fallback for template-only generation

#### 4. **Test Builder** (`core/test_builder.py`)
Manages multi-question test creation:
- Allows topic selection
- Generates multiple questions
- Formats questions and answers
- Saves to text files
- Tracks question metadata

#### 5. **PDF Generator** (`core/pdf_generator.py`)
Generates professional PDF documents:
- Question sheets (one question per page)
- Answer keys
- Evaluation reports with scores
- Uses ReportLab for PDF generation

### JSON Template Structure

New JSON format supports multiple question variants per topic:

```json
{
  "keywords": ["topic", "keywords"],
  "params": {
    "param_name": {
      "type": "int",
      "default": 8,
      "choices": [4, 8, 10]
    }
  },
  "questions": [
    {
      "id": "variant_id",
      "question": "Question template with {params}",
      "answer": "Answer template or placeholder",
      "requires_computation": true/false
    }
  ]
}
```

### User Interface

#### Enhanced CLI (`ui/enhanced_client.py`)
Full-featured command-line interface:
- Generate single questions
- Generate multi-question tests
- Select topics from available list
- Specify number of questions
- Save to text or PDF format
- Answer questions with automatic evaluation

#### Simple CLI (`ui/client.py`)
Simplified interface for single question generation and answering.

## Usage Examples

### Generate a Single Question

```python
from core.question_factory import generate_question_and_answer

question, answer = generate_question_and_answer('n-queens', params={})
print(question)
```

### Generate a Test

```python
from core.test_builder import TestBuilder

builder = TestBuilder()
questions, answers = builder.generate_test(
    topics=['n-queens', 'minimax', 'csp'],
    num_questions=5
)

# Save to text
builder.save_questions_to_file('test.txt')
builder.save_answers_to_file('answers.txt')
```

### Generate PDF Test

```python
from core.test_builder import TestBuilder
from core.pdf_generator import PDFGenerator

builder = TestBuilder()
questions, answers = builder.generate_test(
    topics=['n-queens', 'minimax'],
    num_questions=3
)

pdf_gen = PDFGenerator()
pdf_gen.generate_questions_pdf(questions, 'test.pdf')
pdf_gen.generate_answers_pdf(answers, 'answers.pdf')
```

### Evaluate an Answer

```python
from core.evaluator import evaluate_answer

score = evaluate_answer(
    correct_answer="Backtracking is the best strategy",
    user_answer="Use backtracking"
)
print(f"Score: {score}%")
```

## Benefits of New Architecture

### 1. **No Code Repetition**
- Common functionality extracted to BaseQuestionHandler
- Question generation logic reused across all types
- Template formatting centralized

### 2. **Scalability**
- Easy to add new question types (create handler, add JSON)
- Multiple question variants per topic
- Dynamic question/answer generation

### 3. **Flexibility**
- Questions can be pure template or computed
- Parameters defined in JSON with defaults
- Random selection from multiple variants

### 4. **Maintainability**
- Clear separation of concerns
- Each handler focuses on one question type
- JSON templates separate from code

### 5. **Extensibility**
- New output formats easy to add (PDF, HTML, etc.)
- Test builder can be extended with filtering, difficulty levels
- Evaluation can be enhanced with AI-based checking

## Adding a New Question Type

1. Create JSON template in `templates/`:
```json
{
  "keywords": ["new", "topic"],
  "params": { ... },
  "questions": [ ... ]
}
```

2. Create handler in `core/question_handlers/`:
```python
from ..base_question_handler import BaseQuestionHandler

class NewTopicHandler(BaseQuestionHandler):
    def generate_custom(self, variant, params):
        # Custom logic here
        return question, answer
```

3. Register in `core/question_factory.py`:
```python
HANDLER_CLASSES = {
    "new-topic": NewTopicHandler,
    ...
}
```

4. Add to `core/question_handlers/__init__.py`

Done! The new question type is now available throughout the system.

## File Organization

```
SmarTest/
├── core/
│   ├── base_question_handler.py      # Base handler class
│   ├── question_handlers/            # Specialized handlers
│   │   ├── __init__.py
│   │   ├── n_queens_handler.py
│   │   ├── minimax_handler.py
│   │   └── ...
│   ├── question_factory.py           # Factory pattern
│   ├── test_builder.py               # Multi-question tests
│   ├── pdf_generator.py              # PDF generation
│   ├── evaluator.py                  # Answer evaluation
│   └── question_types/               # Old modules (deprecated)
├── templates/                         # JSON templates
│   ├── n_queens.json
│   ├── minimax.json
│   └── ...
├── ui/
│   ├── enhanced_client.py            # Full CLI
│   └── client.py                     # Simple CLI
├── main.py                           # Entry point
└── requirements.txt
```

## Dependencies

- `fuzzywuzzy` - Answer similarity matching
- `unidecode` - Text normalization
- `reportlab` - PDF generation

Install with:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

This launches the enhanced CLI with full test generation capabilities.
