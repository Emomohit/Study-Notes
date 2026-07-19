import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Try to register Arial font for Windows, fallback to standard Helvetica
font_name = "Helvetica"
font_name_bold = "Helvetica-Bold"
font_name_italic = "Helvetica-Oblique"

try:
    # Reportlab searches C:\Windows\Fonts automatically when using TTFont
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Italic', 'ariali.ttf'))
    font_name = "Arial"
    font_name_bold = "Arial-Bold"
    font_name_italic = "Arial-Italic"
    print("Successfully registered Arial font.")
except Exception as e:
    print(f"Could not register Arial font: {e}. Falling back to standard Helvetica.")

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count
    along with a clean, professional header line and footer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont(font_name, 8.5)
        self.setFillColor(colors.HexColor('#555555'))
        
        # Draw a thin footer line
        self.setStrokeColor(colors.HexColor('#D0D3D4'))
        self.setLineWidth(0.5)
        self.line(40, 45, 555, 45)
        
        # Footer text
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, footer_text)
        self.drawString(40, 30, "SISTec Department of Engineering Sciences - Master Sessional Test (MST)")
        self.restoreState()

# Main generator
pdf_path = "M3_MST_Sample_Paper_SISTec.pdf"

# Set up standard doc
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=60 # Extra room for footer
)

styles = getSampleStyleSheet()

# Typography and Styling Theme
title_style = ParagraphStyle(
    'TitleStyle',
    fontName=font_name_bold,
    fontSize=13,
    leading=17,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#1B365D') # Deep Navy
)

subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    fontName=font_name_bold,
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#444444')
)

normal_style = ParagraphStyle(
    'NormalStyle',
    fontName=font_name,
    fontSize=9.5,
    leading=14.5,
    textColor=colors.HexColor('#222222')
)

bold_style = ParagraphStyle(
    'BoldStyle',
    fontName=font_name_bold,
    fontSize=9.5,
    leading=14.5,
    textColor=colors.HexColor('#222222')
)

section_header_style = ParagraphStyle(
    'SectionHeaderStyle',
    fontName=font_name_bold,
    fontSize=10,
    leading=14,
    textColor=colors.white,
    keepWithNext=True
)

section_title_style = ParagraphStyle(
    'SectionTitleStyle',
    fontName=font_name_bold,
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor('#1B365D'),
    spaceBefore=6,
    spaceAfter=3,
    keepWithNext=True
)

eq_style = ParagraphStyle(
    'EqStyle',
    parent=normal_style,
    leftIndent=15
)

or_style = ParagraphStyle(
    'OrStyle',
    parent=bold_style,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#666666'),
    spaceBefore=4,
    spaceAfter=4
)

def make_section_banner(title_text):
    banner_table = Table([[Paragraph(title_text, section_header_style)]], colWidths=[515])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1B365D')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return KeepTogether([Spacer(1, 10), banner_table, Spacer(1, 6)])

def make_options_table(opt_a, opt_b, opt_c, opt_d, style):
    max_len = max(len(opt_a), len(opt_b), len(opt_c), len(opt_d))
    
    p_a = Paragraph(f"<b>A)</b> {opt_a}", style)
    p_b = Paragraph(f"<b>B)</b> {opt_b}", style)
    p_c = Paragraph(f"<b>C)</b> {opt_c}", style)
    p_d = Paragraph(f"<b>D)</b> {opt_d}", style)
    
    if max_len < 25:
        col_widths = [128.75, 128.75, 128.75, 128.75]
        data = [[p_a, p_b, p_c, p_d]]
    elif max_len < 55:
        col_widths = [257.5, 257.5]
        data = [
            [p_a, p_b],
            [p_c, p_d]
        ]
    else:
        col_widths = [515]
        data = [
            [p_a],
            [p_b],
            [p_c],
            [p_d]
        ]
        
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t

def make_question(num_str, text_str, content_flowables=None):
    q_style = ParagraphStyle(
        'QStyle',
        parent=normal_style,
    )
    
    p_num = Paragraph(f"<b>{num_str}</b>", q_style)
    p_text = Paragraph(text_str, q_style)
    
    row_data = [[p_num, p_text]]
    q_table = Table(row_data, colWidths=[20, 495])
    q_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    
    flowables = [q_table]
    if content_flowables:
        flowables.extend(content_flowables)
        
    flowables.append(Spacer(1, 3))
    return KeepTogether(flowables)

elements = []

