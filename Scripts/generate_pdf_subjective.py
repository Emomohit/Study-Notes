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
        
        # 1. Header (only draw on page 2 and later)
        if self._pageNumber > 1:
            self.setFont(font_name_bold, 8)
            self.setFillColor(colors.HexColor('#1E3A8A')) # Deep Navy
            self.drawString(40, 805, "EMo Learners")
            self.setFont(font_name, 8)
            self.setFillColor(colors.HexColor('#4B5563')) # Medium Gray
            self.drawString(100, 805, " |   Analysis and Design of Algorithms (ADA) Solutions")
            self.drawRightString(555, 805, "Subjective & Numerical Question Bank")
            
            # Header line
            self.setStrokeColor(colors.HexColor('#E5E7EB')) # Light grey
            self.setLineWidth(0.5)
            self.line(40, 797, 555, 797)
            
        # 2. Footer (draw on all pages)
        self.setStrokeColor(colors.HexColor('#E5E7EB'))
        self.setLineWidth(0.75)
        self.line(40, 45, 555, 45)
        
        # Footer left text
        self.setFont(font_name, 8.5)
        self.setFillColor(colors.HexColor('#4B5563')) # Dark Gray
        self.drawString(40, 30, "Document Exclusively Curated by ")
        
        # Highlight "EMo Learners" in bold teal
        self.setFont(font_name_bold, 8.5)
        self.setFillColor(colors.HexColor('#0D9488')) # Teal
        self.drawString(178, 30, "EMo Learners")
        
        # Footer right text
        self.setFont(font_name, 8.5)
        self.setFillColor(colors.HexColor('#4B5563'))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_text)
        
        self.restoreState()

# Main generator
pdf_path = "ADA_Unit_1_2_Subjective_Bank_Solutions.pdf"

# Set up standard doc
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=60,  # Extra room for header
    bottomMargin=60 # Extra room for footer
)

styles = getSampleStyleSheet()

# Typography and Styling Theme (With generous breathing space and line heights)
title_style = ParagraphStyle(
    'TitleStyle',
    fontName=font_name_bold,
    fontSize=13.5,
    leading=18,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#1E3A8A'),
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    fontName=font_name_bold,
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#4B5563')
)

normal_style = ParagraphStyle(
    'NormalStyle',
    fontName=font_name,
    fontSize=9.5,
    leading=16,
    textColor=colors.HexColor('#1F2937'),
    spaceBefore=5,
    spaceAfter=5
)

bold_style = ParagraphStyle(
    'BoldStyle',
    fontName=font_name_bold,
    fontSize=9.5,
    leading=16,
    textColor=colors.HexColor('#1F2937'),
    spaceBefore=5,
    spaceAfter=5
)

section_header_style = ParagraphStyle(
    'SectionHeaderStyle',
    fontName=font_name_bold,
    fontSize=11,
    leading=15,
    textColor=colors.white,
    keepWithNext=True
)

answer_body_style = ParagraphStyle(
    'AnswerBody',
    parent=normal_style,
    leftIndent=15,
    textColor=colors.HexColor('#2D3748'), # Slate Gray
    fontSize=9.5,
    leading=16.5,
    spaceBefore=6,
    spaceAfter=6
)

answer_bold_style = ParagraphStyle(
    'AnswerBold',
    parent=bold_style,
    leftIndent=15,
    textColor=colors.HexColor('#1E3A8A'), # Navy for inner sub-headers
    fontName=font_name_bold,
    fontSize=9.5,
    leading=16.5,
    spaceBefore=10,
    spaceAfter=6
)

answer_bullet_style = ParagraphStyle(
    'AnswerBullet',
    parent=answer_body_style,
    leftIndent=28,
    firstLineIndent=-12,
    spaceBefore=4,
    spaceAfter=4,
    leading=15.5
)

code_style = ParagraphStyle(
    'CodeStyle',
    fontName='Courier',
    fontSize=8.5,
    leading=12.5,
    leftIndent=28,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=4,
    spaceAfter=4
)

table_text_style = ParagraphStyle(
    'TableText',
    fontName=font_name,
    fontSize=8.5,
    leading=13,
    textColor=colors.HexColor('#2D3748')
)

table_header_style = ParagraphStyle(
    'TableHeader',
    fontName=font_name_bold,
    fontSize=9,
    leading=13,
    textColor=colors.white
)

def make_section_banner(title_text):
    banner_table = Table([[Paragraph(title_text, section_header_style)]], colWidths=[515])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1E3A8A')), # Deep Navy
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return KeepTogether([Spacer(1, 15), banner_table, Spacer(1, 10)])

def make_subjective_qa(num_str, q_type, q_text, answer_flowables):
    q_style = ParagraphStyle(
        'SubjQStyle',
        parent=normal_style,
        fontName=font_name_bold,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
    )
    
    label = f"<b>{num_str} [{q_type}]</b>"
    p_num = Paragraph(label, q_style)
    p_text = Paragraph(q_text, ParagraphStyle('SubjQText', parent=normal_style, fontName=font_name_bold, fontSize=10, leading=15))
    
    q_table = Table([[p_num, p_text]], colWidths=[110, 405])
    q_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    # We wrap the question header and the first element of the answer in a KeepTogether to avoid orphan headings.
    # The remaining answer flowables can follow freely so they can split across pages if needed!
    flowables = []
    
    first_part = [q_table, Spacer(1, 6)]
    if answer_flowables:
        first_part.append(answer_flowables[0])
        
    flowables.append(KeepTogether(first_part))
    
    if len(answer_flowables) > 1:
        flowables.extend(answer_flowables[1:])
        
    flowables.append(Spacer(1, 24)) # Spaced-out question gap (increased from 10 to 24)
    return flowables

elements = []

