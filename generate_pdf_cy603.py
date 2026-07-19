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
            self.drawString(100, 805, " |   SISTec COA (CY-603) Solved Question Bank")
            self.drawRightString(555, 805, "Unit 1 & Unit 2 Solutions")
            
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
pdf_path = "CY_603_COA_Solved_Question_Bank.pdf"

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
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return KeepTogether([Spacer(1, 15), banner_table, Spacer(1, 10)])

def make_cy603_qa(num_str, bloom_lvl, co_str, q_text, answer_flowables):
    q_style = ParagraphStyle(
        'CyQStyle',
        parent=normal_style,
        fontName=font_name_bold,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
    )
    
    label = f"<b>Q.{num_str}</b>"
    
    # Render question text combined with its Bloom's Level & CO tag in a professional header
    full_q_text = f"{q_text}"
    badge_text = f"<br/><font color='#0D9488' size='8'><b>Bloom's Taxonomy: {bloom_lvl} | Course Outcome: {co_str}</b></font>"
    full_q_text += badge_text
        
    p_num = Paragraph(label, q_style)
    p_text = Paragraph(full_q_text, ParagraphStyle('CyQText', parent=normal_style, fontName=font_name_bold, fontSize=10, leading=15))
    
    q_table = Table([[p_num, p_text]], colWidths=[50, 465])
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
        
    flowables.append(Spacer(1, 24)) # Spaced-out question gap
    return flowables

