import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Image
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
            self.drawString(100, 805, " |   Computer Organization & Architecture (COA) Solved Model Paper - III")
            self.drawRightString(555, 805, "Units 1 & 2 - Semester IV")
            
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
pdf_path = "COA_Unit_1_2_Model_Exam_Paper_3.pdf"

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

# Typography and Styling Theme (With generous breathing space)
title_style = ParagraphStyle(
    'TitleStyle',
    fontName=font_name_bold,
    fontSize=13.5,
    leading=18,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#1E3A8A'),
    spaceAfter=6
)

normal_style = ParagraphStyle(
    'NormalStyle',
    fontName=font_name,
    fontSize=9.5,
    leading=16.5,
    textColor=colors.HexColor('#1F2937'),
    spaceBefore=5,
    spaceAfter=5
)

bold_style = ParagraphStyle(
    'BoldStyle',
    fontName=font_name_bold,
    fontSize=9.5,
    leading=16.5,
    textColor=colors.HexColor('#1F2937'),
    spaceBefore=5,
    spaceAfter=5
)

section_header_style = ParagraphStyle(
    'SectionHeaderStyle',
    fontName=font_name_bold,
    fontSize=10.5,
    leading=14,
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
    leading=12,
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
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return KeepTogether([Spacer(1, 10), banner_table, Spacer(1, 8)])

def make_mcq_qa(num_str, q_text, options_list, correct_ans, explanation_text):
    q_style = ParagraphStyle(
        'McqQStyle',
        parent=normal_style,
        fontName=font_name_bold,
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
    )
    
    label = f"<b>{num_str}</b>"
    
    p_num = Paragraph(label, q_style)
    p_text = Paragraph(q_text, ParagraphStyle('McqQText', parent=normal_style, fontName=font_name_bold, fontSize=9.5, leading=14))
    
    q_table = Table([[p_num, p_text]], colWidths=[30, 485])
    q_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    flowables = [q_table, Spacer(1, 4)]
    
    # Format options (2-column table layout for compact visual style)
    opt_data = []
    for i in range(0, len(options_list), 2):
        row = []
        opt1 = options_list[i]
        row.append(Paragraph(f"<b>{opt1[0]}</b> &nbsp;{opt1[1]}", ParagraphStyle('McqOpt', parent=normal_style, leading=14)))
        if i+1 < len(options_list):
            opt2 = options_list[i+1]
            row.append(Paragraph(f"<b>{opt2[0]}</b> &nbsp;{opt2[1]}", ParagraphStyle('McqOpt', parent=normal_style, leading=14)))
        else:
            row.append(Paragraph("", normal_style))
        opt_data.append(row)
        
    opt_table = Table(opt_data, colWidths=[240, 245])
    opt_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 30),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    flowables.append(opt_table)
    flowables.append(Spacer(1, 4))
    
    # Answer and Explanation
    p_ans = Paragraph(f"<b>Answer:</b> <font color='#0D9488'><b>{correct_ans}</b></font>", ParagraphStyle('McqAns', parent=normal_style, leftIndent=30, fontName=font_name_bold, textColor=colors.HexColor('#1F2937')))
    p_exp = Paragraph(f"<i>Explanation:</i> {explanation_text}", ParagraphStyle('McqExp', parent=normal_style, leftIndent=30, fontSize=8.5, leading=12, textColor=colors.HexColor('#4B5563')))
    
    flowables.append(p_ans)
    flowables.append(p_exp)
    flowables.append(Spacer(1, 10))
    
    return KeepTogether(flowables)

def make_coa_qa(num_str, mark_str, q_text, answer_flowables):
    q_style = ParagraphStyle(
        'CoaQStyle',
        parent=normal_style,
        fontName=font_name_bold,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
    )
    
    label = f"<b>{num_str}</b>"
    
    full_q_text = f"{q_text}"
    if mark_str:
        full_q_text += f"<br/><font color='#0D9488' size='8'><b>[★ Marks: {mark_str}]</b></font>"
        
    p_num = Paragraph(label, q_style)
    p_text = Paragraph(full_q_text, ParagraphStyle('CoaQText', parent=normal_style, fontName=font_name_bold, fontSize=10, leading=15))
    
    q_table = Table([[p_num, p_text]], colWidths=[40, 475])
    q_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    flowables = []
    
    first_part = [q_table, Spacer(1, 6)]
    if answer_flowables:
        first_part.append(answer_flowables[0])
        
    flowables.append(KeepTogether(first_part))
    
    if len(answer_flowables) > 1:
        flowables.extend(answer_flowables[1:])
        
    flowables.append(Spacer(1, 18)) # Spaced-out question gap
    return flowables