# ==========================================
# 1. EXAM HEADER PANEL (Page 1)
# ==========================================
header_data = [
    [Paragraph("<b>EMo Learners</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.HexColor('#0D9488')))],
    [Paragraph("<b>PROFESSIONAL QUESTION BANK WITH FULL SOLUTIONS</b>", ParagraphStyle('HSub', fontName=font_name_bold, fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>Analysis and Design of Algorithms (ADA)</b>", ParagraphStyle('HSub2', fontName=font_name_bold, fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1F2937')))],
    [Paragraph("<b>Subjective, Comparative, Derivation, and Tracing Solutions</b>", ParagraphStyle('HDesc', fontName=font_name_bold, fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor('#4B5563')))]
]

header_table = Table(header_data, colWidths=[515])
header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#0D9488')), # Teal divider
]))
elements.append(header_table)
elements.append(Spacer(1, 12))

# ==========================================
# 2. METADATA SECTION
# ==========================================
info_data = [
    [
        Paragraph("<b>Subject:</b> Analysis &amp; Design of Algorithms (ADA)", normal_style),
        Paragraph("<b>Scope:</b> Units 1 &amp; 2 (Detailed Textbook Answers)", normal_style)
    ],
    [
        Paragraph("<b>Prep Quality:</b> Verified &amp; Curated", normal_style),
        Paragraph("<b>Branding Highlight:</b> EMo Learners Exclusive", normal_style)
    ]
]
info_table = Table(info_data, colWidths=[270, 245])
info_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LINEBELOW', (0, 1), (-1, 1), 0.75, colors.HexColor('#E2E8F0')),
]))
elements.append(info_table)

# ==========================================
# 3. UNIT 1 BANNER
# ==========================================
elements.append(make_section_banner("UNIT 1: ALGORITHMS, DESIGNING, AND ANALYZING"))

# ==========================================
# UNIT 1 QUESTIONS & SOLUTIONS
# ==========================================

# Q1: What is an algorithm? Characteristics
q1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("An <b>algorithm</b> is a well-defined, step-by-step computational procedure that takes some value (or set of values) as input and produces some value (or set of values) as output to solve a specific mathematical or computational problem. It serves as an abstract recipe for solving a problem, independent of specific programming languages or execution environments.", answer_body_style),
    Paragraph("A good and correct algorithm must exhibit the following <b>six key characteristics</b>:", answer_bold_style),
    Paragraph("• <b>Input:</b> An algorithm must have zero or more well-defined inputs, supplied from an external source.", answer_bullet_style),
    Paragraph("• <b>Output:</b> It must produce at least one well-defined output value that solves the target problem.", answer_bullet_style),
    Paragraph("• <b>Definiteness (Unambiguous):</b> Each step of the algorithm must be clear, precise, and completely unambiguous. There should be only one interpretation of each instruction.", answer_bullet_style),
    Paragraph("• <b>Finiteness:</b> The algorithm must always terminate after a finite number of execution steps, avoiding infinite loops.", answer_bullet_style),
    Paragraph("• <b>Feasibility (Effectiveness):</b> Every step must be basic enough to be carried out in practice, meaning it is realizable with paper and pencil using finite resources.", answer_bullet_style),
    Paragraph("• <b>Language Independence:</b> The steps must be purely logical and generic, allowing direct translation into any programming language (C, Python, Java, etc.).", answer_bullet_style),
]
elements.extend(make_subjective_qa("Q1.", "Short Answer", "What is an algorithm? Explain the various characteristics of a good algorithm.", q1_ans))

# Q2: Asymptotic Notations
q2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Asymptotic Notations</b> are mathematical tools used to describe and analyze the running time or space complexity of an algorithm in terms of the input size <i>n</i> as <i>n</i> grows arbitrarily large (approaching infinity). They provide a way to establish boundaries on growth rates.", answer_body_style),
    Paragraph("The three primary asymptotic notations are defined and exemplified below:", answer_bold_style),
    
    Paragraph("1. Big-Oh Notation (<i>O</i>) — Asymptotic Upper Bound", answer_bold_style),
    Paragraph("Used to describe the worst-case scenario. It guarantees that an algorithm will never take longer than this upper limit.", answer_body_style),
    Paragraph("• <i>Formal Definition:</i> <i>T</i>(<i>n</i>) = <i>O</i>(<i>f</i>(<i>n</i>)) if there exist positive constants <i>c</i> and <i>n</i><sub>0</sub> such that:<br/>0 ≤ <i>T</i>(<i>n</i>) ≤ <i>c</i>·<i>f</i>(<i>n</i>) for all <i>n</i> ≥ <i>n</i><sub>0</sub>.", answer_bullet_style),
    Paragraph("• <i>Example:</i> Let <i>T</i>(<i>n</i>) = 3<i>n</i> + 2. We can claim <i>T</i>(<i>n</i>) = <i>O</i>(<i>n</i>) because 3<i>n</i> + 2 ≤ 4<i>n</i> for all <i>n</i> ≥ 2. Here, our constants are <i>c</i> = 4 and <i>n</i><sub>0</sub> = 2.", answer_bullet_style),

    Paragraph("2. Big-Omega Notation (Ω) — Asymptotic Lower Bound", answer_bold_style),
    Paragraph("Used to describe the best-case scenario. It guarantees that an algorithm will take at least this much time.", answer_body_style),
    Paragraph("• <i>Formal Definition:</i> <i>T</i>(<i>n</i>) = Ω(<i>f</i>(<i>n</i>)) if there exist positive constants <i>c</i> and <i>n</i><sub>0</sub> such that:<br/>0 ≤ <i>c</i>·<i>f</i>(<i>n</i>) ≤ <i>T</i>(<i>n</i>) for all <i>n</i> ≥ <i>n</i><sub>0</sub>.", answer_bullet_style),
    Paragraph("• <i>Example:</i> Let <i>T</i>(<i>n</i>) = 3<i>n</i> + 2. We can claim <i>T</i>(<i>n</i>) = Ω(<i>n</i>) because 3<i>n</i> + 2 ≥ 3<i>n</i> for all <i>n</i> ≥ 1. Here, our constants are <i>c</i> = 3 and <i>n</i><sub>0</sub> = 1.", answer_bullet_style),

    Paragraph("3. Theta Notation (Θ) — Asymptotic Tight Bound", answer_bold_style),
    Paragraph("Used to describe the average-case running time. It bounds the function from both above and below.", answer_body_style),
    Paragraph("• <i>Formal Definition:</i> <i>T</i>(<i>n</i>) = Θ(<i>f</i>(<i>n</i>)) if there exist positive constants <i>c</i><sub>1</sub>, <i>c</i><sub>2</sub>, and <i>n</i><sub>0</sub> such that:<br/>0 ≤ <i>c</i><sub>1</sub>·<i>f</i>(<i>n</i>) ≤ <i>T</i>(<i>n</i>) ≤ <i>c</i><sub>2</sub>·<i>f</i>(<i>n</i>) for all <i>n</i> ≥ <i>n</i><sub>0</sub>.", answer_bullet_style),
    Paragraph("• <i>Example:</i> Let <i>T</i>(<i>n</i>) = 3<i>n</i> + 2. We can claim <i>T</i>(<i>n</i>) = Θ(<i>n</i>) because we can sandwich it: 3<i>n</i> ≤ 3<i>n</i> + 2 ≤ 4<i>n</i> for all <i>n</i> ≥ 2. Here, <i>c</i><sub>1</sub> = 3, <i>c</i><sub>2</sub> = 4, and <i>n</i><sub>0</sub> = 2.", answer_bullet_style),
]
elements.extend(make_subjective_qa("Q2.", "Short Answer", "Define Asymptotic Notations. Explain Big-Oh (O), Omega (Ω), and Theta (Θ) notations with suitable examples.", q2_ans))