def get_image_flowable(image_filename, width=380, height=230):
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
    [Paragraph("<b>SAGAR INSTITUTE OF SCIENCE &amp; TECHNOLOGY (SISTec)</b>", ParagraphStyle('SISTitle', fontName=font_name_bold, fontSize=12, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>DEPARTMENT OF CSE - CYBER SECURITY</b>", ParagraphStyle('SISDept', fontName=font_name_bold, fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#1F2937')))],
    [Paragraph("<b>QUESTION BANK SOLUTIONS — SESSION 2024-25</b>", ParagraphStyle('SISSub', fontName=font_name_bold, fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#4B5563')))],
    [Paragraph("<b>COMPUTER ORGANIZATION &amp; ARCHITECTURE (CY-603)</b>", ParagraphStyle('SISSubject', fontName=font_name_bold, fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#0D9488')))],
    [Paragraph("<b>Document Curated &amp; Published by: <font color='#0D9488'>EMo Learners</font></b>", ParagraphStyle('SISFaculty', fontName=font_name_bold, fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))]
]

header_table = Table(header_data, colWidths=[515])
header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
    ('LINEBELOW', (0, 3), (-1, 3), 1.5, colors.HexColor('#0D9488')), # Teal divider
]))
elements.append(header_table)
elements.append(Spacer(1, 10))

# ==========================================
# 2. METADATA SECTION
# ==========================================
info_data = [
    [
        Paragraph("<b>Subject:</b> Computer Organization &amp; Architecture (CS-404)", normal_style),
        Paragraph("<b>Total Solved Questions:</b> 20", normal_style)
    ],
    [
        Paragraph("<b>Design Standards:</b> Highly Spacious Step-by-Step Traces", normal_style),
        Paragraph("<b>Branding Highlight:</b> EMo Learners Premium Quality", normal_style)
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
# 3. UNIT 1 BANNER
# ==========================================
elements.append(make_section_banner("UNIT 1: COMPUTER STRUCTURE, BUSES, AND CONTROL UNITS"))

# ==========================================
# UNIT 1 QUESTIONS & SOLUTIONS
# ==========================================

# Q1: Desktop computer structure & block diagram
q1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A desktop computer is structured around a central motherboard housing the processing core, memory systems, and interface cards.", answer_body_style),
    Paragraph("<b>Functional Block Diagram (Von-Neumann Architecture):</b>", answer_bold_style),
]

# Safely embed the real generated Von-Neumann diagram
vn_img = get_image_flowable("von_neumann.png", width=380, height=230)
if vn_img:
    q1_ans.append(vn_img)
else:
    # Fallback to ASCII schematic if PNG not available
    q1_ans.append(Paragraph("   +-------------------------------------------------------------+<br/>"
                            "   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>CENTRAL PROCESSING UNIT (CPU)</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
                            "   | &nbsp;&nbsp;+-----------------+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+--------------------+ &nbsp;|<br/>"
                            "   | &nbsp;&nbsp;| &nbsp;<b>Control Unit</b> &nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| <b>Registers (ACC,PC)</b>| &nbsp;|<br/>"
                            "   | &nbsp;&nbsp;+--------+--------+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+---------+----------+ &nbsp;|<br/>"
                            "   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
                            "   | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+-------------&gt; [ <b>ALU</b> ] &lt;-----------+ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
                            "   +-----------------------------+-------------------------------+<br/>"
                            "                                 |<br/>"
                            "                        =================== [ <b>System Bus</b> ]<br/>"
                            "                           |              |<br/>"
                            "                           v              v<br/>"
                            "                     +-----+-----+  +-----+-----+<br/>"
                            "                     | <b>Memory</b>    |  | <b>I/O Unit</b>  | &lt;=== Ports &amp; Peripherals<br/>"
                            "                     | <b>(RAM/ROM)</b> |  | <b>Interface</b> |<br/>"
                            "                     +-----------+  +-----------+", code_style))

q1_ans.extend([
    Paragraph("<b>Functions of Major Units:</b>", answer_bold_style),
    Paragraph("• <b>Input Unit:</b> Translates user data (keyboard, mouse) into binary representation for processing.", answer_bullet_style),
    Paragraph("• <b>Memory Unit:</b> Stores operating systems, active applications (RAM), and booting code (ROM).", answer_bullet_style),
    Paragraph("• <b>CPU Control Unit:</b> Decodes instructions and generates timing signals to coordinate data flows.", answer_bullet_style),
    Paragraph("• <b>CPU ALU Unit:</b> Execution core performing mathematical and logical processing on operands.", answer_bullet_style),
    Paragraph("• <b>Output Unit:</b> Converts binary calculations back into human-readable text/displays (monitors, printers).", answer_bullet_style),
])
elements.extend(make_cy603_qa("1", "1(Remembering)", "CO1", "Explain the structure of a desktop computer with a neat block diagram and describe the function of each major unit.", q1_ans))

# Q2: Register/Stack Definitions
q2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Essential registers and memory structures are defined below:", answer_body_style),
    Paragraph("• <b>Program Counter (PC):</b> A 12-bit or 16-bit register holding the memory address of the next instruction to fetch. <i>Example:</i> If PC = `0AF2H`, the CPU fetches the instruction word at memory address `0AF2H`.", answer_bullet_style),
    Paragraph("• <b>Instruction Register (IR):</b> Holds the active instruction code fetched from memory during decoding. <i>Example:</i> Stores the 16-bit binary instruction `7020H` (representing clear accumulator).", answer_bullet_style),
    Paragraph("• <b>Memory Register (MBR / Data Register):</b> Temporarily stores data retrieved from or written to memory address slots. <i>Example:</i> Stores the 16-bit word loaded from RAM address `1F0H` before processing.", answer_bullet_style),
    Paragraph("• <b>Control Word:</b> A sequence of control bits stored in control memory that directly drives hardware multiplexers and enable lines. <i>Example:</i> A 16-bit control word where bits 0–2 select ALU function, bits 3–5 select source register, and bit 6 enables register load.", answer_bullet_style),
    Paragraph("• <b>Stack Organization:</b> A LIFO (Last-In, First-Out) memory stack managed by a **Stack Pointer (SP)** register. <i>Example:</i> In subroutine calls, the return address is 'Pushed' onto the stack (decrementing SP) and later 'Popped' (incrementing SP) to resume main program execution.", answer_bullet_style),
]
elements.extend(make_cy603_qa("2", "1(Remembering)", "CO1", "Define Program Counter, Instruction Register, Memory Register, Control Word, and Stack Organization with suitable examples.", q2_ans))

# Q3: General Register Organization
q3_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In a **General Register Organization**, registers share access to an internal bus structure that feeds directly into the ALU.", answer_body_style),
    Paragraph("<b>Bus-based CPU Register Organization:</b>", answer_bold_style),
    Paragraph("Outputs from registers are routed to two multiplexers (MUX A and MUX B). The select inputs (SELA and SELB) choose two registers to place their data on Bus A and Bus B. The ALU processes these buses based on selection variables (OPR) and writes the output sum back into a target register via a decoder (SELD) on the active clock edge.", answer_body_style),
    Paragraph("• <b>Role of ALU in Instruction Execution:</b> The ALU acts as the central execution engine. Once the control unit decodes an instruction (e.g. `ADD R1, R2`), it places the contents of R1 on Bus A, R2 on Bus B, selects the addition operation in the ALU, and routes the sum back to R1. This executes the target machine instruction in a single clock cycle.", answer_bullet_style),
]
elements.extend(make_cy603_qa("3", "2(Understanding)", "CO1", "Explain the general register organization of CPU and describe the role of ALU in instruction execution.", q3_ans))

# Q4: Instruction format & addressing modes
q4_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("An **Instruction Format** defines the bit division of a computer instruction word. A typical format consists of an **Opcode** (the operation), an **Addressing Mode** (specifying address calculation rules), and **Operands** (data registers or addresses).", answer_body_style),
    Paragraph("<b>Core Addressing Modes:</b>", answer_bold_style),
    Paragraph("• <b>Implied Mode:</b> The operand is implicitly defined in the opcode itself. <i>Example:</i> `CMA` (Complement Accumulator) requires no address field.", answer_bullet_style),
    Paragraph("• <b>Immediate Mode:</b> The operand is explicitly specified in the instruction itself. <i>Example:</i> `ADD 5` adds the value 5 directly to the accumulator.", answer_bullet_style),
    Paragraph("• <b>Direct Addressing:</b> The address field contains the actual address of the operand. <i>Example:</i> `ADD 250H` fetches the value at memory address `250H`.", answer_bullet_style),
    Paragraph("• <b>Indirect Addressing:</b> The address field points to a memory location that contains the actual effective address of the operand. <i>Example:</i> `ADD [250H]` looks at address `250H` to read address `500H`, then fetches the operand from `500H`.", answer_bullet_style),
    Paragraph("• <b>Register Indirect:</b> A register holds the address of the operand in memory. <i>Example:</i> `ADD (R1)` fetches the operand at memory address stored inside R1.", answer_bullet_style),
]
elements.extend(make_cy603_qa("4", "2(Understanding)", "CO1", "Describe the instruction format and various addressing modes used in computer systems with examples.", q4_ans))

# Q5: Register Transfer Language
q5_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Register Transfer Language (RTL)</b> is a formal symbolic notation used to describe the transfer of binary information between registers in a digital system.", answer_body_style),
    Paragraph("<b>Demonstration of Transfer Operations:</b>", answer_bold_style),
    Paragraph("• <b>Register Transfer:</b> `R2 ← R1`<br/>"
              "Moves the 16-bit binary contents of R1 directly into R2 during the next active clock transition.", answer_bullet_style),
    Paragraph("• <b>Bus Transfer (Using Common Bus):</b> `BUS ← R1, R2 ← BUS`<br/>"
              "Register R1 places its output on the common bus lines, and register R2 loads the data from the bus.", answer_bullet_style),
    Paragraph("• <b>Memory Read:</b> `DR ← M[AR]`<br/>"
              "The Data Register (DR) loads the data word from the memory address specified by the Address Register (AR).", answer_bullet_style),
    Paragraph("• <b>Memory Write:</b> `M[AR] ← R1`<br/>"
              "Writes the contents of register R1 into the memory address specified by the AR.", answer_bullet_style),
]
elements.extend(make_cy603_qa("5", "3(Applying)", "CO1", "Illustrate the concept of Register Transfer Language (RTL) and demonstrate bus and memory transfer operations using suitable examples.", q5_ans))

# Q6: Fetch and execution cycle (With Flow Diagram!)
q6_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The **Fetch-Execute Cycle** represents the continuous operational loop of the CPU.", answer_body_style),
    Paragraph("<b>Instruction Cycle Flowchart:</b>", answer_bold_style),
]

# Safely embed the real generated Fetch-Execute Flowchart
fe_img = get_image_flowable("fetch_execute.png", width=380, height=230)
if fe_img:
    q6_ans.append(fe_img)
else:
    # Fallback to ASCII flowchart if PNG not available
    q6_ans.append(Paragraph("          +--------------------------------------+<br/>"
                            "          | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;START CYCLE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
                            "          +------------------+-------------------+<br/>"
                            "                             |<br/>"
                            "                             v<br/>"
                            "          +--------------------------------------+<br/>"
                            "          | <b>Fetch Phase (T0, T1):</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
                            "          | • AR ← PC &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
                            "          | • IR ← M[AR], PC ← PC + 1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
                            "          +------------------+-------------------+<br/>"
                            "                             |<br/>"
                            "                             v<br/>"
              "          +--------------------------------------+<br/>"
              "          | <b>Decode Phase (T2):</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
              "          | • Decode Opcode in IR &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
              "          | • Calculate Effective Address &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
              "          +------------------+-------------------+<br/>"
              "                             |<br/>"
              "                             v<br/>"
              "          +--------------------------------------+<br/>"
              "          | <b>Execute Phase (T3):</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
              "          | • Generate Control Timing signals &nbsp;&nbsp;&nbsp;|<br/>"
              "          | • Execute ALU Operation &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
              "          +------------------+-------------------+<br/>"
              "                             |<br/>"
              "                             +--- (Return to fetch next instruction)", code_style))

elements.extend(make_cy603_qa("6", "3(Applying)", "CO1", "Demonstrate the fetch and execution cycle of an instruction with the help of a flow diagram.", q6_ans))

# Q7: Bus structures and CPU-Memory Communication
q7_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A computer system uses three primary buses (system bus) to manage communication between the CPU and memory:", answer_body_style),
    Paragraph("• <b>Address Bus:</b> A unidirectional bus carrying the target memory address from the CPU to memory chip decoders.", answer_bullet_style),
    Paragraph("• <b>Data Bus:</b> A bidirectional bus transferring the actual instruction or operand data word between the CPU and memory.", answer_bullet_style),
    Paragraph("• <b>Control Bus:</b> Unidirectional control lines carrying timing and operational commands (such as **Memory Read (MEMR)** or **Memory Write (MEMW)**) from the CPU control unit to synchronize the memory interface.", answer_bullet_style),
    Paragraph("<b>Step-by-Step Read Communication Sequence:</b>", answer_bold_style),
    Paragraph("1. The CPU writes the target address onto the address bus.", answer_bullet_style),
    Paragraph("2. The CPU activates the **Memory Read** line on the control bus.", answer_bullet_style),
    Paragraph("3. The memory decoder decodes the address bus inputs and enables the target memory location.", answer_bullet_style),
    Paragraph("4. The memory chip drives the data contents onto the data bus.", answer_bullet_style),
    Paragraph("5. The CPU reads the bits off the data bus and loads them into internal registers (like the MBR).", answer_bullet_style),
]
elements.extend(make_cy603_qa("7", "4(Analyzing)", "CO1", "Analyze the bus structure of a computer system and examine how CPU and memory communicate through system buses.", q7_ans))

