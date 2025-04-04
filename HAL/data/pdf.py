
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY


class PDF:

    def __init__(self, file_name: str):
        self.file = file_name
        self.doc = SimpleDocTemplate(self.file, pagesize=A4)
        self.paragraphs = []

    
    def export(self):
        self.doc.build(self.paragraphs)
        print('Aplausos! The PDF has been exported!')



    def add_paragraph(self, text: str, font_name="Helvetica", font_size=12, space_after=12, space_before=0, text_alignement=4):

        styles = getSampleStyleSheet()
        style = ParagraphStyle(
            'CustomStyle',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=font_size,
            spaceAfter=space_after,  # Space after paragraphs
            spaceBefore=space_before,
            alignment=4,  # Align left (use 1 for center, 2 for right)
            wordWrap='None',  # Ensure word wrapping
        )
        paragraph = Paragraph(text, style)
        self.paragraphs.append(paragraph)