# Q3: Compare Quick Sort and Merge Sort
t_headers = [Paragraph("<b>Comparison Parameter</b>", table_header_style), 
             Paragraph("<b>Quick Sort</b>", table_header_style), 
             Paragraph("<b>Merge Sort</b>", table_header_style)]

t_row1 = [Paragraph("<b>Design Paradigm</b>", table_text_style),
          Paragraph("Divide-and-Conquer. Relies on partitioning the array around a pivot element.", table_text_style),
          Paragraph("Divide-and-Conquer. Splits the array in halves recursively and merges them.", table_text_style)]

t_row2 = [Paragraph("<b>Time Complexity</b>", table_text_style),
          Paragraph("<b>Best/Average:</b> <i>O</i>(<i>n</i> log <i>n</i>)<br/><b>Worst-Case:</b> <i>O</i>(<i>n</i><sup>2</sup>) (when partition is highly skewed)", table_text_style),
          Paragraph("<b>Best/Average/Worst:</b> <i>O</i>(<i>n</i> log <i>n</i>) (highly consistent, independent of input order)", table_text_style)]

t_row3 = [Paragraph("<b>Auxiliary Space</b>", table_text_style),
          Paragraph("<i>O</i>(log <i>n</i>) (very efficient, in-place sorting relying only on recursion stack)", table_text_style),
          Paragraph("<i>O</i>(<i>n</i>) (requires an extra temporary array of size <i>n</i> to merge elements)", table_text_style)]

t_row4 = [Paragraph("<b>Stability</b>", table_text_style),
          Paragraph("<b>Unstable</b> (may swap equal elements and change their relative original positions)", table_text_style),
          Paragraph("<b>Stable</b> (guarantees relative order of equal elements is preserved)", table_text_style)]

t_row5 = [Paragraph("<b>Data Suitability</b>", table_text_style),
          Paragraph("Excellent for arrays due to high cache locality and in-place sorting.", table_text_style),
          Paragraph("Highly optimal for linked lists and massive external sorting files.", table_text_style)]

comp_table = Table([t_headers, t_row1, t_row2, t_row3, t_row4, t_row5], colWidths=[110, 200, 205])
# Added spacious table cell padding (8pt)
comp_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q3_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Quick Sort and Merge Sort are two of the most popular divide-and-conquer sorting algorithms. A comprehensive, spacious comparison is tabulated below:", answer_body_style),
    Spacer(1, 6),
    comp_table,
    Spacer(1, 6)
]
elements.extend(make_subjective_qa("Q3.", "Short Answer", "Compare Quick Sort and Merge Sort on the basis of their performance, memory usage, and time complexity.", q3_ans))