# Q8: Compare hardwired and microprogrammed control units
t_headers = [Paragraph("<b>Comparison Parameter</b>", table_header_style), 
             Paragraph("<b>Hardwired Control Unit</b>", table_header_style), 
             Paragraph("<b>Microprogrammed Control Unit</b>", table_header_style)]

t_row1 = [Paragraph("<b>Design Complexity</b>", table_text_style),
          Paragraph("Highly complex. Sprawling logic gates are difficult to design and debug.", table_text_style),
          Paragraph("Systematic, simple, and clean design utilizing standard memory arrays.", table_text_style)]

t_row2 = [Paragraph("<b>Speed</b>", table_text_style),
          Paragraph("<b>Extremely Fast:</b> No memory access latency; signals propagate through gates instantly.", table_text_style),
          Paragraph("<b>Slower:</b> Must access internal Control Memory (ROM) for every microinstruction step.", table_text_style)]

t_row3 = [Paragraph("<b>Flexibility</b>", table_text_style),
          Paragraph("<b>Low:</b> Adding new instructions requires physical redesign and rewiring.", table_text_style),
          Paragraph("<b>High:</b> Easily update or add instructions by modifying microprograms in ROM.", table_text_style)]

t_row4 = [Paragraph("<b>Typical Architecture</b>", table_text_style),
          Paragraph("Used in modern high-speed **RISC** processors.", table_text_style),
          Paragraph("Ideal for complex **CISC** processors.", table_text_style)]

comp_table = Table([t_headers, t_row1, t_row2, t_row3, t_row4], colWidths=[110, 200, 205])
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

