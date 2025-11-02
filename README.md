# 🎓 SmarTest - Sistem Inteligent de Generare și Evaluare Întrebări

Aplicație pentru generarea automată de întrebări tip examen AI și evaluarea răspunsurilor, construită cu arhitectură OOP scalabilă.

## 📋 Conținut

- [Despre Proiect](#despre-proiect)
- [Arhitectură](#arhitectură)
- [Instalare](#instalare)
- [Utilizare](#utilizare)
- [Structura Proiectului](#structura-proiectului)
- [Cum să Adăugați Noi Tipuri de Întrebări](#cum-să-adăugați-noi-tipuri-de-întrebări)
- [Împărțire Taskuri Echipă](#împărțire-taskuri-echipă)

---

## 📖 Despre Proiect

**SmarTest** este o aplicație Python pentru:
- ✅ Generarea dinamică de întrebări cu parametri randomizați
- ✅ Răspunsuri punctuale și detaliate (cu explicații)
- ✅ Evaluare automată a răspunsurilor cu fuzzy matching
- ✅ Export întrebări/răspunsuri în format JSON
- 🚧 Export în PDF (coming soon - Persoana 3)
- 🚧 Interfață grafică (coming soon - Persoana 4)

### Tipuri de Întrebări Implementate (Livrabil 2)
- [ ] **n-Queens**: Alegerea strategiei optime (Backtracking, FC, MRV, AC-3)
- [ ] **Nash Equilibrium**: Identificare echilibru Nash pur (TODO - Livrabil 3)
- [ ] **CSP Backtracking**: Asignare variabile cu optimizări (TODO - Livrabil 3)
- [ ] **MinMax Alpha-Beta**: Valoare rădăcină și noduri vizitate (TODO - Livrabil 4)

---

## 🏗️ Arhitectură

### **Arhitectură OOP cu Factory Pattern**

```
QuestionBase (abstract)
    ↓
NQueensQuestion
    ↓
QuestionFactory.register("n-queens", NQueensQuestion)
    ↓
question = create_question("n-queens", "medium")
    ↓
question.create() → params + question_text + correct_answer
```

### **Cum funcționează legătura întrebare-răspuns?**

```python
# 1. Crearea întrebării generează AUTOMAT parametrii
question = NQueensQuestion(difficulty="medium")
question.create()  # Generează: params={n: 8}, question_text, correct_answer

# 2. Parametrii sunt stocați în instanță
print(question.params)  # {"n": 8, "problems": [...]}

# 3. Răspunsul se generează PE BAZA acelorași parametri
print(question.correct_answer)  # "Backtracking" (pentru n=8)
print(question.get_answer(detailed=True))  # Explicații pentru n=8

# 4. Keywords sunt generate dinamic
print(question.get_keywords())  # ["backtracking", "n-queens", "csp"]
```

**Avantaje:**
- ✅ **Sincronizare automată**: Întrebarea și răspunsul sunt MEREU sincronizate
- ✅ **Reutilizabil**: Aceeași instanță poate fi evaluată, exportată, afișată
- ✅ **Scalabil**: Adăugarea unui nou tip = o singură clasă nouă
- ✅ **Testabil**: Fiecare clasă poate fi testată independent

---

## ⚙️ Instalare

### 1. Clonare repository
```bash
git clone https://github.com/alexnec29/SmarTest.git
cd SmarTest
```

### 2. Creare mediu virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalare dependențe
```bash
pip install -r requirements.txt
```

**Notă:** Momentan, aplicația funcționează cu Python standard library! Nu sunt necesare pachete externe pentru funcționalitatea de bază.

---

## 🚀 Utilizare

### Modul Interactiv (CLI)

```bash
python main.py
```

**Exemplu de sesiune:**
```
🎓 SmarTest - Sistem de generare și evaluare întrebări AI
======================================================================

Tipuri de întrebări disponibile: n-queens

Introduceți tipul întrebării (n-queens) sau 'exit': n-queens
Dificultate (easy/medium/hard) [medium]: hard

🔄 Generez întrebare...
──────────────────────────────────────────────────────────────────────
📝 ÎNTREBARE:
──────────────────────────────────────────────────────────────────────
Problema identificată: 12-Queens

Având în vedere problema 12-Queens și comparând-o cu următoarele 
probleme: graph-coloring, knights-tour, generalized-hanoi, care este 
cea mai potrivită strategie de rezolvare dintre cele menționate la curs?

Strategii disponibile: Backtracking, Backtracking + FC, 
Backtracking + MRV, Backtracking + AC-3

[Debug] Parametri generați: {'n': 12, 'problems': [...]}

❓ Doriți să vedeți răspunsul corect înainte? (da/nu) [nu]: nu
──────────────────────────────────────────────────────────────────────
✏️ Introduceți răspunsul dvs.:
(Lăsați gol și apăsați Enter de 2 ori pentru a termina)
──────────────────────────────────────────────────────────────────────
Backtracking with MRV


🔍 Evaluez răspunsul...
======================================================================
📊 REZULTATE EVALUARE
======================================================================

✅ SCOR: 92%

💬 FEEDBACK: Excelent! Toate conceptele cheie sunt prezente.

✓ Keywords găsite: backtracking, mrv, minimum remaining values, n-queens

──────────────────────────────────────────────────────────────────────
✅ RĂSPUNS CORECT:
──────────────────────────────────────────────────────────────────────
Backtracking cu Minimum Remaining Values (MRV)

📚 Doriți să vedeți răspunsul detaliat? (da/nu) [da]: da
──────────────────────────────────────────────────────────────────────
📖 RĂSPUNS DETALIAT:
──────────────────────────────────────────────────────────────────────
[... explicații detaliate ...]
```

### Modul Batch (Generare multiplă)

```bash
# Generează 5 întrebări n-queens de dificultate hard
python ui/client.py batch 5 n-queens hard
```

### Utilizare Programatică

```python
from core.question_factory import create_question
from core.evaluator import evaluate_question

# 1. Creează întrebare
question = create_question("n-queens", difficulty="medium")

# 2. Afișează întrebarea
print(question.get_question())

# 3. Obține răspunsul (punctual sau detaliat)
print(question.get_answer(detailed=False))  # Scurt
print(question.get_answer(detailed=True))   # Cu explicații

# 4. Evaluează răspuns utilizator
user_answer = "Backtracking with Forward Checking"
result = evaluate_question(question, user_answer)

print(f"Scor: {result['score']}%")
print(f"Feedback: {result['feedback']}")
print(f"Răspuns corect: {result['correct_answer']}")

# 5. Export ca JSON
import json
data = question.to_dict()
with open("question.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

---

## 📁 Structura Proiectului

```
SmarTest/
├── core/                           # Core business logic
│   ├── question_factory.py         # ✅ Factory pentru crearea întrebărilor
│   ├── evaluator.py                # ✅ Evaluare răspunsuri cu fuzzy matching
│   ├── answer_generator.py         # 🔜 (momentan integrat în clase)
│   └── question_types/             # Tipuri de întrebări
│       ├── __init__.py             # ✅ Package init
│       ├── base.py                 # ✅ Clasă abstractă QuestionBase
│       └── n_queens.py             # ✅ Implementare n-Queens
│
├── ui/                             # User interfaces
│   ├── client.py                   # ✅ CLI interactiv
│   └── gui.py                      # 🚧 GUI (TODO - Persoana 4)
│
├── utils/                          # 🚧 Utilitare (TODO - Persoana 3)
│   ├── pdf_generator.py           # 🚧 Generare PDF
│   └── pdf_parser.py              # 🚧 Citire PDF
│
├── tests/                          # 🚧 Unit tests (TODO - toți)
│   ├── test_questions.py
│   ├── test_evaluator.py
│   └── test_pdf.py
│
├── templates/                      # Template-uri (opțional)
│   └── n_queens.json
│
├── main.py                         # ✅ Entry point
├── requirements.txt                # ✅ Dependențe
├── README.md                       # ✅ Documentație
└── .gitignore                      # ✅ Git ignore rules
```

**Legenda:**
- ✅ = Implementat (Livrabil 2)
- 🚧 = În dezvoltare
- 🔜 = Planificat

---

## 🆕 Cum să Adăugați Noi Tipuri de Întrebări

### Pas 1: Creați clasa în `core/question_types/`

```python
# core/question_types/nash_equilibrium.py

from .base import QuestionBase
import random

class NashEquilibriumQuestion(QuestionBase):
    
    def generate_params(self):
        # Generează o matrice de joc aleatorie
        matrix = [[random.randint(0, 10) for _ in range(3)] 
                  for _ in range(3)]
        return {"matrix": matrix}
    
    def generate_question_text(self):
        matrix = self.params["matrix"]
        return f"Pentru jocul în formă normală:\n{matrix}\n" \
               f"Există echilibru Nash pur? Care este acesta?"
    
    def generate_correct_answer(self):
        # Logica pentru găsirea echilibrului Nash
        matrix = self.params["matrix"]
        # ... implementare ...
        return "Echilibrul Nash este (2,1) cu payoff (5,7)"
    
    def generate_detailed_answer(self):
        return f"Explicație pas cu pas:\n1. ...\n2. ..."
    
    def get_keywords(self):
        return ["nash", "equilibrium", "echilibru", "pur"]
```

### Pas 2: Înregistrați tipul în `question_factory.py`

```python
from .question_types.nash_equilibrium import NashEquilibriumQuestion

QuestionFactory.register("nash-equilibrium", NashEquilibriumQuestion)
```

### Pas 3: Gata! Acum puteți folosi:

```python
question = create_question("nash-equilibrium", "medium")
```

---

## 👥 Împărțire Taskuri Echipă (4 persoane)

### **Persoana 1: Question Generation & Templates** 🎯
**Status: ✅ DONE pentru n-Queens**

**Taskuri pentru Livrabil 3:**
- [ ] Implementează `NashEquilibriumQuestion`
- [ ] Creează sistem de template-uri pentru diferite formate de joc
- [ ] Adaugă validare matrici și verificare consistență
- [ ] Documentează formatul întrebărilor Nash

**Fișiere:**
- `core/question_types/nash_equilibrium.py` (NOU)
- `templates/nash_equilibrium.json` (NOU)

---

### **Persoana 2: Answer Generation & Evaluation** 🧠
**Status: ✅ DONE pentru evaluare de bază**

**Taskuri pentru Livrabil 3:**
- [ ] Îmbunătățește evaluator pentru răspunsuri matematice (matrici, perechi)
- [ ] Adaugă suport pentru evaluare răspunsuri structurate (ex: (2,1))
- [ ] Implementează logging pentru debugging evaluare
- [ ] Creează teste unit pentru evaluator

**Fișiere:**
- `core/evaluator.py` (UPDATE)
- `tests/test_evaluator.py` (NOU)

---

### **Persoana 3: PDF Management** 📄
**Status: 🚧 NOT STARTED**

**Taskuri pentru Livrabil 3:**
- [ ] Implementează `pdf_generator.py` cu reportlab
- [ ] Creează template PDF profesional (header, footer, formatare)
- [ ] Implementează `pdf_parser.py` cu PyPDF2/pdfplumber
- [ ] Adaugă export/import pentru întrebări și evaluări

**Fișiere:**
- `utils/pdf_generator.py` (NOU)
- `utils/pdf_parser.py` (NOU)
- `templates/pdf_template.html` (NOU - opțional)

**Dependențe de instalat:**
```bash
pip install reportlab PyPDF2 pdfplumber
```

---

### **Persoana 4: User Interface & Integration** 🖥️
**Status: 🚧 NOT STARTED**

**Taskuri pentru Livrabil 3:**
- [ ] Implementează GUI cu tkinter sau Streamlit
- [ ] Integrează toate componentele în interfață
- [ ] Adaugă flux complet: generare → afișare → răspuns → evaluare
- [ ] Testează end-to-end și fixează bug-uri de integrare

**Fișiere:**
- `ui/gui.py` (NOU)
- `main.py` (UPDATE pentru suport GUI)

**Dependințe de instalat (alegeți UNA):**
```bash
# Opțiunea 1: Streamlit (recomandat - cel mai simplu)
pip install streamlit

# Opțiunea 2: tkinter (built-in, nu necesită instalare)
# (nu e nevoie de pip install)

# Opțiunea 3: PyQt6 (cel mai profesional, dar complex)
pip install PyQt6
```

---

## 🎯 Roadmap

### ✅ Livrabil 2 (DONE)
- [x] Arhitectură OOP cu clase
- [x] Implementare completă n-Queens
- [x] Evaluator cu fuzzy matching
- [x] CLI interactiv

### 🚧 Livrabil 3 (În lucru)
- [ ] 2 tipuri de întrebări complete (n-Queens + 1 nou)
- [ ] PDF export/import (Persoana 3)
- [ ] GUI funcțional (Persoana 4)
- [ ] Testing automatizat

### 🔜 Livrabil 4 (Planificat)
- [ ] Toate cele 4 tipuri de întrebări
- [ ] Funcționalități avansate (nivele dificultate, statistici)
- [ ] Documentație completă

---

## 📝 Notițe Dezvoltare

### Cum funcționează sincronizarea întrebare-răspuns?

**Problem:** Cum garantăm că răspunsul generat corespunde întrebării?

**Soluție:** Parametrii sunt stocați în instanța clasei!

```python
class NQueensQuestion:
    def create(self):
        self.params = {"n": 8}              # 1. Generează parametri
        self.question_text = f"{n}-Queens"  # 2. Întrebare folosește params
        self.correct_answer = self._solve() # 3. Răspuns folosește params
```

Când apelați `question.get_answer()`, răspunsul se bazează pe `self.params` care a fost folosit și pentru întrebare!

### De ce clase în loc de funcții?

**Înainte (problematic):**
```python
question = generate_question()  # n=8
answer = generate_answer()      # n=??? (nu știm n!)
```

**Acum (corect):**
```python
q = NQueensQuestion()
q.create()              # n=8 stocat în q.params
print(q.get_question()) # Folosește q.params["n"]=8
print(q.get_answer())   # Folosește ACELAȘI q.params["n"]=8
```

---

## 🤝 Contribuție

1. Fork repository
2. Creați branch pentru feature-ul vostru
3. Commit cu mesaje descriptive
4. Push și creați Pull Request
5. Wait for review

---

## 📞 Contact

**Echipa SmarTest**
- GitHub: [alexnec29/SmarTest](https://github.com/alexnec29/SmarTest)
- Profesor coordonator: [Contact laborator AI]

---

## 📄 Licență

Proiect academic pentru cursul "Inteligență Artificială" - [An Academic] [Universitate]