# Q4: Strassen's Matrix Multiplication
q4_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Conventional matrix multiplication of two <i>n</i> × <i>n</i> matrices requires splitting each into four submatrices of size <i>n</i>/2 × <i>n</i>/2, which leads to <b>8 recursive multiplications</b> and 4 additions. This yields the recurrence relation:<br/><i>T</i>(<i>n</i>) = 8<i>T</i>(<i>n</i>/2) + Θ(<i>n</i><sup>2</sup>). By Master Theorem, this solves to <b><i>O</i>(<i>n</i><sup>3</sup>)</b>.", answer_body_style),
    Paragraph("<b>Strassen's Breakthrough:</b> Volker Strassen showed that we can multiply matrices using only <b>7 multiplications</b> and 18 additions/subtractions, improving asymptotic performance.", answer_body_style),
    Paragraph("<b>The 7 Sub-Multiplication Products (P<sub>1</sub> to P<sub>7</sub>):</b>", answer_bold_style),
    Paragraph("Let matrices <i>A</i> and <i>B</i> be partitioned into <i>n</i>/2 × <i>n</i>/2 submatrices. The 7 strategic products are defined as:", answer_body_style),
    Paragraph("• <i>P</i><sub>1</sub> = <i>A</i><sub>11</sub> · (<i>B</i><sub>12</sub> - <i>B</i><sub>22</sub>)", answer_bullet_style),
    Paragraph("• <i>P</i><sub>2</sub> = (<i>A</i><sub>11</sub> + <i>A</i><sub>12</sub>) · <i>B</i><sub>22</sub>", answer_bullet_style),
    Paragraph("• <i>P</i><sub>3</sub> = (<i>A</i><sub>21</sub> + <i>A</i><sub>22</sub>) · <i>B</i><sub>11</sub>", answer_bullet_style),
    Paragraph("• <i>P</i><sub>4</sub> = <i>A</i><sub>22</sub> · (<i>B</i><sub>21</sub> - <i>B</i><sub>11</sub>)", answer_bullet_style),
    Paragraph("• <i>P</i><sub>5</sub> = (<i>A</i><sub>11</sub> + <i>A</i><sub>22</sub>) · (<i>B</i><sub>11</sub> + <i>B</i><sub>22</sub>)", answer_bullet_style),
    Paragraph("• <i>P</i><sub>6</sub> = (<i>A</i><sub>12</sub> - <i>A</i><sub>22</sub>) · (<i>B</i><sub>21</sub> + <i>B</i><sub>22</sub>)", answer_bullet_style),
    Paragraph("• <i>P</i><sub>7</sub> = (<i>A</i><sub>11</sub> - <i>A</i><sub>21</sub>) · (<i>B</i><sub>11</sub> + <i>B</i><sub>12</sub>)", answer_bullet_style),
    Paragraph("<b>Combining Products for Result Matrix C:</b>", answer_bold_style),
    Paragraph("• <i>C</i><sub>11</sub> = <i>P</i><sub>5</sub> + <i>P</i><sub>4</sub> - <i>P</i><sub>2</sub> + <i>P</i><sub>6</sub>", answer_bullet_style),
    Paragraph("• <i>C</i><sub>12</sub> = <i>P</i><sub>1</sub> + <i>P</i><sub>2</sub>", answer_bullet_style),
    Paragraph("• <i>C</i><sub>21</sub> = <i>P</i><sub>3</sub> + <i>P</i><sub>4</sub>", answer_bullet_style),
    Paragraph("• <i>C</i><sub>22</sub> = <i>P</i><sub>5</sub> + <i>P</i><sub>1</sub> - <i>P</i><sub>3</sub> - <i>P</i><sub>7</sub>", answer_bullet_style),
    Paragraph("<b>Derivation of Time Complexity:</b>", answer_bold_style),
    Paragraph("Since there are 7 recursive multiplications and additions take quadratic time for merging, the recurrence relation is:<br/><i>T</i>(<i>n</i>) = 7<i>T</i>(<i>n</i>/2) + Θ(<i>n</i><sup>2</sup>)", answer_body_style),
    Paragraph("Using the <b>Master Theorem</b> of the form <i>T</i>(<i>n</i>) = <i>aT</i>(<i>n</i>/<i>b</i>) + <i>f</i>(<i>n</i>):", answer_body_style),
    Paragraph("• <i>a</i> = 7, <i>b</i> = 2, and <i>f</i>(<i>n</i>) = Θ(<i>n</i><sup>2</sup>)", answer_bullet_style),
    Paragraph("• Compare <i>f</i>(<i>n</i>) with <i>n</i><sup>log<sub><i>b</i></sub><i>a</i></sup> = <i>n</i><sup>log<sub>2</sub>7</sup> ≈ <i>n</i><sup>2.81</sup>", answer_bullet_style),
    Paragraph("• Since 2 &lt; 2.81, this falls under Case 1 of Master Theorem.", answer_bullet_style),
    Paragraph("• Therefore, the complexity is <b>Θ(<i>n</i><sup>log<sub>2</sub>7</sup>) ≈ Θ(<i>n</i><sup>2.81</sup>)</b>.", answer_bullet_style),
    Paragraph("<b>How it Improves:</b> For large-scale matrices (typically <i>n</i> &gt; 128), Strassen's algorithm drastically reduces CPU multiplication operations. Standard matrix multiplication grows at a rate of <i>n</i><sup>3</sup>, whereas Strassen's grows at <i>n</i><sup>2.81</sup>, which saves billions of operations as the size scales.", answer_body_style),
]
elements.extend(make_subjective_qa("Q4.", "Long Answer", "Discuss Strassen's matrix multiplication algorithm. Derive its time complexity and explain how it improves upon conventional matrix multiplication.", q4_ans))

# Q5: Heap Sort Technique & Tracing (Completely redesigned into step-by-step paragraphs!)
q5_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Heap Sort</b> is a comparison-based sorting technique based on a Binary Heap data structure. It is an in-place algorithm that has a guaranteed running time of <i>O</i>(<i>n</i> log <i>n</i>).", answer_body_style),
    
    Paragraph("<b>Phase 1: Build Max-Heap (Step-by-Step heapification):</b>", answer_bold_style),
    Paragraph("We begin heapifying starting from the last non-leaf node index ⌊(11-2)/2⌋ = 4 (element 45) up to the root index 0:", answer_body_style),
    
    Paragraph("• <b>Heapify at Index 4 (Value 45):</b> Children are at index 9 (88) and index 10 (12). Since child 88 is greater than 45, we swap them.<br/>"
              "<i>Resulting Array State:</i> [81, 39, 10, 36, <b>88</b>, 15, 55, 23, 91, <b>45</b>, 12]", answer_bullet_style),
              
    Paragraph("• <b>Heapify at Index 3 (Value 36):</b> Children are at index 7 (23) and index 8 (91). Since child 91 is greater than 36, we swap them.<br/>"
              "<i>Resulting Array State:</i> [81, 39, 10, <b>91</b>, 88, 15, 55, 23, <b>36</b>, 45, 12]", answer_bullet_style),
              
    Paragraph("• <b>Heapify at Index 2 (Value 10):</b> Children are at index 5 (15) and index 6 (55). Since child 55 is greater than 10, we swap them.<br/>"
              "<i>Resulting Array State:</i> [81, 39, <b>55</b>, 91, 88, 15, <b>10</b>, 23, 36, 45, 12]", answer_bullet_style),
              
    Paragraph("• <b>Heapify at Index 1 (Value 39):</b> Children are at index 3 (91) and index 4 (88). Since child 91 is greater than 39, we swap them. No sub-heapify swap is needed as 39 is greater than its new children 23 and 36.<br/>"
              "<i>Resulting Array State:</i> [81, <b>91</b>, 55, <b>39</b>, 88, 15, 10, 23, 36, 45, 12]", answer_bullet_style),
              
    Paragraph("• <b>Heapify at Index 0 (Value 81):</b> Children are index 1 (91) and index 2 (55). Since 91 is greater, swap 81 and 91. Next, sub-heapify index 1 (value 81) with children index 3 (39) and index 4 (88). Swap 81 and 88.<br/>"
              "<i>Resulting Max-Heap State:</i> [<b>91</b>, <b>88</b>, 55, 39, <b>81</b>, 15, 10, 23, 36, 45, 12]", answer_bullet_style),
              
    Paragraph("<b>Max-Heap Constructed successfully:</b> <i>[91, 88, 55, 39, 81, 15, 10, 23, 36, 45, 12]</i>", answer_body_style),
    
    Paragraph("<b>Phase 2: Repeatedly Extract Max &amp; Sort:</b>", answer_bold_style),
    Paragraph("We swap the root element (index 0) with the last element of the active heap, reduce the heap size by 1, and heapify the root. We repeat this 10 times to sort the list:", answer_body_style),
    
    Paragraph("• <b>Step 1:</b> Swap root 91 and last index 12. Heap size = 10. Heapify root 12.<br/>"
              "<i>Active Heap:</i> [88, 81, 55, 39, 45, 15, 10, 23, 36, 12] | <i>Sorted:</i> [<b>91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 2:</b> Swap root 88 and last index 12. Heap size = 9. Heapify root 12.<br/>"
              "<i>Active Heap:</i> [81, 45, 55, 39, 12, 15, 10, 23, 36] | <i>Sorted:</i> [<b>88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 3:</b> Swap root 81 and last index 36. Heap size = 8. Heapify root 36.<br/>"
              "<i>Active Heap:</i> [55, 45, 36, 39, 12, 15, 10, 23] | <i>Sorted:</i> [<b>81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 4:</b> Swap root 55 and last index 23. Heap size = 7. Heapify root 23.<br/>"
              "<i>Active Heap:</i> [45, 39, 36, 23, 12, 15, 10] | <i>Sorted:</i> [<b>55, 81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 5:</b> Swap root 45 and last index 10. Heap size = 6. Heapify root 10.<br/>"
              "<i>Active Heap:</i> [39, 23, 36, 10, 12, 15] | <i>Sorted:</i> [<b>45, 55, 81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 6:</b> Swap root 39 and last index 15. Heap size = 5. Heapify root 15.<br/>"
              "<i>Active Heap:</i> [36, 23, 15, 10, 12] | <i>Sorted:</i> [<b>39, 45, 55, 81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 7:</b> Swap root 36 and last index 12. Heap size = 4. Heapify root 12.<br/>"
              "<i>Active Heap:</i> [23, 12, 15, 10] | <i>Sorted:</i> [<b>36, 39, 45, 55, 81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 8:</b> Swap root 23 and last index 10. Heap size = 3. Heapify root 10.<br/>"
              "<i>Active Heap:</i> [15, 12, 10] | <i>Sorted:</i> [<b>23, 36, 39, 45, 55, 81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 9:</b> Swap root 15 and last index 10. Heap size = 2. Heapify root 10.<br/>"
              "<i>Active Heap:</i> [12, 10] | <i>Sorted:</i> [<b>15, 23, 36, 39, 45, 55, 81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("• <b>Step 10:</b> Swap root 12 and last index 10. Heap size = 1. Active Heap stabilizes at root [10].<br/>"
              "<i>Sorted list:</i> [<b>10, 12, 15, 23, 36, 45, 55, 81, 88, 91</b>]", answer_bullet_style),
              
    Paragraph("<b>Final Sorted Output:</b> [10, 12, 15, 23, 36, 45, 55, 81, 88, 91]", answer_bold_style),
]
elements.extend(make_subjective_qa("Q5.", "Long Answer", "Explain the Heap sort technique. Trace the steps to sort the following array using heap sort: 81, 39, 10, 36, 45, 15, 55, 23, 91, 88, 12.", q5_ans))