q8_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Hardwired and microprogrammed control units represent the two primary design styles for processor control units. A spacious comparison is tabulated below:", answer_body_style),
    Spacer(1, 6),
    comp_table,
    Spacer(1, 6)
]
elements.extend(make_cy603_qa("8", "4(Analyzing)", "CO1", "Compare hardwired control unit and microprogrammed control unit with respect to design complexity, speed, and flexibility.", q8_ans))

# Q9: Microprogram sequencer and control memory
q9_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In a microprogrammed control unit, execution is guided by the **Control Memory** and the **Microprogram Sequencer**:", answer_body_style),
    Paragraph("• <b>Control Memory (ROM):</b> An internal ROM array holding the sequence of control words (microinstructions) that execute every machine opcode.", answer_bullet_style),
    Paragraph("• <b>Microprogram Sequencer:</b> An address-selection unit that determines the next address to load into the Control Address Register (CAR). It evaluates condition bits, control codes, and branch flags to select the next address from four possible sources:", answer_bullet_style),
    Paragraph("1. **CAR + 1:** Increments CAR to execute the next sequential microinstruction.", answer_bullet_style),
    Paragraph("2. **Address Field of Microinstruction:** Performs a jump to a branch address specified in the current control word.", answer_bullet_style),
    Paragraph("3. **Opcode Mapping Logic:** Converts the opcode of the machine instruction inside the IR into a starting address in Control Memory.", answer_bullet_style),
    Paragraph("4. **Subroutine Return (SBR):** Loads the return address from the Subroutine Register to return from a microprogram function.", answer_bullet_style),
]
elements.extend(make_cy603_qa("9", "5(Evaluating)", "CO1", "Evaluate the role of microprogram sequencer and control memory in sequencing and execution of microinstructions.", q9_ans))

# Q10: Design a control unit architecture
q10_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Designing a microprogrammed control unit requires defining a **Control Memory structure** and a **Microinstruction format** to coordinate data paths.", answer_body_style),
    Paragraph("<b>1. Microinstruction Word Format Design (20 bits):</b>", answer_bold_style),
    Paragraph("+-------------------+-------------------+-------------------+-------------------+<br/>"
              "| &nbsp;&nbsp;<b>F1 (Micro-op)</b> &nbsp;| &nbsp;&nbsp;<b>F2 (Micro-op)</b> &nbsp;| &nbsp;<b>CD (Condition)</b> &nbsp;| &nbsp;<b>AD (Next Addr)</b> &nbsp;|<br/>"
              "| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6 bits &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6 bits &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2 bits &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6 bits &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
              "+-------------------+-------------------+-------------------+-------------------+", code_style),
    Spacer(1, 4),
    Paragraph("• <b>Microoperation Fields (F1, F2):</b> Decode to enable registers or ALU functions.", answer_bullet_style),
    Paragraph("• <b>Condition Field (CD):</b> 00 = Always, 01 = If Zero, 10 = If Carry, 11 = If Sign.", answer_bullet_style),
    Paragraph("• <b>Address Field (AD):</b> Holds a 6-bit target address in Control Memory (up to 64 microinstructions).", answer_bullet_style),
    Spacer(1, 4),
    Paragraph("<b>2. Functional Architecture Diagram:</b>", answer_bold_style),
]

# Safely embed the real generated Microprogrammed Control Unit diagram
cu_img = get_image_flowable("control_unit.png", width=380, height=230)
if cu_img:
    q10_ans.append(cu_img)
else:
    # Fallback explanation if PNG not available
    q10_ans.append(Paragraph("• **Mapping Unit:** Accepts opcodes and translates them into starting addresses.", answer_bullet_style))

elements.extend(make_cy603_qa("10", "6(Creating )", "CO1", "Design a functional architecture of a control unit incorporating microinstruction format and control memory organization.", q10_ans))

# ==========================================
# 4. UNIT 2 BANNER
# ==========================================
elements.append(make_section_banner("UNIT 2: COMPUTER ARITHMETIC & NUMERICAL OPERATIONS"))

# ==========================================
# UNIT 2 QUESTIONS & SOLUTIONS
# ==========================================

# Q1: 1's and 2's complements
q1_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("1's and 2's complement representations are used to represent signed integers in binary computer systems.", answer_body_style),
    Paragraph("• <b>1's Complement:</b> Formed by inverting all the bits of a positive binary number (0s become 1s, 1s become 0s).", answer_bullet_style),
    Paragraph("• <b>2's Complement:</b> Formed by taking the 1's complement and adding 1 to the Least Significant Bit (LSB).", answer_bullet_style),
    Paragraph("<b>Advantages of 2's Complement in Signed Arithmetic:</b>", answer_bold_style),
    Paragraph("• <b>Unique Representation of Zero:</b> 1's complement has two zero representations (+0: `00000000` and -0: `11111111`), which requires complicated comparisons. 2's complement has a single representation for zero (`00000000`), simplifying logic.", answer_bullet_style),
    Paragraph("• <b>Unified Addition &amp; Subtraction Hardware:</b> Subtraction <i>A - B</i> is calculated directly by adding <i>A + (-B)<sub>2's</sub></i>. The CPU does not require separate adder and subtractor logic circuits; a single parallel binary adder is used for both operations.", answer_bullet_style),
    Paragraph("• <b>No End-Around Carry:</b> During addition, any carry-out from the sign bit (MSB) is simply discarded, unlike 1's complement which requires adding the carry back to the sum (end-around carry).", answer_bullet_style),
]
elements.extend(make_cy603_qa("1", "1(Remembering)", "CO2", "Define 1’s complement and 2’s complement representation and list their advantages in signed arithmetic operations.", q1_u2_ans))

