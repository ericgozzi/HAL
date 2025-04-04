from fpdf import FPDF
from textwrap import wrap

def export_as_pdf(title: str, text:str):

    text = text.replace("’", "'").replace("“", '"').replace("”", '"')

    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Helvetica', size=12)

    left_margin = 15
    right_margin = 15

    line_height = 4
    usable_width = pdf.w - left_margin - right_margin

    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)

    pdf.set_font('Helvetica', size=15)
    pdf.multi_cell(w=usable_width, h=7, txt=title.strip(), align='J')
    pdf.ln(3)

    pdf.set_font('Helvetica', size=12)
    for paragraph in text.strip().split('\n'):
        pdf.multi_cell(w=usable_width, h=7, txt=paragraph.strip(), align='J')
        pdf.ln(1)
    
    pdf.output('quotes.pdf')
    print("PDF saved")