# Q6: Design Merge Sort
q6_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Merge Sort</b> is a classic divide-and-conquer sorting algorithm. It divides the input array into two halves, calls itself for the two halves, and then merges the two sorted halves using a helper function.", answer_body_style),
    Paragraph("<b>Algorithm Pseudocode:</b>", answer_bold_style),
    Paragraph("<b>MERGE-SORT(A, p, r):</b>", code_style),
    Paragraph("1. <b>if</b> p &lt; r", code_style),
    Paragraph("2. &nbsp;&nbsp;&nbsp;&nbsp;q = ⌊(p + r) / 2⌋", code_style),
    Paragraph("3. &nbsp;&nbsp;&nbsp;&nbsp;MERGE-SORT(A, p, q)", code_style),
    Paragraph("4. &nbsp;&nbsp;&nbsp;&nbsp;MERGE-SORT(A, q + 1, r)", code_style),
    Paragraph("5. &nbsp;&nbsp;&nbsp;&nbsp;MERGE(A, p, q, r)", code_style),
    Spacer(1, 4),
    Paragraph("<b>MERGE(A, p, q, r):</b>", code_style),
    Paragraph("1. n1 = q - p + 1", code_style),
    Paragraph("2. n2 = r - q", code_style),
    Paragraph("3. Let L[1..n1+1] and R[1..n2+1] be new arrays", code_style),
    Paragraph("4. <b>for</b> i = 1 <b>to</b> n1: L[i] = A[p + i - 1]", code_style),
    Paragraph("5. <b>for</b> j = 1 <b>to</b> n2: R[j] = A[q + j]", code_style),
    Paragraph("6. L[n1 + 1] = ∞, R[n2 + 1] = ∞", code_style),
    Paragraph("7. i = 1, j = 1", code_style),
    Paragraph("8. <b>for</b> k = p <b>to</b> r", code_style),
    Paragraph("9. &nbsp;&nbsp;&nbsp;&nbsp;<b>if</b> L[i] ≤ R[j]", code_style),
    Paragraph("10. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A[k] = L[i]; i = i + 1", code_style),
    Paragraph("11. &nbsp;&nbsp;&nbsp;&nbsp;<b>else</b> A[k] = R[j]; j = j + 1", code_style),
    Paragraph("<b>Complexity Analysis:</b>", answer_bold_style),
    Paragraph("The division step takes constant time, and merging two arrays of sizes <i>n</i>/2 takes <i>O</i>(<i>n</i>) time. This leads to the recurrence relation:<br/><i>T</i>(<i>n</i>) = 2<i>T</i>(<i>n</i>/2) + <i>O</i>(<i>n</i>)", answer_body_style),
    Paragraph("• <b>Best-Case Time Complexity:</b> <i>O</i>(<i>n</i> log <i>n</i>) — Even if the array is already fully sorted, the recursive splitting and linear merging are executed.", answer_bullet_style),
    Paragraph("• <b>Average-Case Time Complexity:</b> <i>O</i>(<i>n</i> log <i>n</i>) — Occurs for arbitrary random arrays.", answer_bullet_style),
    Paragraph("• <b>Worst-Case Time Complexity:</b> <i>O</i>(<i>n</i> log <i>n</i>) — Occurs when elements are reverse sorted. It is highly robust as it does not rely on pivot selection.", answer_bullet_style),
]
elements.extend(make_subjective_qa("Q6.", "Long Answer", "Design the Merge Sort algorithm. Apply it to sort a given list and discuss its best-case, average-case, and worst-case time complexities.", q6_ans))

