# core/pdf_generator.py

"""
PDF generation for questions and answers.
Uses ReportLab for PDF generation.
"""

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFGenerator:
    """Generate PDF files for questions and answers."""
    
    def __init__(self):
        """Initialize PDF generator."""
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "ReportLab is required for PDF generation. "
                "Install it with: pip install reportlab"
            )
        
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor='darkblue',
            spaceAfter=30,
            alignment=TA_CENTER,
        ))
        
        # Question heading style
        self.styles.add(ParagraphStyle(
            name='QuestionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor='darkgreen',
            spaceAfter=12,
        ))
        
        # Topic style
        self.styles.add(ParagraphStyle(
            name='TopicStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor='gray',
            italic=True,
            spaceAfter=6,
        ))
    
    def generate_questions_pdf(
        self, 
        questions: list, 
        filename: str,
        title: str = "AI Exam Questions",
        include_topics: bool = True
    ):
        """
        Generate PDF file with questions.
        
        Args:
            questions: List of question dictionaries
            filename: Output PDF filename
            title: Title for the document
            include_topics: Whether to include topic names
        """
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        title_para = Paragraph(title, self.styles['CustomTitle'])
        story.append(title_para)
        story.append(Spacer(1, 0.3*inch))
        
        # Questions
        for i, q in enumerate(questions, 1):
            # Question number
            q_heading = Paragraph(f"Question {i}", self.styles['QuestionHeading'])
            story.append(q_heading)
            
            # Topic (if requested)
            if include_topics and 'topic_name' in q:
                topic_para = Paragraph(
                    f"Topic: {q['topic_name']}", 
                    self.styles['TopicStyle']
                )
                story.append(topic_para)
            
            # Question text
            question_text = self._escape_html(q.get('question', ''))
            question_para = Paragraph(question_text, self.styles['Normal'])
            story.append(question_para)
            story.append(Spacer(1, 0.5*inch))
            
            # Page break after each question (except last)
            if i < len(questions):
                story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
    
    def generate_answers_pdf(
        self, 
        answers: list, 
        filename: str,
        title: str = "Answer Key"
    ):
        """
        Generate PDF file with answers.
        
        Args:
            answers: List of answer strings
            filename: Output PDF filename
            title: Title for the document
        """
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        title_para = Paragraph(title, self.styles['CustomTitle'])
        story.append(title_para)
        story.append(Spacer(1, 0.3*inch))
        
        # Answers
        for i, answer in enumerate(answers, 1):
            # Answer number
            a_heading = Paragraph(f"Answer {i}", self.styles['QuestionHeading'])
            story.append(a_heading)
            
            # Answer text
            answer_text = self._escape_html(answer)
            answer_para = Paragraph(answer_text, self.styles['Normal'])
            story.append(answer_para)
            story.append(Spacer(1, 0.4*inch))
        
        # Build PDF
        doc.build(story)
    
    def generate_evaluation_pdf(
        self,
        question: str,
        user_answer: str,
        correct_answer: str,
        score: int,
        filename: str
    ):
        """
        Generate PDF file with evaluation result.
        
        Args:
            question: The question text
            user_answer: User's answer
            correct_answer: Correct answer
            score: Score percentage (0-100)
            filename: Output PDF filename
        """
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        title_para = Paragraph("Evaluation Result", self.styles['CustomTitle'])
        story.append(title_para)
        story.append(Spacer(1, 0.3*inch))
        
        # Score
        score_text = f"<b>Score: {score}%</b>"
        score_para = Paragraph(score_text, self.styles['Heading2'])
        story.append(score_para)
        story.append(Spacer(1, 0.3*inch))
        
        # Question
        q_heading = Paragraph("Question:", self.styles['QuestionHeading'])
        story.append(q_heading)
        question_para = Paragraph(self._escape_html(question), self.styles['Normal'])
        story.append(question_para)
        story.append(Spacer(1, 0.3*inch))
        
        # User's answer
        ua_heading = Paragraph("Your Answer:", self.styles['QuestionHeading'])
        story.append(ua_heading)
        user_answer_para = Paragraph(self._escape_html(user_answer), self.styles['Normal'])
        story.append(user_answer_para)
        story.append(Spacer(1, 0.3*inch))
        
        # Correct answer
        ca_heading = Paragraph("Correct Answer:", self.styles['QuestionHeading'])
        story.append(ca_heading)
        correct_answer_para = Paragraph(self._escape_html(correct_answer), self.styles['Normal'])
        story.append(correct_answer_para)
        
        # Build PDF
        doc.build(story)
    
    def _escape_html(self, text: str) -> str:
        """
        Escape special HTML characters for ReportLab.
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text
        """
        if not text:
            return ""
        
        # Replace special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Preserve line breaks
        text = text.replace('\n', '<br/>')
        
        return text


def is_pdf_available() -> bool:
    """Check if PDF generation is available."""
    return REPORTLAB_AVAILABLE