# ==========================================
# 1. EXAM HEADER PANEL
# ==========================================
header_data = [
    [Paragraph("<b>SAGAR INSTITUTE OF SCIENCE & TECHNOLOGY (SISTec)</b>", title_style)],
    [Paragraph("DEPARTMENT OF ENGINEERING SCIENCES", subtitle_style)],
    [Paragraph("<b>MASTER SESSIONAL TEST (MST)</b>", subtitle_style)],
    [Paragraph("<b>ENGINEERING MATHEMATICS – III (BT-401)</b>", title_style)]
]
header_table = Table(header_data, colWidths=[515])
header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('LINEBELOW', (0, 3), (0, 3), 1.5, colors.HexColor('#1B365D')),
]))
elements.append(header_table)
elements.append(Spacer(1, 8))

# ==========================================
# 2. METADATA SECTION
# ==========================================
info_data = [
    [
        Paragraph("<b>Branch:</b> CSE/AI/IT/ME/CE", normal_style),
        Paragraph("<b>Semester:</b> III", normal_style)
    ],
    [
        Paragraph("<b>Time:</b> 1 Hour 30 Minutes", normal_style),
        Paragraph("<b>Maximum Marks:</b> 28", normal_style)
    ]
]
info_table = Table(info_data, colWidths=[257.5, 257.5])
info_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('LINEBELOW', (0, 1), (-1, 1), 0.75, colors.HexColor('#D0D3D4')),
]))
elements.append(info_table)
elements.append(Spacer(1, 10))

# ==========================================
# 3. PART A - OBJECTIVE QUESTIONS
# ==========================================
elements.append(make_section_banner("PART – A: Objective Type Questions (18 × 0.5 = 9 Marks)"))

mcqs = [
    ("1.", "The method based on repeated halving of interval is:", 
     "Newton Raphson Method", "Bisection Method", "Gauss Jordan Method", "Simpson’s Rule"),
    
    ("2.", "Newton-Raphson formula is:", 
     "x<sub>n+1</sub> = x<sub>n</sub> - f(x<sub>n</sub>)", 
     "x<sub>n+1</sub> = x<sub>n</sub> + f(x<sub>n</sub>)/f'(x<sub>n</sub>)", 
     "x<sub>n+1</sub> = x<sub>n</sub> - f(x<sub>n</sub>)/f'(x<sub>n</sub>)", 
     "x<sub>n+1</sub> = f(x<sub>n</sub>)"),
    
    ("3.", "In Regula-Falsi method, root lies between:", 
     "Equal signs", "Opposite signs", "Positive numbers only", "Negative numbers only"),
    
    ("4.", "The forward difference operator is denoted by:", 
     "&nabla;", "&Delta;", "E", "&delta;"),
    
    ("5.", "The backward difference operator is:", 
     "&Delta;", "E", "&nabla;", "D"),
    
    ("6.", "Shifting operator is represented by:", 
     "&Delta;", "E", "&nabla;", "&delta;"),
    
    ("7.", "Relation between operators is:", 
     "E = 1 + &Delta;", "E = 1 - &Delta;", "E = &Delta; - 1", "E = &nabla; + 1"),
    
    ("8.", "Interpolation is used to find:", 
     "Exact roots", "Missing values", "Derivatives only", "Integrals only"),
    
    ("9.", "Simpson’s 1/3 rule is used for:", 
     "Differentiation", "Root finding", "Numerical integration", "Matrix inversion"),
    
    ("10.", "In Trapezoidal rule, graph is approximated by:", 
     "Triangle", "Rectangle", "Trapezium", "Circle"),
    
    ("11.", "Numerical integration is also called:", 
     "Cubature", "Quadrature", "Factorization", "Iteration"),
    
    ("12.", "Gauss elimination method is used to solve:", 
     "Differential equations", "Algebraic equations", "Simultaneous linear equations", "Integrals"),
    
    ("13.", "In Gauss Jordan method, matrix is converted into:", 
     "Diagonal form", "Triangular form", "Identity form", "Symmetric form"),
    
    ("14.", "Jacobi method is:", 
     "Direct method", "Iterative method", "Graphical method", "Analytical method"),
    
    ("15.", "Crout’s method is related to:", 
     "Interpolation", "Integration", "Matrix factorization", "Differentiation"),
    
    ("16.", "Simpson’s 3/8 rule requires intervals to be multiple of:", 
     "2", "3", "4", "5"),
    
    ("17.", "The formula for first forward difference is:", 
     "f(x + h) + f(x)", "f(x + h) - f(x)", "f(x) - f(x + h)", "hf(x)"),
    
    ("18.", "The condition necessary for Gauss-Seidel method convergence is:", 
     "Symmetric matrix", "Diagonal dominance", "Zero determinant", "Unit matrix")
]