# ==========================================
# 4. UNIT 2 BANNER
# ==========================================
elements.append(make_section_banner("UNIT 2: STUDY OF GREEDY STRATEGY"))

# ==========================================
# UNIT 2 QUESTIONS & SOLUTIONS
# ==========================================

# Q1: Greedy Approach
q1_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The <b>Greedy Strategy</b> is an algorithmic paradigm that builds up a solution piece-by-piece, always choosing the next piece that offers the most immediate and obvious benefit (locally optimal choice) with the hope that these choices lead to a globally optimal solution.", answer_body_style),
    Paragraph("<b>Primary Characteristics of a Greedy Algorithm:</b>", answer_bold_style),
    Paragraph("• <b>Greedy Choice Property:</b> A globally optimal solution can be arrived at by making locally optimal (greedy) choices. The algorithm makes whatever choice seems best at the moment without looking ahead to future consequences.", answer_bullet_style),
    Paragraph("• <b>Optimal Substructure:</b> A problem exhibits optimal substructure if an optimal solution to the entire problem contains optimal solutions to its subproblems.", answer_bullet_style),
    Paragraph("• <b>Irreversibility (No Backtracking):</b> Once a decision is made in a greedy algorithm, it is completely permanent and cannot be altered or undone (unlike Backtracking or Dynamic Programming).", answer_bullet_style),
]
elements.extend(make_subjective_qa("Q1.", "Short Answer", "Describe the Greedy approach to algorithm designing. What are its primary characteristics?", q1_u2_ans))

# Q2: Kruskal vs Prim Table
k_headers = [Paragraph("<b>Parameter</b>", table_header_style), 
             Paragraph("<b>Kruskal's Algorithm</b>", table_header_style), 
             Paragraph("<b>Prim's Algorithm</b>", table_header_style)]

k_row1 = [Paragraph("<b>MST Growth Style</b>", table_text_style),
          Paragraph("Grows the Minimum Spanning Tree by selecting edges one-by-one based on sorting order.", table_text_style),
          Paragraph("Grows the Spanning Tree by connecting vertices one-by-one to a single root node.", table_text_style)]

k_row2 = [Paragraph("<b>Structure During Execution</b>", table_text_style),
          Paragraph("Maintains a 'forest' (a collection of disconnected trees) that eventually merges.", table_text_style),
          Paragraph("Maintains a single connected tree at all times during the algorithm.", table_text_style)]

k_row3 = [Paragraph("<b>Optimal Data Structures</b>", table_text_style),
          Paragraph("Disjoint Set Union (Union-Find) to detect cycles, and edge sorting.", table_text_style),
          Paragraph("Priority Queue (Min-Heap) and adjacency list representation.", table_text_style)]

k_row4 = [Paragraph("<b>Time Complexity</b>", table_text_style),
          Paragraph("<b><i>O</i>(<i>E</i> log <i>E</i>)</b> or <b><i>O</i>(<i>E</i> log <i>V</i>)</b> (dominated by initial sorting of edges)", table_text_style),
          Paragraph("<b><i>O</i>(<i>E</i> log <i>V</i>)</b> with binary heap; <b><i>O</i>(<i>E</i> + <i>V</i> log <i>V</i>)</b> with Fibonacci heap", table_text_style)]

k_row5 = [Paragraph("<b>Best Suited For</b>", table_text_style),
          Paragraph("Sparse graphs with relatively few edges (where <i>E</i> ≈ <i>V</i>).", table_text_style),
          Paragraph("Dense graphs with a high number of edges (where <i>E</i> ≈ <i>V</i><sup>2</sup>).", table_text_style)]

k_table = Table([k_headers, k_row1, k_row2, k_row3, k_row4, k_row5], colWidths=[110, 200, 205])
# Added spacious table cell padding (8pt)
k_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q2_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Both Kruskal's and Prim's are greedy algorithms used to construct a Minimum Spanning Tree (MST) of a connected weighted graph. Their core differences are tabulated below:", answer_body_style),
    Spacer(1, 6),
    k_table,
    Spacer(1, 6)
]
elements.extend(make_subjective_qa("Q2.", "Short Answer", "Tabulate the differences between Kruskal's and Prim's algorithms for finding a minimum cost spanning tree.", q2_u2_ans))

# Q3: Knapsack problem description
q3_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The <b>Knapsack Problem</b> is a classic optimization problem. Given a set of items, each with a weight <i>w</i><sub>i</sub> and a profit <i>p</i><sub>i</sub>, and a knapsack with maximum weight capacity <i>W</i>, the objective is to choose items to include in the knapsack to maximize the total profit without exceeding the capacity.", answer_body_style),
    Paragraph("<b>Fractional Knapsack Solution (Greedy Method):</b>", answer_bold_style),
    Paragraph("In the Fractional version, we can take fractions of items (e.g., liquid, powder). The Greedy Strategy yields the mathematically optimal solution via these steps:", answer_body_style),
    Paragraph("• <b>Calculate Profit Density:</b> For each item, compute the profit-to-weight ratio <i>r</i><sub>i</sub> = <i>p</i><sub>i</sub> / <i>w</i><sub>i</sub>.", answer_bullet_style),
    Paragraph("• <b>Sort Items:</b> Sort all items in descending order of their ratio <i>r</i><sub>i</sub>.", answer_bullet_style),
    Paragraph("• <b>Fill Knapsack Greedily:</b> Take as much of the item with the highest ratio as possible. If the knapsack capacity accommodates the entire item, pack it and subtract its weight from the capacity. If the capacity is less than the item's weight, take the exact fraction of the item that fills the remaining capacity and terminate.", answer_bullet_style),
]
elements.extend(make_subjective_qa("Q3.", "Short Answer", "What is the Knapsack problem? Briefly explain how the Fractional Knapsack problem is solved using the Greedy method.", q3_u2_ans))