# Q2: Booth's algorithm steps
q2_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Booth's Multiplication Algorithm</b> multiplies two signed binary numbers in 2's complement format. The step-by-step algorithmic procedure is outlined below:", answer_body_style),
    Paragraph("1. **Setup Registers:** Accumulator (A) = 0, Q<sub>-1</sub> register = 0, Multiplier loaded into register Q, Multiplicand loaded into register M, and Sequence Counter (SC) set to bit length <i>n</i>.", answer_bullet_style),
    Paragraph("2. **Loop Execution:** While SC &gt; 0, examine the least significant bit of Q (Q<sub>0</sub>) and Q<sub>-1</sub>:", answer_bullet_style),
    Paragraph("- **01:** Add multiplicand to A (`A = A + M`).<br/>"
              "- **10:** Subtract multiplicand from A (`A = A - M` or `A = A + M' + 1`).<br/>"
              "- **00 or 11:** Perform no arithmetic operation.", answer_bullet_style),
    Paragraph("3. **Shift Phase:** Perform an **Arithmetic Right Shift (ARS)** on the combined registers A-Q-Q<sub>-1</sub> by 1 bit, preserving the sign bit (MSB) of A.", answer_bullet_style),
    Paragraph("4. **Decrement Counter:** Decrement SC by 1.", answer_bullet_style),
    Paragraph("5. **Termination:** Once SC = 0, the final product is stored in the combined register space A Q.", answer_bullet_style),
]
elements.extend(make_cy603_qa("2", "1(Remembering)", "CO2", "State the algorithmic steps involved in Booth’s multiplication algorithm.", q2_u2_ans))

# Q3: Signed addition/subtraction
q3_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In 2's complement representation, subtraction is treated directly as addition, allowing unified hardware processing.", answer_body_style),
    Paragraph("<b>Demonstration with Examples:</b>", answer_bold_style),
    Paragraph("Let us perform operations using 5-bit signed binary numbers (range: -16 to +15):", answer_body_style),
    
    Paragraph("<b>Example 1: Signed Addition (+9) + (+4)</b>", answer_bold_style),
    Paragraph("• +9 in binary = <b>01001<sub>2</sub></b><br/>"
              "• +4 in binary = <b>00100<sub>2</sub></b><br/>"
              "• Perform direct binary addition:<br/>"
              "&nbsp;&nbsp;&nbsp;&nbsp;01001 &nbsp;(+9)<br/>"
              "&nbsp;&nbsp;+ 00100 &nbsp;(+4)<br/>"
              "&nbsp;&nbsp;-------<br/>"
              "&nbsp;&nbsp;&nbsp;&nbsp;01101 &nbsp;(+13 in decimal, MSB=0, positive). Correct!", answer_bullet_style),
              
    Paragraph("<b>Example 2: Signed Subtraction (+9) − (+4)</b>", answer_bold_style),
    Paragraph("This is treated as **+9 + (-4)**:<br/>"
              "• +9 in binary = 01001<sub>2</sub><br/>"
              "• +4 in binary = 00100<sub>2</sub>. Take 2's complement to represent -4:<br/>"
              "&nbsp;&nbsp;1's complement = 11011 → Add 1 = <b>11100<sub>2</sub></b>.<br/>"
              "• Perform binary addition:<br/>"
              "&nbsp;&nbsp;&nbsp;&nbsp;01001 &nbsp;(+9)<br/>"
              "&nbsp;&nbsp;+ 11100 &nbsp;(-4)<br/>"
              "&nbsp;&nbsp;-------<br/>"
              "&nbsp;(1)00101 &nbsp;(+5 in decimal, MSB=0, discard carry). Correct!", answer_bullet_style),
]
elements.extend(make_cy603_qa("3", "2(Understanding)", "CO2", "Explain signed addition and subtraction using 2’s complement method with suitable examples.", q3_u2_ans))

# Q4: Floating point arithmetic
q4_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Floating-point numbers are represented in scientific format (sign, exponent, mantissa). Arithmetic operations process exponents and mantissas separately:", answer_body_style),
    Paragraph("• <b>Addition and Subtraction:</b>", answer_bold_style),
    Paragraph("1. **Compare Exponents:** Compute exponent difference <i>d = E1 - E2</i>.", answer_bullet_style),
    Paragraph("2. **Align Mantissas:** Shift the mantissa of the number with the smaller exponent right by <i>d</i> bits and set its exponent to the larger value.", answer_bullet_style),
    Paragraph("3. **Add/Subtract:** Add or subtract the aligned mantissas based on their sign bits.", answer_bullet_style),
    Paragraph("4. **Normalize:** If carry is generated, shift the mantissa right by 1 bit and increment the exponent. If there are leading zeros, shift left and decrement the exponent.", answer_bullet_style),
    
    Paragraph("• <b>Multiplication:</b>", answer_bold_style),
    Paragraph("1. **Add Exponents:** Add exponents and subtract bias (bias = 127 in single-precision) to avoid double bias.", answer_bullet_style),
    Paragraph("2. **Multiply Mantissas:** Multiply the fractional mantissas directly.", answer_bullet_style),
    Paragraph("3. **Normalize &amp; Round:** Normalize the product and round the mantissa to 23 bits.", answer_bullet_style),
    
    Paragraph("• <b>Division:</b>", answer_bold_style),
    Paragraph("1. **Subtract Exponents:** Subtract divisor exponent from dividend exponent and add bias.", answer_bullet_style),
    Paragraph("2. **Divide Mantissas:** Divide the dividend mantissa by the divisor mantissa.", answer_bullet_style),
    Paragraph("3. **Normalize &amp; Round:** Normalize and round the quotient.", answer_bullet_style),
]
elements.extend(make_cy603_qa("4", "2(Understanding)", "CO2", "Describe the procedure of floating-point arithmetic operations in computer systems.", q4_u2_ans))