def get_image_flowable(image_filename, width=380, height=220):
    """
    Safely loads a PNG/JPEG diagram, centers it using a table wrapper, 
    and returns the flowable object. Falls back to None if file doesn't exist.
    """
    if os.path.exists(image_filename):
        try:
            img = Image(image_filename, width=width, height=height)
            t_img = Table([[img]], colWidths=[495])
            t_img.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            return t_img
        except Exception as e:
            print(f"Error loading image {image_filename}: {e}")
    return None

elements = []

# ==========================================
# 1. EXAM HEADER PANEL (Page 1)
# ==========================================
header_data = [
    [Paragraph("<b><font color='#0D9488'>EMo Learners</font> &nbsp;|&nbsp; Premium Solved Model Exam Paper — III</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=15, leading=20, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>COMPUTER ORGANIZATION &amp; ARCHITECTURE (COA) SOLVED BANK</b>", ParagraphStyle('HSub', fontName=font_name_bold, fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>SISTec Academic Mid-Semester Pattern — Semester IV</b>", ParagraphStyle('HSub2', fontName=font_name_bold, fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#1F2937')))],
    [Paragraph("<b>Unit 1 (Basic Structure of Computer) &amp; Unit 2 (Computer Arithmetic &amp; Control Memory)</b>", ParagraphStyle('HDesc', fontName=font_name_bold, fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor('#4B5563')))]
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
elements.append(Spacer(1, 10))

# ==========================================
# 2. METADATA SECTION
# ==========================================
info_data = [
    [
        Paragraph("<b>Subject:</b> Computer Organization &amp; Architecture (CSIT-404)", normal_style),
        Paragraph("<b>Total Solved Marks:</b> 28 Marks", normal_style)
    ],
    [
        Paragraph("<b>Layout Structure:</b> Part A (MCQ), Part B (Short), Part C (Long Choice)", normal_style),
        Paragraph("<b>Branding Highlight:</b> EMo Learners Exclusive Solved Paper", normal_style)
    ]
]
info_table = Table(info_data, colWidths=[310, 205])
info_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LINEBELOW', (0, 1), (-1, 1), 0.75, colors.HexColor('#E2E8F0')),
]))
elements.append(info_table)

# ==========================================
# 3. PART A BANNER
# ==========================================
elements.append(make_section_banner("PART A: OBJECTIVE MULTIPLE CHOICE QUESTIONS (6 MARKS)"))
elements.append(Paragraph("<i>Instructions: Answer all twelve questions. Each question carries exactly <b>0.5 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 6))

# Q1
elements.append(make_mcq_qa(
    "Q.1",
    "What is meant by the Von-Neumann bottleneck?",
    [("A.", "CPU processing cycles are too slow"), ("B.", "Shared bus restricts simultaneous data and instruction fetch"), ("C.", "Registers are too small to store data"), ("D.", "Multiplexer selection delays the ALU")],
    "B. Shared bus restricts simultaneous data and instruction fetch",
    "Since instructions and data share the same physical bus in the Von-Neumann architecture, the CPU cannot read an instruction and read/write data at the same instant, throttling throughput."
))

# Q2
elements.append(make_mcq_qa(
    "Q.2",
    "In register transfer language (RTL), what does the expression 'P : R2 &larr; R1' represent?",
    [("A.", "R1 loads R2 at all clock pulses"), ("B.", "R1 and R2 swap values on condition P"), ("C.", "If Boolean condition P = 1, R2 loads contents of R1"), ("D.", "R2 is cleared if P = 0")],
    "C. If Boolean condition P = 1, R2 loads contents of R1",
    "P is a control function (Boolean condition). When P evaluates to 1, the target microoperation (transferring R1 to R2) is executed at the next clock edge."
))

# Q3
elements.append(make_mcq_qa(
    "Q.3",
    "Which addressing mode does not require a memory reference to fetch the operand?",
    [("A.", "Direct Addressing"), ("B.", "Indirect Addressing"), ("C.", "Immediate Addressing"), ("D.", "Relative Addressing")],
    "C. Immediate Addressing",
    "In immediate addressing, the operand is explicitly defined inside the instruction word itself, requiring zero memory access cycles to fetch data."
))

# Q4
elements.append(make_mcq_qa(
    "Q.4",
    "Which CPU register holds the address of the next instruction word to be fetched from memory?",
    [("A.", "Instruction Register (IR)"), ("B.", "Program Counter (PC)"), ("C.", "Accumulator (AC)"), ("D.", "Memory Address Register (MAR)")],
    "B. Program Counter (PC)",
    "The Program Counter (PC) is a dedicated register that points to and tracks the next instruction's address in system memory."
))

# Q5
elements.append(make_mcq_qa(
    "Q.5",
    "How many 8-to-1 multiplexers are required to construct a common bus system for eight 16-bit registers?",
    [("A.", "8 multiplexers"), ("B.", "16 multiplexers"), ("C.", "24 multiplexers"), ("D.", "128 multiplexers")],
    "B. 16 multiplexers",
    "A common bus system requires exactly one multiplexer for each bit line of the register size. For 16-bit registers, we need 16 multiplexers (each being 8-to-1 since there are 8 registers)."
))

# Q6
elements.append(make_mcq_qa(
    "Q.6",
    "What is the range of signed integers that can be stored in an 8-bit register using 2's complement representation?",
    [("A.", "-127 to +127"), ("B.", "-128 to +127"), ("C.", "-128 to +128"), ("D.", "0 to 255")],
    "B. -128 to +127",
    "Using n bits, 2's complement represents values from -2^(n-1) to +(2^(n-1) - 1). For 8 bits, this yields -128 to +127, featuring a unique single representation of zero."
))

# Q7
elements.append(make_mcq_qa(
    "Q.7",
    "In Booth's multiplication algorithm, what action is taken when the multiplier bits Q0 and Q<sub>-1</sub> are equal to '10'?",
    [("A.", "Shift only (ARS)"), ("B.", "Add multiplicand to accumulator, then shift"), ("C.", "Subtract multiplicand from accumulator, then shift"), ("D.", "Clear the accumulator")],
    "C. Subtract multiplicand from accumulator, then shift",
    "Booth's algorithm rules specify: 00 or 11 = shift only; 01 = add and shift; 10 = subtract (A = A - M) and shift."
))

# Q8
elements.append(make_mcq_qa(
    "Q.8",
    "What is the biased exponent offset value used in the standard IEEE 754 Single-Precision floating-point format?",
    [("A.", "127"), ("B.", "128"), ("C.", "1023"), ("D.", "255")],
    "A. 127",
    "IEEE 754 single-precision format uses 8 bits for the exponent with a bias of 127, allowing representation of exponents from -126 (stored as 1) to +127 (stored as 254)."
))

# Q9
elements.append(make_mcq_qa(
    "Q.9",
    "What timing component in a hardwired control unit is used to generate sequential timing state signals T0, T1, etc.?",
    [("A.", "Instruction Decoder"), ("B.", "Step Sequence Counter"), ("C.", "Control Address Register"), ("D.", "Control Memory ROM")],
    "B. Step Sequence Counter",
    "A step counter increments continuously on clock edges, feeding into a decoder that generates sequential timing states (T0, T1, T2) to guide microoperations."
))

# Q10
elements.append(make_mcq_qa(
    "Q.10",
    "Where are the control words (microinstructions) stored in a microprogrammed control unit?",
    [("A.", "Primary RAM"), ("B.", "CPU General Registers"), ("C.", "Control Memory (Internal ROM)"), ("D.", "Instruction Register")],
    "C. Control Memory (Internal ROM)",
    "In a microprogrammed control unit, control signals are pre-written as microcode and stored in a high-speed internal Control Memory ROM."
))

# Q11
elements.append(make_mcq_qa(
    "Q.11",
    "Which microinstruction organization offers higher parallel execution capabilities and faster operating speed?",
    [("A.", "Vertical Microinstruction"), ("B.", "Horizontal Microinstruction"), ("C.", "Encoded Microinstruction"), ("D.", "Indirect Microinstruction")],
    "B. Horizontal Microinstruction",
    "Horizontal microinstructions dedicate a separate bit to each physical control line. This eliminates decoding delays, allowing multiple microoperations to execute in parallel instantly."
))

# Q12
elements.append(make_mcq_qa(
    "Q.12",
    "In Restoring Binary Division, what action is taken when the partial remainder in register A becomes negative (MSB = 1) after subtraction?",
    [("A.", "Set quotient bit Q0 = 1"), ("B.", "Add divisor back to A to restore its state, and set Q0 = 0"), ("C.", "Arithmetic right shift A-Q"), ("D.", "Terminate the division loop")],
    "B. Add divisor back to A to restore its state, and set Q0 = 0",
    "Restoring division subtracts the divisor. If the result is negative, it must 'restore' the original value by adding the divisor back, setting the quotient bit Q0 to 0."
))

elements.append(PageBreak())

# ==========================================
# 4. PART B BANNER
# ==========================================
elements.append(make_section_banner("PART B: SHORT ANSWER QUESTIONS (8 MARKS)"))

# Section 1 Header
elements.append(Paragraph("<b>Section 1: Unit 1 (Basic Structure of Computer)</b>", answer_bold_style))
elements.append(Paragraph("<i>Instructions: Answer any <b>two</b> of the following three questions. Each question carries <b>2 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 4))

# Q1 Unit 1
t1_headers = [Paragraph("<b>Parameter</b>", table_header_style), 
              Paragraph("<b>Direct Addressing Mode</b>", table_header_style), 
              Paragraph("<b>Indirect Addressing Mode</b>", table_header_style)]

t1_row1 = [Paragraph("<b>Effective Address (EA)</b>", table_text_style), 
           Paragraph("EA = Address Field (A). Directly points to operand location in memory.", table_text_style), 
           Paragraph("EA = M[A]. Points to a pointer register/memory containing actual EA.", table_text_style)]

t1_row2 = [Paragraph("<b>Memory References</b>", table_text_style), 
           Paragraph("<b>1 reference</b> to read operand.", table_text_style), 
           Paragraph("<b>2 references</b> (1st to read pointer, 2nd for actual operand).", table_text_style)]

t1_row3 = [Paragraph("<b>Execution Speed</b>", table_text_style), 
           Paragraph("Fast due to fewer memory access cycles.", table_text_style), 
           Paragraph("Slower due to overhead of double memory access.", table_text_style)]

t1_row4 = [Paragraph("<b>Flexibility</b>", table_text_style), 
           Paragraph("Limited; hard to implement dynamic reference structures.", table_text_style), 
           Paragraph("High; essential for array pointers and list traversals.", table_text_style)]

t1_row5 = [Paragraph("<b>Assembly Example</b>", table_text_style), 
           Paragraph("`ADD 250H` &rarr; Adds value at address 250H directly to AC.", table_text_style), 
           Paragraph("`ADD [250H]` &rarr; Reads 250H for pointer, adds that target to AC.", table_text_style)]

t1_table = Table([t1_headers, t1_row1, t1_row2, t1_row3, t1_row4, t1_row5], colWidths=[110, 200, 205])
t1_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q1_u1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Direct and Indirect addressing modes are compared below in a structured table:", answer_body_style),
    Spacer(1, 4),
    t1_table,
]
elements.extend(make_coa_qa("Q.1", "2.0", "Compare Direct and Indirect addressing modes with suitable examples.", q1_u1_ans))

# Q2 Unit 1
t2_headers = [Paragraph("<b>Parameter</b>", table_header_style), 
              Paragraph("<b>Hardwired Control Unit</b>", table_header_style), 
              Paragraph("<b>Microprogrammed Control Unit</b>", table_header_style)]

t2_row1 = [Paragraph("<b>Construction</b>", table_text_style), 
           Paragraph("Built using **combinational hardware circuits** (decoders, gates, step-counters).", table_text_style), 
           Paragraph("Built using a systematic **Control Memory ROM** storing microcode words.", table_text_style)]

t2_row2 = [Paragraph("<b>Complexity</b>", table_text_style), 
           Paragraph("Extremely high and customized, grows with instruction set size.", table_text_style), 
           Paragraph("Systematic and clean, modular instruction sequencing logic.", table_text_style)]

t2_row3 = [Paragraph("<b>Operating Speed</b>", table_text_style), 
           Paragraph("<b>Very fast</b> (gate propagation delays only).", table_text_style), 
           Paragraph("Slower due to memory read cycle latency of Control ROM.", table_text_style)]

t2_row4 = [Paragraph("<b>Flexibility</b>", table_text_style), 
           Paragraph("Very rigid; modifying instructions requires physical rewiring.", table_text_style), 
           Paragraph("Highly flexible; can add instructions by updating microcode in ROM.", table_text_style)]

t2_row5 = [Paragraph("<b>Cost & Application</b>", table_text_style), 
           Paragraph("High development cost; preferred in **RISC** cores for raw speed.", table_text_style), 
           Paragraph("Lower design cost; widely used in complex instruction **CISC** cores.", table_text_style)]

t2_table = Table([t2_headers, t2_row1, t2_row2, t2_row3, t2_row4, t2_row5], colWidths=[110, 200, 205])
t2_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q2_u1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Hardwired and Microprogrammed control units are compared in the table below:", answer_body_style),
    Spacer(1, 4),
    t2_table,
]
elements.extend(make_coa_qa("Q.2", "2.0", "Differentiate between Hardwired and Microprogrammed control units with respect to design complexity and flexibility.", q2_u1_ans))

# Q3 Unit 1
q3_u1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The <b>Von-Neumann Bottleneck</b> is a throughput limitation where CPU processing speeds are severely throttled because the data/instruction throughput of the shared bus is much slower than internal CPU processing speeds.", answer_body_style),
    Paragraph("• <b>Causes:</b> Instructions and data share the exact same physical memory bus. The CPU cannot perform an instruction fetch and a data read/write at the same instant.", answer_bullet_style),
    Paragraph("• <b>Mitigation Techniques:</b>", answer_bold_style),
    Paragraph("1. **Cache Memories:** Integrating high-speed L1/L2/L3 SRAM caches inside the CPU.", answer_bullet_style),
    Paragraph("2. **Harvard Architecture:** Splitting instruction caches and data caches into physically separate structures.", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.3", "2.0", "Define the Von-Neumann Bottleneck and its main causes. List two mitigation techniques.", q3_u1_ans))

# Section 2 Header
elements.append(Paragraph("<b>Section 2: Unit 2 (Computer Arithmetic &amp; Control Memory)</b>", answer_bold_style))
elements.append(Paragraph("<i>Instructions: Answer any <b>two</b> of the following three questions. Each question carries <b>2 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 4))

# Q4 Unit 2
q4_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>1's Complement:</b> Formed by inverting all bits of the positive integer (0 to 1, 1 to 0).", answer_bullet_style),
    Paragraph("• <b>2's Complement:</b> Formed by adding 1 to the Least Significant Bit (LSB) of the 1's complement representation.", answer_bullet_style),
    Paragraph("• <b>Advantages in Signed Arithmetic:</b>", answer_bold_style),
    Paragraph("1. <b>No Subtraction Circuitry Needed:</b> Subtraction is performed simply by adding the 2's complement of the subtrahend (A - B = A + (-B)).", answer_bullet_style),
    Paragraph("2. <b>Unique Representation of Zero:</b> 2's complement has a single representation for zero (`00000000`), avoiding the ambiguous '+0' and '-0' found in 1's complement. This significantly simplifies ALU hardware zero-testing logic.", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.4", "2.0", "Define 1's complement and 2's complement representation and list their advantages in signed arithmetic operations.", q4_u2_ans))

# Q5 Unit 2
t5_headers = [Paragraph("<b>Parameter</b>", table_header_style), 
              Paragraph("<b>Fixed-Point Representation</b>", table_header_style), 
              Paragraph("<b>Floating-Point Representation</b>", table_header_style)]

t5_row1 = [Paragraph("<b>Radix Point Position</b>", table_text_style), 
           Paragraph("Fixed at a constant position (e.g. at the end for integers).", table_text_style), 
           Paragraph("Floats dynamically; represented in scientific notation (M &times; R<sup>E</sup>).", table_text_style)]

t5_row2 = [Paragraph("<b>Range of Values</b>", table_text_style), 
           Paragraph("<b>Narrow and limited</b> range for a given register bit width.", table_text_style), 
           Paragraph("<b>Extremely large</b> range (handles tiny fractions and massive values).", table_text_style)]

t5_row3 = [Paragraph("<b>Precision</b>", table_text_style), 
           Paragraph("<b>Uniform and constant</b> spacing between representable values.", table_text_style), 
           Paragraph("<b>Variable precision</b> (high near zero, decreases for larger numbers).", table_text_style)]

t5_row4 = [Paragraph("<b>Hardware Cost</b>", table_text_style), 
           Paragraph("Low; simple adder and shift circuits.", table_text_style), 
           Paragraph("High; requires dedicated **Floating Point Unit (FPU)** logic.", table_text_style)]

t5_row5 = [Paragraph("<b>Arithmetic Speed</b>", table_text_style), 
           Paragraph("Fast and direct execution cycles.", table_text_style), 
           Paragraph("Slower due to alignment, normalization, and rounding steps.", table_text_style)]

t5_table = Table([t5_headers, t5_row1, t5_row2, t5_row3, t5_row4, t5_row5], colWidths=[110, 200, 205])
t5_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q5_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Fixed-point and Floating-point number representations are compared below:", answer_body_style),
    Spacer(1, 4),
    t5_table,
]
elements.extend(make_coa_qa("Q.5", "2.0", "Analyze the difference between fixed-point and floating-point number representation in terms of range and precision.", q5_u2_ans))

# Q6 Unit 2
q6_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The standard IEEE 754 format uses a <b>biased exponent</b> (bias of 127 for 8-bit single-precision exponents) to allow representation of both positive and negative powers of 2 without requiring a sign bit inside the exponent field.", answer_body_style),
    Paragraph("• <b>Simplification of Comparisons:</b> Representing exponents as unsigned positive numbers (ranging from 1 to 254, corresponding to actual exponents -126 to +127) allows high-speed hardware comparators to compare floating-point magnitudes directly using standard integer comparison logic, without needing complex signed math operators.", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.6", "2.0", "Explain the concept and advantages of a biased exponent in IEEE 754 floating-point representation.", q6_u2_ans))

elements.append(PageBreak())

# ==========================================
# 5. PART C BANNER
# ==========================================
elements.append(make_section_banner("PART C: LONG ANSWER & TRACING QUESTIONS (14 MARKS)"))

# Set 1 Header
elements.append(Paragraph("<b>Set 1: Unit 1 (Basic Structure of Computer)</b>", answer_bold_style))
elements.append(Paragraph("<i>Instructions: Answer any <b>one</b> of the following two questions (with internal choice). The question carries <b>7 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 4))

# Q7 [a] General Register Organization
q7_set1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In a <b>General Register Organization</b>, multiple registers are connected through a common internal bus system feeding into a central ALU.", answer_body_style),
    Paragraph("<b>1. Bus-based CPU Register Organization Schematic:</b>", answer_bold_style),
]

# Safely load the register_org.png image if it exists
reg_image = get_image_flowable('register_org.png', width=380, height=220)
if reg_image:
    q7_set1_ans.append(reg_image)
    q7_set1_ans.append(Spacer(1, 4))
else:
    q7_set1_ans.append(Paragraph("<i>[Diagram: General-purpose Registers &rarr; Multiplexers (MUX A &amp; MUX B) &rarr; ALU &rarr; Decoder &rarr; Registers]</i>", code_style))

q7_set1_ans.extend([
    Paragraph("<b>2. Step-by-Step Execution of R1 &larr; R2 + R3:</b>", answer_bold_style),
    Paragraph("To execute the addition microoperation in a single clock cycle, the control unit coordinates the internal buses as follows:", answer_body_style),
    Paragraph("• <b>Select Source Operands (T1):</b> The control unit configures the multiplexer select lines **SELA** to place the contents of R2 onto Bus A, and **SELB** to place the contents of R3 onto Bus B.", answer_bullet_style),
    Paragraph("• <b>ALU Operation Selection (T2):</b> The control unit configures the ALU operation selector **OPR** to perform addition.", answer_bullet_style),
    Paragraph("• <b>Write Back Result (T3):</b> The addition sum is placed on the Result Bus C. The control unit configures the destination decoder **SELD** to enable the **Load (LD)** line of register R1. On the next active clock edge, R1 locks in the sum.", answer_bullet_style),
])
elements.extend(make_coa_qa("Q.7 [a]", "7.0", "Explain the general register organization of the CPU with a neat block diagram and detail the step-by-step role of ALU and internal buses in executing R1 &larr; R2 + R3.", q7_set1_ans))

elements.append(Paragraph("<b><font size='10' color='#0D9488'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;---------------------- OR ----------------------</font></b>", normal_style))
elements.append(Spacer(1, 4))

# Q7 [b] Structure of Desktop Computer
q7_set2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A desktop computer's logical architecture is built on the classic <b>Von Neumann Architecture</b>, containing the CPU, Memory, and Input/Output units.", answer_body_style),
    Paragraph("<b>1. Von Neumann Architecture Hardware Block Diagram:</b>", answer_bold_style),
]

# Safely load the von_neumann.png image if it exists
v_image = get_image_flowable('von_neumann.png', width=380, height=220)
if v_image:
    q7_set2_ans.append(v_image)
    q7_set2_ans.append(Spacer(1, 4))
else:
    q7_set2_ans.append(Paragraph("<i>[Diagram: Input Devices &rarr; CPU (Control Unit + ALU + Registers) &harr; Main Memory &rarr; Output Devices]</i>", code_style))

q7_set2_ans.extend([
    Paragraph("<b>2. Key Functional Units and Their Roles:</b>", answer_bold_style),
    Paragraph("• <b>Input Unit:</b> Translates human and external physical signals (from keyboard, mouse, scanners) into binary codes that can be loaded into system memory and CPU.", answer_bullet_style),
    Paragraph("• <b>Output Unit:</b> Converts binary values processed by the computer back into physical human-readable forms (monitors, printers, speakers).", answer_bullet_style),
    Paragraph("• <b>Memory Unit (Main Memory / RAM):</b> Stores active programs, variable data, and instructions currently being processed by the CPU. The address bus points to words, and the data bus fetches/writes them.", answer_bullet_style),
    Paragraph("• <b>Arithmetic &amp; Logic Unit (ALU):</b> Performs the core mathematical operations (addition, subtraction, multiplication) and relational logical comparisons (AND, OR, NOT, comparisons).", answer_bullet_style),
    Paragraph("• <b>Control Unit (CU):</b> Acts as the nervous system of the CPU. It continuously fetches instructions from memory, decodes their operation fields, and generates timing strobe signals to manage registers, ALU, memory, and bus flows.", answer_bullet_style),
])

elements.extend(make_coa_qa("Q.7 [b]", "7.0", "Explain the structure of a desktop computer with a neat block diagram and describe the function of each major unit (Input, Output, Memory, CPU Control Unit, and ALU).", q7_set2_ans))

elements.append(PageBreak())

# Set 2 Header
elements.append(Paragraph("<b>Set 2: Unit 2 (Computer Arithmetic &amp; Control Memory)</b>", answer_bold_style))
elements.append(Paragraph("<i>Instructions: Answer any <b>one</b> of the following two questions (with internal choice). The question carries <b>7 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 4))

# Q8 [a] Booth's multiplication trace
b_headers = [Paragraph("<b>Cycle / Action Step</b>", table_header_style), 
             Paragraph("<b>Accumulator (A)</b>", table_header_style), 
             Paragraph("<b>Multiplier (Q)</b>", table_header_style),
             Paragraph("<b>Q_(-1)</b>", table_header_style),
             Paragraph("<b>SC</b>", table_header_style)]

b_row1 = [Paragraph("Initial State", table_text_style), Paragraph("000000", table_text_style), Paragraph("110111", table_text_style), Paragraph("0", table_text_style), Paragraph("6", table_text_style)]
b_row2 = [Paragraph("Cycle 1: Q<sub>0</sub>Q<sub>-1</sub> = 10 &rarr; A = A - M<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ARS only", table_text_style), Paragraph("110011<br/>111001", table_text_style), Paragraph("110111<br/>111011", table_text_style), Paragraph("0<br/>1", table_text_style), Paragraph("6<br/>5", table_text_style)]
b_row3 = [Paragraph("Cycle 2: Q<sub>0</sub>Q<sub>-1</sub> = 11 &rarr; ARS only", table_text_style), Paragraph("111100", table_text_style), Paragraph("111101", table_text_style), Paragraph("1", table_text_style), Paragraph("4", table_text_style)]
b_row4 = [Paragraph("Cycle 3: Q<sub>0</sub>Q<sub>-1</sub> = 11 &rarr; ARS only", table_text_style), Paragraph("111110", table_text_style), Paragraph("011110", table_text_style), Paragraph("1", table_text_style), Paragraph("3", table_text_style)]
b_row5 = [Paragraph("Cycle 4: Q<sub>0</sub>Q<sub>-1</sub> = 01 &rarr; A = A + M<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ARS only", table_text_style), Paragraph("001011<br/>000101", table_text_style), Paragraph("011110<br/>101111", table_text_style), Paragraph("1<br/>0", table_text_style), Paragraph("3<br/>2", table_text_style)]
b_row6 = [Paragraph("Cycle 5: Q<sub>0</sub>Q<sub>-1</sub> = 10 &rarr; A = A - M<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ARS only", table_text_style), Paragraph("111000<br/>111100", table_text_style), Paragraph("101111<br/>010111", table_text_style), Paragraph("0<br/>1", table_text_style), Paragraph("2<br/>1", table_text_style)]
b_row7 = [Paragraph("Cycle 6: Q<sub>0</sub>Q<sub>-1</sub> = 11 &rarr; ARS only", table_text_style), Paragraph("111110", table_text_style), Paragraph("001011", table_text_style), Paragraph("1", table_text_style), Paragraph("0", table_text_style)]

b_table = Table([b_headers, b_row1, b_row2, b_row3, b_row4, b_row5, b_row6, b_row7], colWidths=[205, 110, 110, 50, 40])
b_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q8_set1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Let us multiply <b>(+13) &times; (-9)</b> using Booth's Algorithm in 6-bit signed 2's complement representation:", answer_body_style),
    Paragraph("• Multiplicand (M) = <b>+13</b> = <b>001101<sub>2</sub></b><br/>"
              "• Negative Multiplicand (-M) = <b>-13</b> = <b>110011<sub>2</sub></b> (2's complement of 001101)<br/>"
              "• Multiplier (Q) = <b>-9</b> = <b>110111<sub>2</sub></b> (2's complement of 001001)", answer_bullet_style),
    Paragraph("• **Registers:** Accumulator (A) = <b>000000</b> (6 bits), Q<sub>-1</sub> = <b>0</b> (1 bit), SC = <b>6</b>.", answer_bullet_style),
    Spacer(1, 4),
    Paragraph("<b>Cycle-by-Cycle Tracing Table:</b>", answer_bold_style),
    Spacer(1, 4),
    b_table,
    Spacer(1, 6),
    Paragraph("<b>Result Verification:</b>", answer_bold_style),
    Paragraph("The final combined register contents are <b>A Q = 111110001011<sub>2</sub></b> (12 bits signed).", answer_body_style),
    Paragraph("Since the MSB is 1, the result is negative. Let's find its magnitude via 2's complement:<br/>"
              "1. Invert all bits &rarr; 000001110100<br/>"
              "2. Add 1 &rarr; 000001110101<sub>2</sub><br/>"
              "3. Convert to decimal &rarr; 2<sup>6</sup> + 2<sup>5</sup> + 2<sup>4</sup> + 2<sup>2</sup> + 2<sup>0</sup> = 64 + 32 + 16 + 4 + 1 = 117.<br/>"
              "Therefore, the value is <b>-117</b>. Multiplying (+13) &times; (-9) yields <b>-117</b>. The trace is correct!", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.8 [a]", "7.0", "Explain Booth's multiplication algorithm. Trace the step-by-step signed multiplication process to multiply (+13) and (-9) in 6-bit binary, showing the Accumulator, Multiplier, and Q<sub>-1</sub> registers.", q8_set1_ans))

elements.append(Paragraph("<b><font size='10' color='#0D9488'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;---------------------- OR ----------------------</font></b>", normal_style))
elements.append(Spacer(1, 4))

# Q8 [b] Restoring Division Tracing Table (11 / 4)
r_headers = [Paragraph("<b>Cycle / Action Step</b>", table_header_style), 
             Paragraph("<b>Accumulator (A)</b>", table_header_style), 
             Paragraph("<b>Multiplier (Q)</b>", table_header_style),
             Paragraph("<b>SC</b>", table_header_style)]

r_row1 = [Paragraph("Initial State (Dividend Q=1011, Divisor M=0100, -M=1100)", table_text_style), Paragraph("0000", table_text_style), Paragraph("1011", table_text_style), Paragraph("4", table_text_style)]
r_row2 = [Paragraph("<b>Cycle 1:</b><br/>"
                   "1. Shift Left AQ<br/>"
                   "2. Subtract M (A &larr; A + (-M))<br/>"
                   "3. Remainder is negative (MSB=1) &rarr; Set Q<sub>0</sub> = 0<br/>"
                   "4. Restore A (A &larr; A + M)", table_text_style), 
          Paragraph("0001<br/>1101<br/>1101<br/>0001", table_text_style), 
          Paragraph("011_<br/>011_<br/>0110<br/>0110", table_text_style), 
          Paragraph("4<br/>-<br/>-<br/>3", table_text_style)]

r_row3 = [Paragraph("<b>Cycle 2:</b><br/>"
                   "1. Shift Left AQ<br/>"
                   "2. Subtract M (A &larr; A + (-M))<br/>"
                   "3. Remainder is negative (MSB=1) &rarr; Set Q<sub>0</sub> = 0<br/>"
                   "4. Restore A (A &larr; A + M)", table_text_style), 
          Paragraph("0010<br/>1110<br/>1110<br/>0010", table_text_style), 
          Paragraph("110_<br/>110_<br/>1100<br/>1100", table_text_style), 
          Paragraph("3<br/>-<br/>-<br/>2", table_text_style)]

r_row4 = [Paragraph("<b>Cycle 3:</b><br/>"
                   "1. Shift Left AQ<br/>"
                   "2. Subtract M (A &larr; A + (-M))<br/>"
                   "3. Remainder is positive (MSB=0) &rarr; Set Q<sub>0</sub> = 1<br/>"
                   "4. No Restore", table_text_style), 
          Paragraph("0101<br/>0001<br/>0001<br/>0001", table_text_style), 
          Paragraph("100_<br/>100_<br/>1001<br/>1001", table_text_style), 
          Paragraph("2<br/>-<br/>-<br/>1", table_text_style)]

r_row5 = [Paragraph("<b>Cycle 4:</b><br/>"
                   "1. Shift Left AQ<br/>"
                   "2. Subtract M (A &larr; A + (-M))<br/>"
                   "3. Remainder is negative (MSB=1) &rarr; Set Q<sub>0</sub> = 0<br/>"
                   "4. Restore A (A &larr; A + M)", table_text_style), 
          Paragraph("0011<br/>1111<br/>1111<br/>0011", table_text_style), 
          Paragraph("001_<br/>001_<br/>0010<br/>0010", table_text_style), 
          Paragraph("1<br/>-<br/>-<br/>0", table_text_style)]

r_table = Table([r_headers, r_row1, r_row2, r_row3, r_row4, r_row5], colWidths=[235, 130, 110, 40])
r_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q8_set2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In <b>Restoring Division</b>, the divisor M is subtracted from A in each cycle. If the MSB of A is 1 (negative result), the original state is 'restored' by adding M back to A, and the quotient bit Q<sub>0</sub> is set to 0. Otherwise, the remainder remains active and Q<sub>0</sub> is set to 1.", answer_body_style),
    Paragraph("<b>Step-by-Step Hardware Tracing Table (11 &divide; 4):</b>", answer_bold_style),
    Spacer(1, 4),
    r_table,
    Spacer(1, 6),
    Paragraph("<b>Final Verification:</b>", answer_bold_style),
    Paragraph("• <b>Quotient (Q):</b> `0010` &rarr; <b>2 in decimal</b>", answer_bullet_style),
    Paragraph("• <b>Remainder (A):</b> `0011` &rarr; <b>3 in decimal</b>", answer_bullet_style),
    Paragraph("Checking our arithmetic: Dividend = (Divisor &times; Quotient) + Remainder &rarr; 11 = (4 &times; 2) + 3. The tracing process is perfectly correct!", answer_bold_style),
]
elements.extend(make_coa_qa("Q.8 [b]", "7.0", "Perform binary division of 11 divided by 4 using the Restoring division method with a step-by-step hardware trace.", q8_set2_ans))

# Build Document using NumberedCanvas for dynamic footer page counting
doc.build(elements, canvasmaker=NumberedCanvas)

print(f"COA Solved Model Exam Paper 3 PDF generated successfully: {pdf_path}")