# Q4: Dijkstra's Algorithm (Completely redesigned into step-by-step paragraphs!)
q4_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Dijkstra's Algorithm</b> solves the single-source shortest path problem on a directed or undirected graph with non-negative edge weights.", answer_body_style),
    Paragraph("<b>Algorithm Pseudocode:</b>", answer_bold_style),
    Paragraph("1. Initialize dist[v] = ∞ for all vertices, dist[source] = 0.", code_style),
    Paragraph("2. Create a priority queue Q containing all vertices with key as dist[v].", code_style),
    Paragraph("3. <b>while</b> Q is not empty:", code_style),
    Paragraph("4. &nbsp;&nbsp;&nbsp;&nbsp;u = Extract-Min(Q)", code_style),
    Paragraph("5. &nbsp;&nbsp;&nbsp;&nbsp;<b>for</b> each adjacent neighbor v of u:", code_style),
    Paragraph("6. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>if</b> dist[u] + weight(u, v) &lt; dist[v]:", code_style),
    Paragraph("7. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dist[v] = dist[u] + weight(u, v)", code_style),
    Paragraph("8. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decrease-Key(Q, v)", code_style),
    
    Paragraph("<b>Detailed Step-by-Step Distance Relaxation:</b>", answer_bold_style),
    Paragraph("Let us solve for source vertex <b>A</b> on a 5-vertex graph with edges: "
              "<i>A-B(4), A-C(2), B-C(1), B-D(5), C-D(8), C-E(10), D-E(2)</i>.", answer_body_style),
    
    Paragraph("• <b>Initialization:</b> Set source distance <i>dist[A] = 0</i> and all other vertex distances to <i>∞</i>.<br/>"
              "<i>Initial Distance Vector:</i> [A: 0, B: ∞, C: ∞, D: ∞, E: ∞]", answer_bullet_style),
              
    Paragraph("• <b>Step 1: Extract Source A (dist[A] = 0):</b><br/>"
              "Relax adjacent neighbors of A:<br/>"
              "- <i>dist[B]</i> = min(∞, 0 + 4) = <b>4</b><br/>"
              "- <i>dist[C]</i> = min(∞, 0 + 2) = <b>2</b><br/>"
              "<i>Distance Vector Updates:</i> [A: 0, B: 4, C: 2, D: ∞, E: ∞]", answer_bullet_style),
              
    Paragraph("• <b>Step 2: Extract Vertex C (dist[C] = 2):</b><br/>"
              "Relax adjacent neighbors of C:<br/>"
              "- <i>dist[B]</i> = min(4, 2 + 1) = <b>3</b> (Shorter path found!)<br/>"
              "- <i>dist[D]</i> = min(∞, 2 + 8) = <b>10</b><br/>"
              "- <i>dist[E]</i> = min(∞, 2 + 10) = <b>12</b><br/>"
              "<i>Distance Vector Updates:</i> [A: 0, B: 3, C: 2, D: 10, E: 12]", answer_bullet_style),
              
    Paragraph("• <b>Step 3: Extract Vertex B (dist[B] = 3):</b><br/>"
              "Relax adjacent neighbors of B:<br/>"
              "- <i>dist[D]</i> = min(10, 3 + 5) = <b>8</b> (Shorter path found!)<br/>"
              "<i>Distance Vector Updates:</i> [A: 0, B: 3, C: 2, D: 8, E: 12]", answer_bullet_style),
              
    Paragraph("• <b>Step 4: Extract Vertex D (dist[D] = 8):</b><br/>"
              "Relax adjacent neighbors of D:<br/>"
              "- <i>dist[E]</i> = min(12, 8 + 2) = <b>10</b> (Shorter path found!)<br/>"
              "<i>Distance Vector Updates:</i> [A: 0, B: 3, C: 2, D: 8, E: 10]", answer_bullet_style),
              
    Paragraph("• <b>Step 5: Extract Vertex E (dist[E] = 10):</b><br/>"
              "All vertices have successfully been extracted and processed.", answer_bullet_style),
              
    Paragraph("<b>Final Shortest Path Distances from A:</b> A = 0, B = 3, C = 2, D = 8, E = 10.", answer_bold_style),
]
elements.extend(make_subjective_qa("Q4.", "Long Answer", "Write an algorithm for the Single Source Shortest Path (Dijkstra's Algorithm). Explain it with a suitable graph example and discuss its time complexity.", q4_u2_ans))

# Q5: MST comparison (Completely redesigned into step-by-step paragraphs!)
q5_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Let us consider a weighted graph of 4 vertices: <b>A, B, C, D</b>, and 5 edges: <b>(A,B):1, (B,D):2, (B,C):3, (A,C):4, (C,D):5</b>.", answer_body_style),
    
    Paragraph("<b>Comparative Step-by-Step Edge Selection Trace:</b>", answer_bold_style),
    Paragraph("We trace Kruskal's (which sorts all edges) and Prim's (which grows from a starting tree, chosen here as starting vertex A):", answer_body_style),
    
    Paragraph("• <b>Edge 1: (A, B) [weight 1]:</b><br/>"
              "- <i>Kruskal's Action:</i> Selected. Vertices A and B are in disconnected components, so they are merged into component <i>{A, B}</i>.<br/>"
              "- <i>Prim's Action:</i> Selected as the cheapest edge adjacent to the starting tree <i>{A}</i>. Visited tree grows to <i>{A, B}</i>. MST Cost = 1.", answer_bullet_style),
              
    Paragraph("• <b>Edge 2: (B, D) [weight 2]:</b><br/>"
              "- <i>Kruskal's Action:</i> Selected. Vertices B and D are in disconnected components, so they are merged. Component becomes <i>{A, B, D}</i>.<br/>"
              "- <i>Prim's Action:</i> Selected as the cheapest edge adjacent to the visited tree <i>{A, B}</i>. Visited tree grows to <i>{A, B, D}</i>. MST Cost = 1 + 2 = 3.", answer_bullet_style),
              
    Paragraph("• <b>Edge 3: (B, C) [weight 3]:</b><br/>"
              "- <i>Kruskal's Action:</i> Selected. Vertices B and C are in disconnected components, so they are merged. All vertices are now connected. Component = <i>{A, B, C, D}</i>.<br/>"
              "- <i>Prim's Action:</i> Selected as the cheapest edge connecting visited tree <i>{A, B, D}</i> to unvisited vertex C. Visited tree becomes <i>{A, B, C, D}</i>. MST Cost = 3 + 3 = 6.", answer_bullet_style),
              
    Paragraph("• <b>Edge 4: (A, C) [weight 4]:</b><br/>"
              "- <i>Kruskal's Action:</i> Rejected. Both A and C are already in the same component. Adding this would form a cycle.<br/>"
              "- <i>Prim's Action:</i> Ignored. Both A and C are already in the visited tree (forms cycle).", answer_bullet_style),
              
    Paragraph("• <b>Edge 5: (C, D) [weight 5]:</b><br/>"
              "- <i>Kruskal's Action:</i> Rejected. Forms a cycle.<br/>"
              "- <i>Prim's Action:</i> Ignored. Forms a cycle.", answer_bullet_style),
              
    Paragraph("<b>Final Spanning Tree Cost:</b> Total Weight = 1 + 2 + 3 = 6 for both algorithms.", answer_bold_style),
]
elements.extend(make_subjective_qa("Q5.", "Long Answer", "Apply both Kruskal's and Prim's algorithms to find the Minimum Spanning Tree for a given weighted graph. Compare their time complexities.", q5_u2_ans))