for num, q_text, a, b, c, d in mcqs:
    opt_table = make_options_table(a, b, c, d, normal_style)
    elements.append(make_question(num, q_text, [opt_table]))

# ==========================================
# 4. PART B - SHORT QUESTIONS
# ==========================================
elements.append(make_section_banner("PART – B: Short Answer Type Questions"))
elements.append(Paragraph("<b>Attempt any TWO from each section.</b>", bold_style))
elements.append(Spacer(1, 4))

# SECTION I
elements.append(Paragraph("SECTION – I", section_title_style))
elements.append(make_question("19.", "Using Newton-Raphson method, find the cube root of 2 correct upto 4 decimal places."))
elements.append(make_question("20.", "Find a positive root of 3x = cos x + 1 using Bisection Method."))
elements.append(make_question("21.", "Define Forward Difference Operator and Backward Difference Operator."))

# SECTION II
elements.append(Paragraph("SECTION – II", section_title_style))
elements.append(make_question("22.", "Using Newton forward interpolation formula, find f(0.18)."))
elements.append(make_question("23.", "Using Newton backward interpolation formula, find sin 58&deg;."))
elements.append(make_question("24.", "Evaluate &Delta;e<sup>ax</sup> and &Delta;<sup>2</sup>e<sup>x</sup>."))

# SECTION III
elements.append(Paragraph("SECTION – III", section_title_style))
elements.append(make_question("25.", "Evaluate &int;<sub>0</sub><sup>2</sup> x<sup>3</sup>dx using Simpson’s 1/3 rule."))

q26_eqs = [
    Paragraph("2x + y = 5", eq_style),
    Paragraph("x + 3y = 6", eq_style)
]
elements.append(make_question("26.", "Solve using Gauss Elimination Method:", q26_eqs))

q27_eqs = [
    Paragraph("2x + y = 4", eq_style),
    Paragraph("x - y = 1", eq_style)
]
elements.append(make_question("27.", "Apply Gauss Jordan Method to solve:", q27_eqs))

# ==========================================
# 5. PART C - LONG QUESTIONS
# ==========================================
elements.append(make_section_banner("PART – C: Long Answer Type Questions"))
elements.append(Paragraph("<b>Attempt any ONE.</b>", bold_style))
elements.append(Spacer(1, 4))

# Question 28
q28_content = [
    Paragraph("Find the real root of x log<sub>10</sub>x - 1.2 = 0 correct upto 5 decimal places using Regula-Falsi Method.", normal_style),
    Spacer(1, 2),
    Paragraph("OR", or_style),
    Spacer(1, 2),
    Paragraph("Using Lagrange interpolation formula, find u(6) for the given data:", normal_style),
    Spacer(1, 4)
]

table_data = [
    [Paragraph("<b>x</b>", bold_style), Paragraph("1", normal_style), Paragraph("2", normal_style), Paragraph("4", normal_style), Paragraph("7", normal_style), Paragraph("8", normal_style)],
    [Paragraph("<b>u(x)</b>", bold_style), Paragraph("22", normal_style), Paragraph("30", normal_style), Paragraph("82", normal_style), Paragraph("106", normal_style), Paragraph("206", normal_style)]
]
data_table = Table(table_data, colWidths=[40, 40, 40, 40, 40, 40])
data_table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F4F6F8')),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))

table_indent_wrapper = Table([[data_table]], colWidths=[515])
table_indent_wrapper.setStyle(TableStyle([
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
]))
q28_content.append(table_indent_wrapper)

elements.append(make_question("28.", "", q28_content))

# Question 29
q29_content = [
    Paragraph("Evaluate &int;<sub>0</sub><sup>6</sup> dx / (1 + x<sup>2</sup>) using:", normal_style),
    Paragraph("1. Trapezoidal Rule", eq_style),
    Paragraph("2. Simpson’s 1/3 Rule", eq_style),
    Paragraph("3. Simpson’s 3/8 Rule", eq_style),
    Spacer(1, 2),
    Paragraph("OR", or_style),
    Spacer(1, 2),
    Paragraph("Solve by Gauss Seidel Method:", normal_style)
]

q29_eqs = [
    Paragraph("10x + y + z = 12", eq_style),
    Paragraph("2x + 10y + z = 13", eq_style),
    Paragraph("2x + 2y + 10z = 14", eq_style)
]
q29_content.extend(q29_eqs)

elements.append(make_question("29.", "", q29_content))

# Build Document using NumberedCanvas for dynamic footer
doc.build(elements, canvasmaker=NumberedCanvas)

print(f"PDF generated successfully: {pdf_path}")