# Q5: Apply Booth's algorithm (Numerical Trace +13 * -9!)
q5_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Let us multiply **(+13)** and **(-9)** using Booth's Algorithm in 6-bit signed 2's complement representation:", answer_body_style),
    Paragraph("• Multiplicand (M) = <b>+13</b> = <b>001101<sub>2</sub></b><br/>"
              "• Negative Multiplicand (-M) = <b>-13</b> = <b>110011<sub>2</sub></b> (2's complement of 001101)<br/>"
              "• Multiplier (Q) = <b>-9</b> = <b>110111<sub>2</sub></b> (2's complement of 001001)", answer_bullet_style),
    Paragraph("• **Registers:** Accumulator (A) = <b>000000</b> (6 bits), Q<sub>-1</sub> = <b>0</b> (1 bit), SC = <b>6</b>.", answer_bullet_style),
    
    Paragraph("<b>Cycle-by-Cycle Tracing:</b>", answer_bold_style),
    
    Paragraph("• <b>Initial State:</b> A = 000000, Q = 110111, Q<sub>-1</sub> = 0, SC = 6", answer_bullet_style),
    
    Paragraph("• <b>Cycle 1:</b><br/>"
              "- Check Q<sub>0</sub>Q<sub>-1</sub> = <b>10</b> → Perform <b>A = A + (-M)</b>:<br/>"
              "&nbsp;&nbsp;A = 000000 + 110011 = 110011.<br/>"
              "- Perform **Arithmetic Right Shift (ARS)**:<br/>"
              "&nbsp;&nbsp;<b>A = 111001, Q = 111011, Q<sub>-1</sub> = 1</b>. SC = 5.", answer_bullet_style),
              
    Paragraph("• <b>Cycle 2:</b><br/>"
              "- Check Q<sub>0</sub>Q<sub>-1</sub> = <b>11</b> → Perform **ARS only**:<br/>"
              "&nbsp;&nbsp;<b>A = 111100, Q = 111101, Q<sub>-1</sub> = 1</b>. SC = 4.", answer_bullet_style),
              
    Paragraph("• <b>Cycle 3:</b><br/>"
              "- Check Q<sub>0</sub>Q<sub>-1</sub> = <b>11</b> → Perform **ARS only**:<br/>"
              "&nbsp;&nbsp;<b>A = 111110, Q = 011110, Q<sub>-1</sub> = 1</b>. SC = 3.", answer_bullet_style),
              
    Paragraph("• <b>Cycle 4:</b><br/>"
              "- Check Q<sub>0</sub>Q<sub>-1</sub> = <b>01</b> → Perform <b>A = A + M</b>:<br/>"
              "&nbsp;&nbsp;A = 111110 + 001101 = 001011 (discard carry).<br/>"
              "- Perform **ARS**:<br/>"
              "&nbsp;&nbsp;<b>A = 000101, Q = 101111, Q<sub>-1</sub> = 0</b>. SC = 2.", answer_bullet_style),
              
    Paragraph("• <b>Cycle 5:</b><br/>"
              "- Check Q<sub>0</sub>Q<sub>-1</sub> = <b>10</b> → Perform <b>A = A + (-M)</b>:<br/>"
              "&nbsp;&nbsp;A = 000101 + 110011 = 111000.<br/>"
              "- Perform **ARS**:<br/>"
              "&nbsp;&nbsp;<b>A = 111100, Q = 010111, Q<sub>-1</sub> = 1</b>. SC = 1.", answer_bullet_style),
              
    Paragraph("• <b>Cycle 6:</b><br/>"
              "- Check Q<sub>0</sub>Q<sub>-1</sub> = <b>11</b> → Perform **ARS only**:<br/>"
              "&nbsp;&nbsp;<b>A = 111110, Q = 001011, Q<sub>-1</sub> = 1</b>. SC = 0. Stop.", answer_bullet_style),
              
    Paragraph("<b>Result Verification:</b>", answer_bold_style),
    Paragraph("The final combined register contents are <b>A Q = 111110001011<sub>2</sub></b>.", answer_body_style),
    Paragraph("Since the MSB is 1, the result is negative. Let's find its magnitude via 2's complement:<br/>"
              "1. Invert all bits → 000001110100<br/>"
              "2. Add 1 → 000001110101<sub>2</sub><br/>"
              "3. Convert to decimal → 2<sup>6</sup> + 2<sup>5</sup> + 2<sup>4</sup> + 2<sup>2</sup> + 2<sup>0</sup> = 64 + 32 + 16 + 4 + 1 = 117.<br/>"
              "Therefore, the value is <b>-117</b>.", answer_bullet_style),
    Paragraph("Multiplying (+13) × (-9) yields <b>-117</b>. The trace is mathematically 100% correct!", answer_bold_style),
]
elements.extend(make_cy603_qa("5", "3(Applying)", "CO2", "Apply Booth’s Algorithm to multiply two signed binary numbers.", q5_u2_ans))