# Q6: Job sequencing with deadlines
j_headers = [Paragraph("<b>Job ID</b>", table_header_style),
             Paragraph("<b>Profit</b>", table_header_style),
             Paragraph("<b>Deadline</b>", table_header_style),
             Paragraph("<b>Sorting Order (By Profit)</b>", table_header_style)]

j_row1 = [Paragraph("J<sub>1</sub>", table_text_style), Paragraph("100", table_text_style), Paragraph("2", table_text_style), Paragraph("1st (Highest)", table_text_style)]
j_row2 = [Paragraph("J<sub>2</sub>", table_text_style), Paragraph("19", table_text_style), Paragraph("1", table_text_style), Paragraph("4th", table_text_style)]
j_row3 = [Paragraph("J<sub>3</sub>", table_text_style), Paragraph("27", table_text_style), Paragraph("2", table_text_style), Paragraph("2nd", table_text_style)]
j_row4 = [Paragraph("J<sub>4</sub>", table_text_style), Paragraph("25", table_text_style), Paragraph("1", table_text_style), Paragraph("3rd", table_text_style)]
j_row5 = [Paragraph("J<sub>5</sub>", table_text_style), Paragraph("15", table_text_style), Paragraph("3", table_text_style), Paragraph("5th (Lowest)", table_text_style)]

j_table = Table([j_headers, j_row1, j_row2, j_row3, j_row4, j_row5], colWidths=[100, 100, 100, 215])
j_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
]))

g_headers = [Paragraph("<b>Time Slot</b>", table_header_style),
             Paragraph("<b>Scheduled Job</b>", table_header_style),
             Paragraph("<b>Profit Added</b>", table_header_style)]

g_row1 = [Paragraph("[0 to 1]", table_text_style), Paragraph("J<sub>3</sub> (Since slot [1-2] was occupied by J<sub>1</sub>, J<sub>3</sub> is placed in this empty slot)", table_text_style), Paragraph("27", table_text_style)]
g_row2 = [Paragraph("[1 to 2]", table_text_style), Paragraph("J<sub>1</sub> (Placed in the empty slot corresponding to its deadline of 2)", table_text_style), Paragraph("100", table_text_style)]
g_row3 = [Paragraph("[2 to 3]", table_text_style), Paragraph("J<sub>5</sub> (Placed in the empty slot corresponding to its deadline of 3)", table_text_style), Paragraph("15", table_text_style)]

gantt_table = Table([g_headers, g_row1, g_row2, g_row3], colWidths=[100, 315, 100])
gantt_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0D9488')), # Teal header for Gantt
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
]))

q6_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("We consider a set of 5 jobs, each with an associated profit and deadline as defined in the matrix below:", answer_body_style),
    Spacer(1, 6),
    j_table,
    Spacer(1, 6),
    Paragraph("<b>Step-by-Step Greedy Allocation:</b>", answer_bold_style),
    Paragraph("• <b>Maximum Timeline:</b> The maximum deadline is <b>3</b>. We establish 3 slots: [0-1], [1-2], and [2-3].", answer_bullet_style),
    Paragraph("• <b>Job J<sub>1</sub>:</b> Has the highest profit (100). We assign it to its preferred slot [1-2] (empty). Timeline = [ _, J<sub>1</sub>, _ ].", answer_bullet_style),
    Paragraph("• <b>Job J<sub>3</sub>:</b> Second highest profit (27, deadline 2). Slot [1-2] is occupied. We look left and place J<sub>3</sub> in the empty slot [0-1]. Timeline = [ J<sub>3</sub>, J<sub>1</sub>, _ ].", answer_bullet_style),
    Paragraph("• <b>Job J<sub>4</sub>:</b> Third highest profit (25, deadline 1). Preferred slot [0-1] is occupied by J<sub>3</sub>. No earlier slots exist. J<sub>4</sub> is rejected.", answer_bullet_style),
    Paragraph("• <b>Job J<sub>2</sub>:</b> Fourth highest profit (19, deadline 1). Slot [0-1] is occupied. J<sub>2</sub> is rejected.", answer_bullet_style),
    Paragraph("• <b>Job J<sub>5</sub>:</b> Lowest profit (15, deadline 3). We assign it to its preferred empty slot [2-3]. Timeline = [ J<sub>3</sub>, J<sub>1</sub>, J<sub>5</sub> ].", answer_bullet_style),
    Spacer(1, 6),
    Paragraph("<b>Final Scheduled Output Timeline:</b>", answer_bold_style),
    Spacer(1, 6),
    gantt_table,
    Spacer(1, 6),
    Paragraph("<b>Final Maximum Profit:</b> 27 + 100 + 15 = <b>142</b>.", answer_bold_style),
]
elements.extend(make_subjective_qa("Q6.", "Long Answer", "Find the maximum profit using the Job Sequencing with Deadline algorithm. (Be prepared to solve a numerical matrix featuring Jobs, Profits, and Deadlines).", q6_u2_ans))

# Build Document using NumberedCanvas for dynamic footer
doc.build(elements, canvasmaker=NumberedCanvas)

print(f"Subjective PDF generated successfully: {pdf_path}")
