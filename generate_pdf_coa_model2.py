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
            self.drawString(100, 805, " |   Computer Organization & Architecture (COA) Solved Model Paper - II")
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
pdf_path = "COA_Unit_1_2_Model_Exam_Paper_2.pdf"

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

elements = []

# ==========================================
# 1. EXAM HEADER PANEL (Page 1)
# ==========================================
header_data = [
    [Paragraph("<b><font color='#0D9488'>EMo Learners</font> &nbsp;|&nbsp; Premium Solved Model Exam Paper — II</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=15, leading=20, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
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
        Paragraph("<b>Subject:</b> Computer Organization &amp; Architecture (CS-404)", normal_style),
        Paragraph("<b>Total Solved Marks:</b> 28 Marks", normal_style)
    ],
    [
        Paragraph("<b>Layout Structure:</b> Part A (MCQ), Part B (Short), Part C (Long)", normal_style),
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
    "What is the default primary register in the CPU's execution core that acts as the implicit destination/source for single-operand instructions like ADD X?",
    [("A.", "Program Counter (PC)"), ("B.", "Accumulator (AC)"), ("C.", "Memory Address Register (MAR)"), ("D.", "Instruction Register (IR)")],
    "B. Accumulator (AC)",
    "In single-operand instruction architectures (like the basic computer), the Accumulator (AC) is the implied destination and first source operand register, saving instruction bits."
))

# Q2
elements.append(make_mcq_qa(
    "Q.2",
    "What is the correct logical sequencing of phases during instruction cycle execution?",
    [("A.", "Execute -> Decode -> Fetch"), ("B.", "Fetch -> Decode -> Fetch Operand -> Execute -> Write Back"), ("C.", "Decode -> Fetch -> Execute"), ("D.", "Fetch -> Execute -> Interrupt Check -> Decode")],
    "B. Fetch -> Decode -> Fetch Operand -> Execute -> Write Back",
    "The CPU must sequentially fetch the instruction word, decode its opcode, calculate effective addresses and fetch variables, perform arithmetic/logic, and write results back to memory/registers."
))

# Q3
elements.append(make_mcq_qa(
    "Q.3",
    "If a CPU register organization contains 16 general-purpose registers, how many selection control bits are required in the multiplexers to choose a source register?",
    [("A.", "2 bits"), ("B.", "3 bits"), ("C.", "4 bits"), ("D.", "16 bits")],
    "C. 4 bits",
    "To uniquely address $k$ candidate registers, we require $s$ selection lines where $s = \\lceil \\log_2 k \\rceil$. For 16 registers, $s = \\log_2 16 = 4$ selection bits."
))

# Q4
elements.append(make_mcq_qa(
    "Q.4",
    "Which addressing mode determines the effective address by adding a constant offset value to the current Program Counter (PC)?",
    [("A.", "Direct Addressing Mode"), ("B.", "Relative Addressing Mode"), ("C.", "Indexed Addressing Mode"), ("D.", "Register Indirect Mode")],
    "B. Relative Addressing Mode",
    "In Relative Addressing, the effective address is computed as: $EA = PC + \\text{Address Offset}$. This is widely used for localized jump and branch offsets."
))

# Q5
elements.append(make_mcq_qa(
    "Q.5",
    "What is the correct Register Transfer Language (RTL) code to load register R2 from the common bus, where register R1 is placing its data on the bus?",
    [("A.", "R2 <- R1"), ("B.", "BUS <- R1, R2 <- BUS"), ("C.", "R2 <- BUS, BUS <- R1"), ("D.", "R2 <- M[R1]")],
    "B. BUS <- R1, R2 <- BUS",
    "In bus-based transfers, the source register R1 must first be selected to drive its outputs onto the common bus (BUS <- R1), and the target register R2 must then load the data from the bus (R2 <- BUS)."
))

# Q6
elements.append(make_mcq_qa(
    "Q.6",
    "What is the 8-bit signed 2's complement binary representation of the decimal integer -12?",
    [("A.", "11110100"), ("B.", "00001100"), ("C.", "11110011"), ("D.", "10001100")],
    "A. 11110100",
    "Positive +12 is `00001100`. Invert all bits (1's complement) -> `11110011`. Add 1 to LSB -> `11110100` (-12)."
))

# Q7
elements.append(make_mcq_qa(
    "Q.7",
    "Why is Booth's multiplication algorithm faster than traditional shift-and-add algorithms when multiplying strings of consecutive 1s?",
    [("A.", "It performs shift operations in parallel"), ("B.", "It skips all shift operations"), ("C.", "It replaces consecutive additions with a single subtraction and addition"), ("D.", "It does not use an accumulator")],
    "C. It replaces consecutive additions with a single subtraction and addition",
    "Booth's recoding recognizes that a string of 1s (like `011110`) represents $2^5 - 2^1$, replacing four consecutive additions with one subtraction at the start of the string and one addition at the end."
))

# Q8
elements.append(make_mcq_qa(
    "Q.8",
    "How are the 32 bits allocated in the standard IEEE 754 Single-Precision floating-point format?",
    [("A.", "1 Sign, 8 Exponent, 23 Mantissa"), ("B.", "1 Sign, 11 Exponent, 20 Mantissa"), ("C.", "1 Sign, 15 Exponent, 16 Mantissa"), ("D.", "8 Sign, 8 Exponent, 16 Mantissa")],
    "A. 1 Sign, 8 Exponent, 23 Mantissa",
    "IEEE 754 single-precision allocates bit 31 for the sign, bits 30-23 (8 bits) for the biased exponent, and bits 22-0 (23 bits) for the fractional mantissa."
))

# Q9
elements.append(make_mcq_qa(
    "Q.9",
    "Which register in a microprogrammed control unit serves a similar purpose to the Program Counter (PC) in system memory?",
    [("A.", "Instruction Register (IR)"), ("B.", "Control Address Register (CAR)"), ("C.", "Control Data Register (SDR)"), ("D.", "Status Register")],
    "B. Control Address Register (CAR)",
    "Just as the PC tracks the next machine instruction address in main memory, the Control Address Register (CAR) tracks the next microinstruction address in Control Memory."
))

# Q10
elements.append(make_mcq_qa(
    "Q.10",
    "Which type of CPU control unit is systematically designed and easily modified by reprogramming internal control words?",
    [("A.", "Hardwired Control Unit"), ("B.", "Microprogrammed Control Unit"), ("C.", "Direct logic matrix unit"), ("D.", "Tri-state gate control unit")],
    "B. Microprogrammed Control Unit",
    "Since microprogrammed control units store control signals in a ROM array, modifying the instruction set simply requires rewriting control words, without physical rewiring."
))

# Q11
elements.append(make_mcq_qa(
    "Q.11",
    "Why do vertical microinstructions introduce extra hardware delays compared to horizontal formats?",
    [("A.", "They require more bits to transmit"), ("B.", "They must be read from slow primary RAM"), ("C.", "They must pass through external decoders to drive control lines"), ("D.", "They do not support branch sequencing")],
    "C. They must pass through external decoders to drive control lines",
    "Vertical microinstructions store encoded control fields. Before signals can drive hardware control lines, they must pass through decoder circuits, introducing gate propagation delays."
))

# Q12
elements.append(make_mcq_qa(
    "Q.12",
    "In Non-Restoring Binary Division, what is the next step if the partial remainder in register A is negative (MSB = 1) after a shift?",
    [("A.", "Shift left AQ, then subtract M"), ("B.", "Shift left AQ, then add M"), ("C.", "Restore A by adding M directly"), ("D.", "Terminate loop")],
    "B. Shift left AQ, then add M",
    "Non-restoring division avoids restoring additions. If A is negative, the next cycle shifts AQ left (multiplying by 2) and performs addition with M instead of subtraction."
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
q1_u1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Register Transfer Language (RTL)</b> is a formal symbolic notation used to describe the transfer of binary information between registers in a digital system.", answer_body_style),
    Paragraph("• <b>Memory Read Microoperation:</b> <b>`DR &larr; M[AR]`</b><br/>"
              "The Data Register (DR) loads the data word from the memory address specified by the Address Register (AR).", answer_bullet_style),
    Paragraph("• <b>Memory Write Microoperation:</b> <b>`M[AR] &larr; R1`</b><br/>"
              "Writes the contents of register R1 into the memory address specified by the AR.", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.1", "2.0", "Define Register Transfer Language (RTL). Write its symbol for memory read and memory write.", q1_u1_ans))

# Q2 Unit 1
q2_u1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Immediate Addressing Mode:</b> The operand is explicitly specified in the instruction itself, requiring no memory access.", answer_bullet_style),
    Paragraph("<i>Example:</i> `ADD 5` adds the integer constant 5 directly to the Accumulator.", answer_bullet_style),
    Paragraph("• <b>Implied Addressing Mode:</b> The operand is implicitly defined in the instruction opcode itself.", answer_bullet_style),
    Paragraph("<i>Example:</i> `CMA` (Complement Accumulator) implies the accumulator is the target, requiring no address bits.", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.2", "2.0", "Explain the difference between Immediate and Implied addressing modes with suitable examples.", q2_u1_ans))

# Q3 Unit 1
q3_u1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Fetch Phase:</b> The CPU retrieves the instruction word from the memory address specified by the Program Counter (PC) and loads it into the Instruction Register (IR).", answer_body_style),
    Paragraph("<b>T0: AR &larr; PC</b><br/>"
              "<b>T1: IR &larr; M[AR], PC &larr; PC + 1</b>", code_style),
    Paragraph("• <b>Decode Phase:</b> The Control Unit decodes the opcode bits in the IR and determines the addressing mode.", answer_body_style),
    Paragraph("<b>T2: Decoded Opcode, D_0 to D_7 active, Address Mode bit I extracted</b>", code_style),
]
elements.extend(make_coa_qa("Q.3", "2.0", "Describe the basic instruction cycle phases: Fetch and Decode with their RTL states.", q3_u1_ans))

# Section 2 Header
elements.append(Paragraph("<b>Section 2: Unit 2 (Computer Arithmetic &amp; Control Memory)</b>", answer_bold_style))
elements.append(Paragraph("<i>Instructions: Answer any <b>two</b> of the following three questions. Each question carries <b>2 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 4))

# Q4 Unit 2
t_headers = [Paragraph("<b>Comparison Parameter</b>", table_header_style), 
             Paragraph("<b>Horizontal Format</b>", table_header_style), 
             Paragraph("<b>Vertical Format</b>", table_header_style)]

t_row1 = [Paragraph("<b>Decoding Required</b>", table_text_style), Paragraph("<b>None:</b> Direct control signals.", table_text_style), Paragraph("<b>Yes:</b> Uses decoders.", table_text_style)]
t_row2 = [Paragraph("<b>Parallel Execution</b>", table_text_style), Paragraph("High (multi-signals simultaneously).", table_text_style), Paragraph("Low (only few active lines).", table_text_style)]
t_row3 = [Paragraph("<b>Word Width (Size)</b>", table_text_style), Paragraph("Very wide control words.", table_text_style), Paragraph("Narrow and compact words.", table_text_style)]

comp_table = Table([t_headers, t_row1, t_row2, t_row3], colWidths=[130, 190, 195])
comp_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
]))

q4_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The comparison of horizontal and vertical microinstruction formats is tabulated below:", answer_body_style),
    Spacer(1, 4),
    comp_table,
]
elements.extend(make_coa_qa("Q.4", "2.0", "Compare horizontal and vertical microinstruction formats in a table.", q4_u2_ans))

# Q5 Unit 2
q5_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In a microprogrammed control unit:", answer_body_style),
    Paragraph("• <b>Control Address Register (CAR):</b> Holds the address of the microinstruction currently being read from the Control Memory. It acts as the instruction pointer of the control unit, incremented or loaded by the sequencer.", answer_bullet_style),
    Paragraph("• <b>Control Data Register (SDR / Control Buffer):</b> Receives and holds the microinstruction control word read from the Control Memory ROM, driving the hardware control lines directly.", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.5", "2.0", "What is the Control Address Register (CAR) and Control Data Register (SDR)? Describe their roles.", q5_u2_ans))

# Q6 Unit 2
q6_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("An <b>array multiplier</b> is a digital hardware circuit used to multiply binary numbers in parallel, built using an array of AND gates and Full/Half Adders.", answer_body_style),
    Paragraph("<b>2-Bit by 2-Bit Array Multiplier Logic:</b>", answer_bold_style),
    Paragraph("Let multiplicand A = a<sub>1</sub>a<sub>0</sub> and multiplier B = b<sub>1</sub>b<sub>0</sub>. The product P = p<sub>3</sub>p<sub>2</sub>p<sub>1</sub>p<sub>0</sub> is computed as:", answer_body_style),
    Paragraph("                 a1      a0<br/>"
              "              &times;  b1      b0<br/>"
              "              --------------<br/>"
              "               a1b0    a0b0   &lt;--- Partial Product 1<br/>"
              "       a1b1    a0b1           &lt;--- Partial Product 2 (Shifted left)<br/>"
              "      ----------------------<br/>"
              "       P3      P2      P1      P0", code_style),
    Paragraph("• **p0** = a0b0 (Direct AND gate).<br/>"
              "• **p1** = a1b0 + a0b1 (Half Adder).<br/>"
              "• **p2, p3** = carry-out from p1 added to a1b1 (Half/Full Adder).", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.6", "2.0", "Define Array Multiplier. Draw the logical layout of a 2x2 binary multiplier.", q6_u2_ans))

elements.append(PageBreak())

# ==========================================
# 5. PART C BANNER
# ==========================================
elements.append(make_section_banner("PART C: LONG ANSWER & TRACING QUESTIONS (14 MARKS)"))

# Set 1 Header
elements.append(Paragraph("<b>Set 1: Unit 1 (Basic Structure of Computer)</b>", answer_bold_style))
elements.append(Paragraph("<i>Instructions: Answer any <b>one</b> of the following two questions (with internal choice). The question carries <b>7 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 4))

# Q7 [a] Instruction Formats
q7_set1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("An <b>Instruction Format</b> defines the layout of fields in an instruction word. We evaluate $X = (A + B) \times (C + D)$ in four different address structures:", answer_body_style),
    
    Paragraph("<b>1. Three-Address Instructions (Registers R1, R2):</b>", answer_bold_style),
    Paragraph("`ADD R1, A, B` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[R1 &larr; A + B]<br/>"
              "`ADD R2, C, D` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[R2 &larr; C + D]<br/>"
              "`MUL X, R1, R2` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[X &larr; R1 &times; R2]", code_style),
              
    Paragraph("<b>2. Two-Address Instructions:</b>", answer_bold_style),
    Paragraph("`MOV R1, A` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[R1 &larr; A]<br/>"
              "`ADD R1, B` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[R1 &larr; R1 + B]<br/>"
              "`MOV R2, C` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[R2 &larr; C]<br/>"
              "`ADD R2, D` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[R2 &larr; R2 + D]<br/>"
              "`MUL R1, R2` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[R1 &larr; R1 &times; R2]<br/>"
              "`MOV X, R1` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[X &larr; R1]", code_style),
              
    Paragraph("<b>3. One-Address (Accumulator-based) Instructions:</b>", answer_bold_style),
    Paragraph("`LOAD A` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AC &larr; A]<br/>"
              "`ADD B` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AC &larr; AC + B]<br/>"
              "`STORE T` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Temp T &larr; AC]<br/>"
              "`LOAD C` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AC &larr; C]<br/>"
              "`ADD D` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AC &larr; AC + D]<br/>"
              "`MUL T` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AC &larr; AC &times; T]<br/>"
              "`STORE X` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[X &larr; AC]", code_style),
              
    Paragraph("<b>4. Zero-Address (Stack-based) Instructions (TOS: Top of Stack):</b>", answer_bold_style),
    Paragraph("`PUSH A` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TOS &larr; A]<br/>"
              "`PUSH B` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TOS &larr; B]<br/>"
              "`ADD` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TOS &larr; A + B]<br/>"
              "`PUSH C` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TOS &larr; C]<br/>"
              "`PUSH D` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TOS &larr; D]<br/>"
              "`ADD` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TOS &larr; C + D]<br/>"
              "`MUL` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TOS &larr; (A+B) &times; (C+D)]<br/>"
              "`POP X` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[X &larr; TOS]", code_style),
]
elements.extend(make_coa_qa("Q.7 [a]", "7.0", "Explain Instruction Formats (Three-address, Two-address, One-address, Zero-address/stack-based) in detail, showing how the expression X = (A + B) * (C + D) is evaluated in each format.", q7_set1_ans))

elements.append(Paragraph("<b><font size='10' color='#0D9488'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;---------------------- OR ----------------------</font></b>", normal_style))
elements.append(Spacer(1, 4))

# Q7 [b] Fetch and Execution Cycle Flow
q7_set2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The <b>Instruction Cycle</b> represents the continuous operational loop of the CPU. Below is the comprehensive timing logic sequence and microoperations flow:", answer_body_style),
    
    Paragraph("<b>1. Flowchart Logic Sequence:</b>", answer_bold_style),
    Paragraph("               [ START CYCLE ]<br/>"
              "                      |<br/>"
              "                      v (Fetch Phase: T0, T1)<br/>"
              "               +--------------+<br/>"
              "               |  AR &larr; PC     |<br/>"
              "               |  IR &larr; M[AR]  |<br/>"
              "               |  PC &larr; PC + 1 |<br/>"
              "               +------+-------+<br/>"
              "                      |<br/>"
              "                      v (Decode Phase: T2)<br/>"
              "               +--------------+<br/>"
              "               | Decode Opcode|<br/>"
              "               | Extract Mode |<br/>"
              "               +------+-------+<br/>"
              "                      |<br/>"
              "                      v (Evaluate Addressing Mode: T3)<br/>"
              "             /&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\\<br/>"
              "        (If Indirect I=1)&nbsp;&nbsp;&nbsp;&nbsp;(If Direct I=0)<br/>"
              "             / &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\\<br/>"
              "      +------+------+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+------+------+<br/>"
              "      | AR &larr; M[AR]  | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;No Action &nbsp;|<br/>"
              "      +------+------+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+------+------+<br/>"
              "             \\ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/<br/>"
              "              \\ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/<br/>"
              "               v (Execution Phase: T4, T5, T6)<br/>"
              "         +-----------+-----------+<br/>"
              "         | Execute ALU Microcode |<br/>"
              "         | Write-back result     |<br/>"
              "         +-----------+-----------+<br/>"
              "                     |<br/>"
              "                     +---&gt; [ LOOP BACK TO FETCH next instruction ]", code_style),
    Spacer(1, 4),
    Paragraph("• <b>Fetch Cycle (T0, T1):</b> The target address is sent to memory, the instruction word is loaded into the IR, and the PC is incremented.", answer_bullet_style),
    Paragraph("• <b>Decode Cycle (T2):</b> Opcode is parsed, and the addressing bit $I$ is extracted.", answer_bullet_style),
    Paragraph("• <b>Effective Address (T3):</b> If $I=1$ (indirect), the CPU reads memory pointing to the actual operand address.", answer_bullet_style),
    Paragraph("• <b>Execution (T4+):</b> ALU logic generates control gates to perform calculation and writes back.", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.7 [b]", "7.0", "Discuss the Fetch and Execution Cycle in detail. Draw a comprehensive flowchart illustrating the entire instruction cycle (from fetch, decode, effective address calculation, to execution and loop back).", q7_set2_ans))

elements.append(PageBreak())

# Set 2 Header
elements.append(Paragraph("<b>Set 2: Unit 2 (Computer Arithmetic &amp; Control Memory)</b>", answer_bold_style))
elements.append(Paragraph("<i>Instructions: Answer any <b>one</b> of the following two questions (with internal choice). The question carries <b>7 marks</b>.</i>", normal_style))
elements.append(Spacer(1, 4))

# Q8 [a] Non-restoring binary division trace
n_headers = [Paragraph("<b>Step Description</b>", table_header_style), 
             Paragraph("<b>Accumulator (A)</b>", table_header_style), 
             Paragraph("<b>Multiplier (Q)</b>", table_header_style),
             Paragraph("<b>SC</b>", table_header_style)]

n_row1 = [Paragraph("Initial State (Dividend Q, Divisor M=0100, -M=1100)", table_text_style), Paragraph("0000", table_text_style), Paragraph("1011", table_text_style), Paragraph("4", table_text_style)]
n_row2 = [Paragraph("Step 1:<br/>1. Shift Left AQ<br/>2. Since A positive &rarr; Subtract M (A = A + (-M))<br/>3. Since A negative &rarr; Set Q<sub>0</sub> = 0", table_text_style), Paragraph("0001<br/>1101<br/>1101", table_text_style), Paragraph("011_<br/>011_<br/>0110", table_text_style), Paragraph("4<br/>-<br/>3", table_text_style)]
n_row3 = [Paragraph("Step 2:<br/>1. Shift Left AQ<br/>2. Since A negative &rarr; Add M (A = A + M)<br/>3. Since A negative &rarr; Set Q<sub>0</sub> = 0", table_text_style), Paragraph("1010<br/>1110<br/>1110", table_text_style), Paragraph("110_<br/>110_<br/>1100", table_text_style), Paragraph("3<br/>-<br/>2", table_text_style)]
n_row4 = [Paragraph("Step 3:<br/>1. Shift Left AQ<br/>2. Since A negative &rarr; Add M (A = A + M)<br/>3. Since A positive &rarr; Set Q<sub>0</sub> = 1", table_text_style), Paragraph("1101<br/>0001<br/>0001", table_text_style), Paragraph("100_<br/>100_<br/>1001", table_text_style), Paragraph("2<br/>-<br/>1", table_text_style)]
n_row5 = [Paragraph("Step 4:<br/>1. Shift Left AQ<br/>2. Since A positive &rarr; Subtract M (A = A - M)<br/>3. Since A negative &rarr; Set Q<sub>0</sub> = 0", table_text_style), Paragraph("0011<br/>1111<br/>1111", table_text_style), Paragraph("001_<br/>001_<br/>0010", table_text_style), Paragraph("1<br/>-<br/>0", table_text_style)]
n_row6 = [Paragraph("Correction Step (SC=0):<br/>Since final remainder A is negative &rarr; Add M to restore A", table_text_style), Paragraph("1111 + 0100 = <b>0011</b>", table_text_style), Paragraph("0010", table_text_style), Paragraph("0", table_text_style)]

n_table = Table([n_headers, n_row1, n_row2, n_row3, n_row4, n_row5, n_row6], colWidths=[235, 130, 110, 40])
n_table.setStyle(TableStyle([
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
    Paragraph("In <b>Non-Restoring Division</b>, we avoid restoring additions in every cycle, adding or subtracting divisor based on previous signs and adding a single correction step at the end if the remainder is negative.", answer_body_style),
    Paragraph("<b>Step-by-Step Tracing Table (11 / 4):</b>", answer_bold_style),
    Spacer(1, 4),
    n_table,
    Spacer(1, 6),
    Paragraph("<b>Final Division Outputs:</b>", answer_bold_style),
    Paragraph("• <b>Quotient (Q):</b> <b>`0010` (2 in decimal)</b>", answer_bullet_style),
    Paragraph("• <b>Remainder (A):</b> <b>`0011` (3 in decimal)</b>", answer_bullet_style),
    Paragraph("Since $11 = (4 &times; 2) + 3$, the binary division trace is mathematically correct!", answer_bold_style),
]
elements.extend(make_coa_qa("Q.8 [a]", "7.0", "Explain Non-Restoring Binary Division in detail. Trace step-by-step the division process to divide 11 by 4 (Dividend Q = 1011, Divisor M = 0100, size n = 4) in binary, showing A, Q, and SC.", q8_set1_ans))

elements.append(Paragraph("<b><font size='10' color='#0D9488'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;---------------------- OR ----------------------</font></b>", normal_style))
elements.append(Spacer(1, 4))

# Q8 [b] Microprogrammed Control Unit block diagram
q8_set2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A <b>Microprogrammed Control Unit</b> stores timing and control signals as control words inside an internal Read-Only Memory called Control Memory.", answer_body_style),
    Paragraph("<b>1. Microprogrammed Control Architecture Block Diagram:</b>", answer_bold_style),
    Paragraph("               External Opcode (IR)<br/>"
              "                       |<br/>"
              "                       v (Mapping Logic)<br/>"
              "           +------------------------+<br/>"
              "           | Control Address (CAR)  |<br/>"
              "           +-----------+------------+<br/>"
              "                       |<br/>"
              "                       v (Address input)<br/>"
              "           +-----------+------------+<br/>"
              "           |     <b>Control Memory</b>     |<br/>"
              "           |     <b>(Read-Only ROM)</b>    |<br/>"
              "           +-----------+------------+<br/>"
              "                       |<br/>"
              "                       v (Control Word fetched)<br/>"
              "           +-----------+------------+<br/>"
              "           |  <b>Control Buffer (SDR)</b> | &lt;-- Split fields<br/>"
              "           +-----+--------------+---+<br/>"
              "                 |              |<br/>"
              "                 v              v (Next address logic)<br/>"
              "          [Control Signals]   [Sequencer] -----&gt; (Feeds back into CAR)", code_style),
    Spacer(1, 4),
    Paragraph("<b>2. Key Functional Components:</b>", answer_bold_style),
    Paragraph("• <b>Control Memory (ROM):</b> Read-only memory storing all microprograms (control words) that execute machine instructions.", answer_bullet_style),
    Paragraph("• <b>Control Address Register (CAR):</b> Points to the address of the active microinstruction in Control Memory, similar to PC.", answer_bullet_style),
    Paragraph("• <b>Control Buffer Register (SDR):</b> Holds the fetched microinstruction word, separating the microoperation fields from the sequencing bits.", answer_bullet_style),
    Paragraph("• <b>Next-Address Sequencer:</b> Determines the next address to load into the CAR (CAR+1, branch address, or opcode map).", answer_bullet_style),
]
elements.extend(make_coa_qa("Q.8 [b]", "7.0", "Discuss Microprogrammed Control Unit Design. Draw a neat block diagram showing the interaction between the Control Address Register (CAR), Control Memory ROM, Control Buffer Register (SDR), and the Next-Address Generator (Sequencer), explaining each component's role.", q8_set2_ans))

# Build Document using NumberedCanvas for dynamic footer page counting
doc.build(elements, canvasmaker=NumberedCanvas)

print(f"COA Solved Model Exam Paper 2 PDF generated successfully: {pdf_path}")