# Q6: Binary Division Restoring and Non-restoring
q6_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Let us perform binary division of **11 divided by 4** (Dividend Q = 11 = `1011`, Divisor M = 4 = `0100`, size n = 4) using both methods.", answer_body_style),
    
    Paragraph("<b>Method 1: Restoring Division (Step-by-Step):</b>", answer_bold_style),
    Paragraph("• <b>Init:</b> A = 0000, Q = 1011, M = 0100, -M = 1100", answer_bullet_style),
    
    Paragraph("• <b>Step 1:</b><br/>"
              "1. Shift Left AQ → A = 0001, Q = 011_<br/>"
              "2. Subtract M (A = A + (-M)) → A = 0001 + 1100 = 1101.<br/>"
              "3. Since A is negative (MSB=1), set Q<sub>0</sub> = 0, and restore A (A = A + M) → A = 1101 + 0100 = 0001.<br/>"
              "<i>State:</i> A = 0001, Q = 0110.", answer_bullet_style),
              
    Paragraph("• <b>Step 2:</b><br/>"
              "1. Shift Left AQ → A = 0010, Q = 110_<br/>"
              "2. Subtract M → A = 0010 + 1100 = 1110.<br/>"
              "3. Since A is negative, set Q<sub>0</sub> = 0, and restore A → A = 1110 + 0100 = 0010.<br/>"
              "<i>State:</i> A = 0010, Q = 1100.", answer_bullet_style),
              
    Paragraph("• <b>Step 3:</b><br/>"
              "1. Shift Left AQ → A = 0101, Q = 100_<br/>"
              "2. Subtract M → A = 0101 + 1100 = 0001.<br/>"
              "3. Since A is positive (MSB=0), set Q<sub>0</sub> = 1, no restore needed.<br/>"
              "<i>State:</i> A = 0001, Q = 1001.", answer_bullet_style),
              
    Paragraph("• <b>Step 4:</b><br/>"
              "1. Shift Left AQ → A = 0011, Q = 011_<br/>"
              "2. Subtract M → A = 0011 + 1100 = 1111.<br/>"
              "3. Since A is negative, set Q<sub>0</sub> = 0, and restore A → A = 1111 + 0100 = 0011.<br/>"
              "<i>State:</i> A = 0011, Q = 0010.", answer_bullet_style),
    Paragraph("• <b>Restoring Result:</b> Quotient Q = <b>0010<sub>2</sub> (2)</b>, Remainder A = <b>0011<sub>2</sub> (3)</b>.", answer_bold_style),
    
    Spacer(1, 4),
    Paragraph("<b>Method 2: Non-Restoring Division (Step-by-Step):</b>", answer_bold_style),
    Paragraph("In Non-Restoring Division, we do not perform restoring additions. If A is positive, we shift left and subtract M. If A is negative, we shift left and add M.", answer_body_style),
    Paragraph("• <b>Init:</b> A = 0000, Q = 1011, M = 0100, -M = 1100", answer_bullet_style),
    
    Paragraph("• <b>Step 1 (A is positive):</b><br/>"
              "1. Shift Left AQ → A = 0001, Q = 011_<br/>"
              "2. Subtract M → A = 0001 + 1100 = 1101.<br/>"
              "3. Since A is negative, set Q<sub>0</sub> = 0 (no restore).<br/>"
              "<i>State:</i> A = 1101, Q = 0110.", answer_bullet_style),
              
    Paragraph("• <b>Step 2 (A is negative):</b><br/>"
              "1. Shift Left AQ → A = 1010, Q = 110_<br/>"
              "2. Add M → A = 1010 + 0100 = 1110.<br/>"
              "3. Since A is negative, set Q<sub>0</sub> = 0.<br/>"
              "<i>State:</i> A = 1110, Q = 1100.", answer_bullet_style),
              
    Paragraph("• <b>Step 3 (A is negative):</b><br/>"
              "1. Shift Left AQ → A = 1101, Q = 100_<br/>"
              "2. Add M → A = 1101 + 0100 = 0001.<br/>"
              "3. Since A is positive, set Q<sub>0</sub> = 1.<br/>"
              "<i>State:</i> A = 0001, Q = 1001.", answer_bullet_style),
              
    Paragraph("• <b>Step 4 (A is positive):</b><br/>"
              "1. Shift Left AQ → A = 0011, Q = 001_<br/>"
              "2. Subtract M → A = 0011 + 1100 = 1111.<br/>"
              "3. Since A is negative, set Q<sub>0</sub> = 0.<br/>"
              "<i>State:</i> A = 1111, Q = 0010.", answer_bullet_style),
              
    Paragraph("• <b>Correction Step:</b> Since A is negative at the end, perform <b>A = A + M</b> to restore final remainder:<br/>"
              "&nbsp;&nbsp;A = 1111 + 0100 = 0011.<br/>"
              "<i>Final Corrected State:</i> A = 0011, Q = 0010.", answer_bullet_style),
    Paragraph("• <b>Non-Restoring Result:</b> Quotient Q = <b>0010<sub>2</sub> (2)</b>, Remainder A = <b>0011<sub>2</sub> (3)</b>.", answer_bold_style),
]
elements.extend(make_cy603_qa("6", "3(Applying)", "CO2", "Perform binary division using restoring and non-restoring division methods with a suitable example.", q6_u2_ans))

# Q7: Fixed-point vs Floating-point comparison
q7_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Below is a detailed analysis contrasting Fixed-Point and Floating-Point number representations across range and precision boundaries:", answer_body_style),
    Paragraph("• <b>Range of Values:</b>", answer_bold_style),
    Paragraph("- <b>Fixed-Point:</b> Has a very narrow, restricted range of values because the radix point is fixed at a static bit position. <i>Example:</i> An 8-bit fixed-point format with a 4-bit integer part can only represent values between -8.0 and +7.93.", answer_bullet_style),
    Paragraph("- <b>Floating-Point:</b> Offers an exceptionally vast range of values because the exponent field dynamically shifts the radix point. <i>Example:</i> Standard 32-bit single-precision float can represent values from ±1.18 × 10<sup>-38</sup> to ±3.4 × 10<sup>38</sup>.", answer_bullet_style),
    Paragraph("• <b>Precision (Resolution):</b>", answer_bold_style),
    Paragraph("- <b>Fixed-Point:</b> Maintains constant, absolute precision across the entire range of values. The gap between any two consecutive representable numbers is identical.", answer_bullet_style),
    Paragraph("- <b>Floating-Point:</b> Exhibits variable, relative precision. The absolute precision is extremely high for values close to zero but degrades significantly for extremely large numbers (due to the limited 23-bit mantissa space).", answer_bullet_style),
]
elements.extend(make_cy603_qa("7", "4(Analyzing)", "CO2", "Analyze the difference between fixed-point and floating-point number representation in terms of range and precision.", q7_u2_ans))

# Q8: Hardware implementation of arithmetic unit
q8_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Designing a high-performance **Arithmetic Unit** stage requires satisfying key hardware requirements to support multiple parallel microoperations:", answer_body_style),
    Paragraph("• <b>Full Adder Array:</b> A central array of Full Adders (FAs) forms the core mathematical summation engine.", answer_bullet_style),
    Paragraph("• <b>Input Conditioning Logic (MUX):</b> Rather than routing register outputs directly to the adder inputs, multiplexers are used to condition the inputs first. For example, the Y input of the adder is driven by a multiplexer that selects between <i>B<sub>i</sub></i> (addition), <i>B<sub>i</sub>'</i> (subtraction), <i>0</i> (transfer), or <i>1</i> (decrement).", answer_bullet_style),
    Paragraph("• <b>Complementer Arrays:</b> Controlled XOR gates or inverters to generate 1's complements of registers instantly.", answer_bullet_style),
    Paragraph("• <b>Control Select Lines:</b> Dedicated selection pins (S<sub>1</sub>, S<sub>0</sub>, C<sub>in</sub>) driven directly by control memory to dynamically set the active arithmetic mode.", answer_bullet_style),
    Paragraph("• <b>Bus Latches &amp; Registers:</b> Bidirectional buffers and registers (like AC and DR) with Load lines tied to system clock edges to capture the result safely without race hazards.", answer_bullet_style),
]
elements.extend(make_cy603_qa("8", "4(Analyzing)", "CO2", "Examine the hardware implementation requirements for arithmetic unit design.", q8_u2_ans))

# Q9: Efficiency of Booth's algorithm
q9_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Booth's Multiplication Algorithm</b> offers significant efficiency improvements over conventional shift-and-add multiplication methods:", answer_body_style),
    Paragraph("• <b>Shift-and-Add Overhead:</b> Conventional multiplication requires examining every single bit of the multiplier. If a bit is 1, a full binary addition must occur. For an <i>n</i>-bit multiplier, this results in an average of <i>n/2</i> additions.", answer_bullet_style),
    Paragraph("• <b>Booth's Grouping Shortcut:</b> Booth's algorithm exploits the fact that a string of consecutive 1s in the multiplier (e.g. `00111100`, which represents 60) can be computed with a single subtraction at the start of the string (`2<sup>6</sup>`) and a single addition at the end (`2<sup>2</sup>`), rather than performing 4 separate additions (64 − 4 = 60).", answer_bullet_style),
    Paragraph("• <b>Efficiency Gains:</b>", answer_bold_style),
    Paragraph("- <b>Best-Case Speedup:</b> If the multiplier contains long sequences of 1s or 0s, the number of addition/subtraction cycles drops dramatically, reducing arithmetic hardware latency.", answer_bullet_style),
    Paragraph("- <b>Unified Signed Handling:</b> Unlike conventional methods (which require separate pre-processing steps to handle negative signs), Booth's algorithm naturally multiplies positive and negative 2's complement numbers without any sign adjustments, streamlining execution pathways.", answer_bullet_style),
]
elements.extend(make_cy603_qa("9", "5(Evaluating)", "CO2", "Evaluate the efficiency of Booth’s algorithm compared to conventional multiplication methods.", q9_u2_ans))

# Q10: Design a complete arithmetic unit
q10_u2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("To design a complete, multi-functional arithmetic unit capable of performing **addition, subtraction, multiplication, and division**, we organize the hardware into modular execution pipelines:", answer_body_style),
    Paragraph("<b>Functional Block Design of the Complete Arithmetic Unit:</b>", answer_bold_style),
    Paragraph("• <b>Adder-Subtractor Core:</b> An <i>n</i>-bit Parallel Binary Adder combined with XOR gates on the register B inputs. A control line **Sub** decides the function: if Sub = 0, it performs addition (A + B); if Sub = 1, it complements B and sets carry-in C<sub>0</sub> = 1, performing 2's complement subtraction (A + B' + 1).", answer_bullet_style),
    Paragraph("• <b>Booth's Multiplier Pipeline:</b> Incorporates a dedicated Shift Register (A-Q-Q<sub>-1</sub>) and an execution sequencer that automatically controls the Adder-Subtractor core based on Q<sub>0</sub>Q<sub>-1</sub> bit transitions, completing signed multiplications in <i>n</i> clock cycles.", answer_bullet_style),
    Paragraph("• <b>Restoring/Non-Restoring Division Module:</b> Integrates left-shift path lines on registers A and Q, feeding the output of the adder-subtractor back to A based on the sign of the remainder (MSB of A), enabling hardware division.", answer_bullet_style),
    Paragraph("• <b>Internal Control Bus Matrix:</b> Directs register load enable signals, MUX input routing, and clock gates to orchestrate data flows among all processing modules.", answer_bullet_style),
]
elements.extend(make_cy603_qa("10", "6(Creating )", "CO2", "Design an arithmetic unit capable of performing addition, subtraction, multiplication, and division operations.", q10_u2_ans))

# Build Document using NumberedCanvas for dynamic footer
doc.build(elements, canvasmaker=NumberedCanvas)

print(f"CY-603 COA Question Bank PDF generated successfully: {pdf_path}")
