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
            self.drawString(100, 805, " |   Database Management System (DBMS) Solved Question Bank")
            self.drawRightString(555, 805, "Units 1 &amp; 2 - Semester IV")
            
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
pdf_path = "DBMS_Units_1_2_Solved_Question_Bank.pdf"

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

def make_dbms_qa(num_str, pyq_str, q_text, answer_flowables):
    q_style = ParagraphStyle(
        'DbmsQStyle',
        parent=normal_style,
        fontName=font_name_bold,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
    )
    
    label = f"<b>{num_str}</b>"
    
    full_q_text = f"{q_text}"
    if pyq_str:
        full_q_text += f"<br/><font color='#0D9488' size='8'><b>[RGPV PYQ: {pyq_str}]</b></font>"
        
    p_num = Paragraph(label, q_style)
    p_text = Paragraph(full_q_text, ParagraphStyle('DbmsQText', parent=normal_style, fontName=font_name_bold, fontSize=10, leading=15))
    
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
        
    flowables.append(Spacer(1, 24)) # Space between solved questions
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
    [Paragraph("<b><font color='#0D9488'>EMo Learners</font> &nbsp;|&nbsp; Premium Solved Question Bank</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=15, leading=20, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>DATABASE MANAGEMENT SYSTEM (DBMS) SOLVED PYQS</b>", ParagraphStyle('HSub', fontName=font_name_bold, fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>RGPV Syllabus Focus Pattern — Semester IV (CSIT)</b>", ParagraphStyle('HSub2', fontName=font_name_bold, fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#1F2937')))],
    [Paragraph("<b>Complete Solved Solutions for Unit 1 and Unit 2 in Simplified Language</b>", ParagraphStyle('HDesc', fontName=font_name_bold, fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor('#4B5563')))]
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
        Paragraph("<b>Subject:</b> Database Management System (CSIT-405)", normal_style),
        Paragraph("<b>Target Audience:</b> B.Tech CSIT IV Semester", normal_style)
    ],
    [
        Paragraph("<b>Coverage:</b> Solved Unit 1 and Unit 2 Complete Question Set", normal_style),
        Paragraph("<b>Format Rule:</b> Simple Language, No Asterisks/Stars in Text", normal_style)
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
# 3. UNIT 1 SOLUTIONS
# ==========================================
elements.append(make_section_banner("UNIT 1: INTRODUCTION TO DATABASE MANAGEMENT SYSTEM"))

# Shared tables
t1_headers = [Paragraph("<b>Parameter</b>", table_header_style), 
              Paragraph("<b>Traditional File System</b>", table_header_style), 
              Paragraph("<b>Database Management System (DBMS)</b>", table_header_style)]
t1_row1 = [Paragraph("<b>Data Redundancy</b>", table_text_style), Paragraph("High; multiple files repeat duplicate information, wasting storage.", table_text_style), Paragraph("Minimal; centralized database minimizes duplicate storage entries.", table_text_style)]
t1_row2 = [Paragraph("<b>Data Consistency</b>", table_text_style), Paragraph("Poor; updating one file leaves redundant copies unchanged (inconsistency).", table_text_style), Paragraph("High; single central update reflects across all logical views.", table_text_style)]
t1_row3 = [Paragraph("<b>Access &amp; Querying</b>", table_text_style), Paragraph("Difficult; requires writing custom programs in C or Java to search files.", table_text_style), Paragraph("Easy; uses standard declaratives like SQL for rapid search queries.", table_text_style)]
t1_row4 = [Paragraph("<b>Data Isolation</b>", table_text_style), Paragraph("High; data is scattered in different formats, making integration hard.", table_text_style), Paragraph("Low; structured schemas provide unified access interfaces.", table_text_style)]
t1_row5 = [Paragraph("<b>Security &amp; Concurrency</b>", table_text_style), Paragraph("Very poor; no concurrent access controls or detailed user access limits.", table_text_style), Paragraph("Excellent; robust transaction locking and distinct user permission grants.", table_text_style)]
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

tk_headers = [Paragraph("<b>Constraint Type</b>", table_header_style), 
              Paragraph("<b>Core Rules &amp; Enforcement</b>", table_header_style), 
              Paragraph("<b>SQL Implementation Example</b>", table_header_style)]
tk_row1 = [Paragraph("<b>Domain Integrity</b>", table_text_style), 
           Paragraph("Restricts the set of values allowed in a specific column. Enforces data type, format, ranges, uniqueness, or nullability rules.", table_text_style), 
           Paragraph("<code>Age INT CHECK (Age &gt;= 18)</code> or <code>Status VARCHAR(10) NOT NULL</code>", table_text_style)]
tk_row2 = [Paragraph("<b>Entity Integrity</b>", table_text_style), 
           Paragraph("Requires that every relation must have a primary key. The primary key columns must contain unique, non-null values to identify each row.", table_text_style), 
           Paragraph("<code>Roll_No INT PRIMARY KEY</code>", table_text_style)]
tk_row3 = [Paragraph("<b>Referential Integrity</b>", table_text_style), 
           Paragraph("Maintains relationship links between tables. Requires that foreign key values in a child table must match an existing primary key in the parent table, or be set to NULL.", table_text_style), 
           Paragraph("<code>FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID) ON DELETE CASCADE</code>", table_text_style)]
tk_row4 = [Paragraph("<b>Key/Unique Constraints</b>", table_text_style), 
           Paragraph("Prevents duplicate values in a column or set of columns that are not the primary key, allowing NULL values in some DBMS.", table_text_style), 
           Paragraph("<code>Email VARCHAR(100) UNIQUE</code>", table_text_style)]
tk_table = Table([tk_headers, tk_row1, tk_row2, tk_row3, tk_row4], colWidths=[110, 200, 205])
tk_table.setStyle(TableStyle([
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


# Q1
q1_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Historically, data storage was managed by conventional file systems, where data was stored in isolated flat files directly managed by the host operating system. However, this approach introduced significant structural issues as applications scaled. A Database Management System (DBMS) addresses these limits by introducing a centralized, logical layer between the physical storage and the user applications.", answer_body_style),
    Spacer(1, 4),
    t1_table,
]
elements.extend(make_dbms_qa("Q.1", "May 2018, Dec 2020", "Explain the disadvantages of a conventional file-based system compared to a Database Management System.", q1_ans))

# Q2
q2_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In computer systems, low-level file operations are the basic instructions executed by the operating system to manage persistent data files on disk storage. Standard textbook explanations of these operations are defined below:", answer_body_style),
    Paragraph("<b>1. Open Operation:</b> The open operation is the initial step required to establish a logical connection between an active application and a persistent file stored on disk. The operating system's file manager resolves the directory path, checks access permissions, and allocates memory buffers to coordinate the upcoming data stream.", answer_bullet_style),
    Paragraph("<b>2. Read Operation:</b> The read operation retrieves data blocks from secondary storage and transfers them into RAM buffers. In a database, this is highly optimized through a buffer caching subsystem to ensure that subsequent requests for the same block can be served at memory speeds without hitting slow secondary storage.", answer_bullet_style),
    Paragraph("<b>3. Write (Insert) Operation:</b> The write operation appends new records or creates a fresh storage block to accommodate incoming data. To prevent physical data corruption, this operation must be coordinated with OS file locking schemes.", answer_bullet_style),
    Paragraph("<b>4. Update (Modify) Operation:</b> The update operation modifies existing byte structures. The storage manager performs a read-modify-write cycle: loading the target block, updating specific byte fields, and writing the dirty block back to secondary storage.", answer_bullet_style),
    Paragraph("<b>5. Delete Operation:</b> Deletion can be logical (marking a record with a deleted flag to bypass it) or physical (removing the record and compacting the block to free up space).", answer_bullet_style),
    Paragraph("<b>6. Close Operation:</b> The close operation flushes any unwritten RAM buffers back to disk, releases active operating system handles, and frees allocated memory.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.2", "June 2020", "Explain the operations of a file in detail.", q2_ans))

# Q3
q3_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The internal structure of a Database Management System consists of three distinct abstraction layers (External, Conceptual, Internal) to isolate user applications from physical storage hardware.", answer_body_style),
]
t_schema_img = get_image_flowable('three_schema_architecture.png', width=380, height=220)
if t_schema_img:
    q3_ans.append(t_schema_img)
    q3_ans.append(Spacer(1, 4))
q3_ans.extend([
    Paragraph("<b>1. The Three Abstraction Levels:</b>", answer_bold_style),
    Paragraph("• <b>External Level (View Schema):</b> Describes only the part of the database a specific user group cares about. It consists of multiple external views.", answer_bullet_style),
    Paragraph("• <b>Conceptual Level (Logical Schema):</b> Describes what data is stored and what relationships exist. It defines tables, domains, primary keys, and logical rules, completely hiding physical storage designs.", answer_bullet_style),
    Paragraph("• <b>Internal Level (Physical Schema):</b> Describes how data is physically stored in secondary storage devices. It details record formats, block sizes, indexes, and compression schemes.", answer_bullet_style),
])
elements.extend(make_dbms_qa("Q.3", "June 2020", "What is the architecture of a database?", q3_ans))

# Q4
q4_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A Database Management System (DBMS) consists of multiple coordinated components that handle query processing, transactional safety, buffer caching, and physical storage interface.", answer_body_style),
]
dbms_arch_img = get_image_flowable('dbms_architecture.png', width=380, height=220)
if dbms_arch_img:
    q4_ans.append(dbms_arch_img)
    q4_ans.append(Spacer(1, 4))
q4_ans.extend([
    Paragraph("<b>Functional Components of DBMS Architecture:</b>", answer_bold_style),
    Paragraph("<b>1. Query Parser and Compiler:</b> This subsystem acts as the entry point for all incoming database requests. It performs lexical and syntactic analysis on raw SQL text, checking it against the system catalog metadata to verify table names, column existence, and user privileges. The parsed query is then translated into a relational algebra expression tree.", answer_bullet_style),
    Paragraph("<b>2. Query Optimizer:</b> The query optimizer is the brain of the compiler. It analyzes multiple equivalent relational algebra trees and evaluates execution paths using a cost-based model. It calculates CPU and disk I/O costs based on database statistics (such as table sizes and index distributions) to select the most efficient plan.", answer_bullet_style),
    Paragraph("<b>3. Query Execution Engine:</b> The execution engine takes the compiled execution plan and coordinates physical operations. It makes calls to the buffer manager and transaction engine to fetch, join, sort, and write database blocks.", answer_bullet_style),
    Paragraph("<b>4. Buffer Manager:</b> Responsible for managing the database's RAM cache. It decides which pages of data should be loaded from disk into memory, and which pages should be evicted back to disk using caching algorithms like Least Recently Used (LRU).", answer_bullet_style),
    Paragraph("<b>5. Transaction and Lock Manager:</b> Monitors active database sessions to guarantee the ACID properties. It manages row-level locks to prevent dirty reads or lost updates and writes recovery logs to disk to handle system rollbacks.", answer_bullet_style),
])
elements.extend(make_dbms_qa("Q.4", "December 2020", "Define database management system. What are the major components of this system? Explain each component.", q4_ans))

# Q5
q5_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A <b>Data Model</b> is a logical collection of conceptual tools used to describe data, data relationships, data semantics, and consistency constraints. It acts as a blueprint for database design.", answer_body_style),
    Paragraph("<b>Primary Data Models in DBMS:</b>", answer_bold_style),
    Paragraph("<b>1. Relational Model:</b> Pioneered by Dr. E.F. Codd, the relational model represents all database data as logical tables called relations. Each row represents a distinct entity record (tuple), and columns represent attributes. Relationships are established mathematically using primary and foreign key references, providing high structural flexibility.", answer_bullet_style),
    Paragraph("<b>2. Entity-Relationship (ER) Model:</b> Introduced by Peter Chen, the ER model is a conceptual design tool. It models the real world as distinct entities (objects) and relationships (associations) between them. It is represented visually in ER diagrams to guide logical schema construction.", answer_bullet_style),
    Paragraph("<b>3. Hierarchical Model:</b> The hierarchical model organizes data in a parent-child tree structure. Each child node can have only one parent, mapping one-to-many relationships directly in the physical file layout. While fast for predefined paths, it is rigid and cannot handle many-to-many relationships easily.", answer_bullet_style),
    Paragraph("<b>4. Network Model:</b> An extension of the hierarchical model, the network model allows child nodes to have multiple parents, forming a graph structure. It represents many-to-many relationships directly via pointers, but the physical pointers make schema modifications highly complex.", answer_bullet_style),
    Paragraph("<b>5. Object-Oriented Model:</b> Extends relational databases by storing data as classes and objects, directly supporting object-oriented programming features like inheritance and encapsulation.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.5", "December 2020", "What is a data model? List a few data models that you know.", q5_ans))

# Q6
q6_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The Database Administrator (DBA) is the central authority who manages the entire database system. The DBA's responsibilities include:", answer_body_style),
    Paragraph("<b>1. Schema Definition and Conceptual Design:</b> The DBA is responsible for designing and creating the logical structure of the database. This involves writing DDL schemas to define tables, attributes, domains, and integrity constraints.", answer_bullet_style),
    Paragraph("<b>2. Access Security:</b> Creating user accounts, granting select/write permissions, and preventing unauthorized breaches.", answer_bullet_style),
    Paragraph("<b>3. System Monitoring and Backup:</b> Checking storage capacity, tuning query execution speeds, scheduling routine data backups, and restoring databases after system crashes.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.6", "June 2020", "Describe rules of DBA and its functions.", q6_ans))

# Q7
q7_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Attributes are logical properties of an entity. They are categorized based on value card limits:", answer_body_style),
    Paragraph("• <b>Single-Valued Attribute:</b> An attribute that holds exactly one value for a specific entity. For example, a student can have only one `Date_of_Birth` or one `Age` value.", answer_bullet_style),
    Paragraph("• <b>Multi-Valued Attribute:</b> An attribute that can hold multiple values for a single entity. For example, a student can have multiple `Phone_Numbers` or multiple `Email_IDs`. In ER diagrams, multi-valued attributes are represented using <b>double ovals</b>.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.7", "", "Differentiate between single valued and multivalued attributes.", q7_ans))

# Q8
q8_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Entity:</b> A real-world object or event that is distinguishable from other objects (e.g. a specific student John, a specific car, a transaction). Drawn as a rectangle box.", answer_bullet_style),
    Paragraph("• <b>Attribute:</b> A logical property or characteristic of an entity (e.g. a Student has Roll_No, Name, and Email). Drawn as an oval circle.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.8", "June 2020", "Write a short note on entities and attributes.", q8_ans))

# Q9
q9_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Formal database design requires a precise understanding of entities and their logical properties:", answer_body_style),
    Paragraph("• <b>Entity:</b> An Entity is a concrete or abstract real-world object that can be uniquely identified (e.g. a student named John).", answer_bullet_style),
    Paragraph("• <b>Entity Type:</b> An Entity Type is the logical blueprint or definition of that object, specifying the attributes it possesses (e.g. `Student` entity type with Roll, Name).", answer_bullet_style),
    Paragraph("• <b>Entity Set:</b> An Entity Set is the actual collection of all instances of a specific entity type stored in the database at any given time (e.g. all students currently enrolled in the university).", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.9", "June 2020", "What is an entity type? What is an entity set? Explain the differences among an entity, entity type, and an entity set.", q9_ans))

# Q10
q10_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The three critical functions of a Database Administrator (DBA) are:", answer_body_style),
    Paragraph("<b>1. Storage Schema Tuning and Physical Organization:</b> Deciding how data is structured on physical disks, building secondary indexes, and optimizing data retrieval paths.", answer_bullet_style),
    Paragraph("<b>2. Granting System Access and Permissions:</b> Assigning security levels, authorizing specific users, and granting selective data reads/writes.", answer_bullet_style),
    Paragraph("<b>3. Scheduling Backups and Recoveries:</b> Ensuring that routine data backups are written to secure offline storage and restoring database consistency after power failures or drive crashes.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.10", "", "Write any three functions of DBA.", q10_ans))

# Q11
q11_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A centralized Database Management System offers key structural advantages over traditional file-based schemes:", answer_body_style),
    Paragraph("• <b>Centralized Data Control:</b> Eliminates redundant storage entries across departments, ensuring disk capacity is optimized.", answer_bullet_style),
    Paragraph("• <b>Strict Data Consistency:</b> Central updates automatically apply across all dynamic user views, avoiding contradictory entries.", answer_bullet_style),
    Paragraph("• <b>Standardized Access &amp; Querying:</b> Enables data retrieval using high-level query languages like SQL, rather than writing custom file parsing scripts.", answer_bullet_style),
    Paragraph("• <b>Transaction Safety &amp; Security:</b> Implements secure locks and rollback logs to ensure database safety under concurrent access.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.11", "May 2019", "Explain the advantages of database management system over file management system.", q11_ans))

# Q12
q12_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The major operational advantages of using a DBMS are:", answer_body_style),
    Paragraph("• <b>Data Integration:</b> Combines scattered files into a unified logical schema.", answer_bullet_style),
    Paragraph("• <b>Concurrency Control:</b> Allows hundreds of concurrent users to read/write without overwriting one another's updates.", answer_bullet_style),
    Paragraph("• <b>Robust Security:</b> Limits tables to authorized users, protecting confidential databases.", answer_bullet_style),
    Paragraph("• <b>Crash Recovery:</b> Employs recovery managers to restore committed data after database crashes.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.12", "November 2019", "Write a short note on the advantages of a database system.", q12_ans))

# Q13
q13_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A Data Model acts as a conceptual framework for database layouts. The types of data models are:", answer_body_style),
    Paragraph("• <b>Relational Model:</b> Stores data in flat tables with keys.", answer_bullet_style),
    Paragraph("• <b>Entity-Relationship Model:</b> Models databases conceptually using entities, attributes, and associations.", answer_bullet_style),
    Paragraph("• <b>Hierarchical Model:</b> Structures records in a rigid parent-child tree layout.", answer_bullet_style),
    Paragraph("• <b>Network Model:</b> Structures records in a graph layout allowing multiple parents.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.13", "May 2019", "What is a data model? List the types of data models you used and explain them.", q13_ans))

# Q14
q14_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The internal structure of a Database Management System consists of multiple coordinated components that handle query parsing, plan optimization, safety locks, caching, and storage mapping.", answer_body_style),
]
if dbms_arch_img:
    q14_ans.append(dbms_arch_img)
    q14_ans.append(Spacer(1, 4))
q14_ans.extend([
    Paragraph("<b>Key Functional Components:</b>", answer_bold_style),
    Paragraph("• <b>Query Processor (Compiler &amp; Optimizer):</b> Takes incoming SQL statements, parses them for syntax, translates them into algebraic expressions, evaluates execution paths, and selects the most optimal path with minimum disk I/O.", answer_bullet_style),
    Paragraph("• <b>Database Execution Engine:</b> Receives the optimized plan from the query optimizer and interacts with the resource managers to execute instructions.", answer_bullet_style),
    Paragraph("• <b>Buffer Manager:</b> Controls physical RAM allocations. It caches frequently accessed data blocks from hard drives into fast memory pages, ensuring the CPU accesses RAM caches first.", answer_bullet_style),
    Paragraph("• <b>Transaction &amp; Lock Manager:</b> Ensures ACID safety. It monitors active transactions, writes transactional logs to disks, and places lock flags on active rows to prevent concurrent read/write data corruption.", answer_bullet_style),
])
elements.extend(make_dbms_qa("Q.14", "November 2019", "Explain the different components of DBMS. Also draw its architecture.", q14_ans))

# Q15
q15_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The <b>Database Administrator (DBA)</b> is the operational director of the database. The DBA manages system performance, maintains security profiles, manages logical structures, executes dynamic backups, and optimizes secondary indexes. The DBA also serves as the liaison between the organization's business needs and the raw physical storage architecture.", answer_body_style),
]
elements.extend(make_dbms_qa("Q.15", "May 2019", "Write a short note on DBA.", q15_ans))

# Q16
q16_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Entity:</b> A concrete or abstract real-world object that can be uniquely identified (e.g. a Student).", answer_bullet_style),
    Paragraph("• <b>Relationship:</b> An association or link between multiple entities (e.g. Student Enrolls in Course).", answer_bullet_style),
    Paragraph("• <b>Student Management System ER Layout:</b>", answer_body_style),
    Paragraph("1. <b>Student Entity:</b> Roll (Primary Key), Name, Email.", answer_bullet_style),
    Paragraph("2. <b>Course Entity:</b> Course_ID (Primary Key), Title, Fee.", answer_bullet_style),
    Paragraph("3. <b>Department Entity:</b> Dept_ID (Primary Key), Name.", answer_bullet_style),
    Paragraph("4. <b>Enrolls Relationship (M:N):</b> Connects Student and Course.", answer_bullet_style),
    Paragraph("5. <b>Belongs_To Relationship (N:1):</b> Connects Student and Department.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.16", "May 2019", "What is an entity? What is a relationship? Explain E-R modeling with the help of a database for a student management system.", q16_ans))

# Q17
q17_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The three levels of DBMS architecture are:", answer_body_style),
]
if t_schema_img:
    q17_ans.append(t_schema_img)
    q17_ans.append(Spacer(1, 4))
q17_ans.extend([
    Paragraph("• <b>External Level (User Views):</b> The highest level of data abstraction. It describes only the part of the database that a specific user group is interested in, showing distinct external schemas.", answer_bullet_style),
    Paragraph("• <b>Conceptual Level (Logical Schema):</b> The middle level of abstraction. It describes what data is stored in the database and what relationships exist between those data entities. It defines tables, domains, primary keys, and logical rules.", answer_bullet_style),
    Paragraph("• <b>Internal Level (Physical Schema):</b> The lowest level of data abstraction. It describes how data is physically stored in secondary storage devices, detailing record formats, block sizes, and indexes.", answer_bullet_style),
])
elements.extend(make_dbms_qa("Q.17", "May 2018", "Draw and discuss the three levels of a database management system.", q17_ans))

# Q18
q18_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Database Administrator (DBA):</b> The central authority who manages the entire database system. The DBA's responsibilities include schema creation, security authorization, performance tuning, and backup/recovery.", answer_bullet_style),
    Paragraph("• <b>Database Users:</b> Users access the database to perform their operational tasks. They include:", answer_body_style),
    Paragraph("1. <b>Application Programmers:</b> Write database access interfaces (e.g. JDBC, embedded SQL API) in C++ or Java.", answer_bullet_style),
    Paragraph("2. <b>Sophisticated Users:</b> Write custom SQL queries to perform deep analytical reports.", answer_bullet_style),
    Paragraph("3. <b>Naive Users:</b> Run pre-built applications with simple button clicks, without knowing the database schema.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.18", "May 2018", "What is the difference between a database user and a database administrator? Explain various functions of a DBA.", q18_ans))

# Q19
q19_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Schema:</b> The overall design and structural description of the database. It is static, written in DDL, and rarely changes. It defines tables, attributes, and keys.", answer_bullet_style),
    Paragraph("• <b>Instance:</b> The actual data stored in the database at a specific moment. It is dynamic, modified using DML, and changes continuously as records are inserted, updated, or deleted.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.19", "December 2017", "Write a short note on schemas and instances.", q19_ans))

# Q20
q20_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The <b>Three-Schema Architecture</b> (ANSI-SPARC architecture) divides the database into three abstraction layers to hide hardware details from users, making it easy to change one layer without breaking the others.", answer_body_style),
]
if t_schema_img:
    q20_ans.append(t_schema_img)
    q20_ans.append(Spacer(1, 4))
q20_ans.extend([
    Paragraph("• <b>External Schema (External View Level):</b> Displays custom views for distinct user groups, hiding unrelated tables.", answer_bullet_style),
    Paragraph("• <b>Conceptual Schema (Logical Level):</b> Defines all tables, primary keys, foreign keys, logical integrity rules, and database metadata.", answer_bullet_style),
    Paragraph("• <b>Internal Schema (Physical Level):</b> Maps files, directories, data formats, indexes, and caching records to physical storage hardware.", answer_bullet_style),
])
elements.extend(make_dbms_qa("Q.20", "Dec 2017", "With a neat sketch discuss the three schema architecture of DBMS.", q20_ans))

# Q21
q21_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The responsibilities of the Database Administrator (DBA) and Database Designer are distinguished below:", answer_body_style),
    Paragraph("• <b>Database Designers:</b> Responsible for the conceptual and logical design of the database. They identify the data to be stored, choose tables, columns, constraints, and relationships. They work before construction starts.", answer_bullet_style),
    Paragraph("• <b>Database Administrator (DBA):</b> Responsible for the physical execution, maintenance, security, and performance of the completed database. The DBA manages system access, grants permissions, coordinates backups, and tunes query speeds.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.21", "June 2017", "Explain the responsibilities of the DBA and the database designers.", q21_ans))

# Q22
q22_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The conventional file system has severe disadvantages compared to a Database Management System:", answer_body_style),
    Paragraph("• <b>Data Redundancy:</b> Multiple copies of the same data are stored in different files, wasting physical disk space.", answer_bullet_style),
    Paragraph("• <b>Data Inconsistency:</b> Updating one file leaves duplicates unchanged, creating contradictory records.", answer_bullet_style),
    Paragraph("• <b>Access Anomalies:</b> Requires writing custom programming code to extract and search data, lacking declarative query systems.", answer_bullet_style),
    Paragraph("• <b>Concurrency Limits:</b> Multiple users cannot update the same file concurrently without creating file conflict errors.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.22", "June 2022", "Describe various disadvantages of a file system compared to a Database Management System.", q22_ans))

# Q23
q23_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("A Database Management System (DBMS) consists of multiple coordinated components that handle query parsing, plan optimization, safety locks, caching, and storage mapping.", answer_body_style),
]
if dbms_arch_img:
    q23_ans.append(dbms_arch_img)
    q23_ans.append(Spacer(1, 4))
q23_ans.extend([
    Paragraph("• <b>Query Processor:</b> Parses, compiles, and optimizes SQL queries for execution.", answer_bullet_style),
    Paragraph("• <b>Buffer Manager:</b> Coordinates data transfer between disk storage and RAM cache.", answer_bullet_style),
    Paragraph("• <b>Transaction &amp; Lock Manager:</b> Ensures ACID safety by locking rows during concurrent writes.", answer_bullet_style),
    Paragraph("• <b>Storage Engine:</b> Low-level driver interface for file read/write operations.", answer_bullet_style),
])
elements.extend(make_dbms_qa("Q.23", "June 2022", "Explain the components of DBMS with a neat diagram.", q23_ans))

# Q24
q24_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The key architectural concepts in database theory are defined below:", answer_body_style),
    Paragraph("• <b>Levels of Data Abstraction:</b> The division of database views into physical (storage details), conceptual (logical rules), and external (user views) levels to simplify data interaction.", answer_bullet_style),
    Paragraph("• <b>Instance:</b> The actual collection of data values stored in the tables at a specific point in time. It is highly dynamic.", answer_bullet_style),
    Paragraph("• <b>Schema:</b> The static design structure of the database, written in DDL, defining tables, domains, and relationships.", answer_bullet_style),
    Paragraph("• <b>Physical Data Independence:</b> The ability to modify physical schemas (e.g. changing disk paths or indexes) without altering logical conceptual schemas.", answer_bullet_style),
    Paragraph("• <b>Logical Data Independence:</b> The ability to modify logical conceptual schemas (e.g. adding columns or tables) without altering existing external views or SQL queries.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.24", "June 2022", "Define and explain the following terms: Levels of data abstraction, Instances, Schema, Physical data independence, and Logical data independence.", q24_ans))

elements.append(PageBreak())

# ==========================================
# 7. UNIT 2 SOLUTIONS
# ==========================================
elements.append(make_section_banner("UNIT 2: RELATIONAL DATABASE MODEL &amp; ER MODELING"))

# Q25 (Q.1)
q25_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In the relational database model, a relation contains two distinct structural characteristics:", answer_body_style),
    Paragraph("• <b>Relational Intension (Schema):</b> The permanent structural definition of the relation table. It specifies the table name, the names of all columns (attributes), and their permitted data types (domains). It is static, defined using DDL commands, and rarely changes. For example, `Student(Roll: INT, Name: VARCHAR, Age: INT)` is the intension.", answer_bullet_style),
    Paragraph("• <b>Relational Extension (State/Instance):</b> The dynamic collection of rows (tuples) present in the table at a specific point in time. It represents the actual data values stored in the table cells. It is dynamic, altered continuously using DML commands (insert, delete, update). For example, the row `(101, 'John', 21)` represents a single tuple in the extension.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.25", "", "Explain relational schema intension and extension.", q25_ans))

# Q26 (Q.2)
q26_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Relational Algebra is a formal procedural query language that takes one or more relations as input and produces a new relation as output. Its six fundamental operations are explained below:", answer_body_style),
    Paragraph("<b>1. Selection (&sigma;):</b> A unary operator that filters rows based on a boolean criteria, extracting subset rows from a table. For example, &sigma;<sub>Age &gt; 20</sub>(Students) filters student rows where age exceeds 20.", answer_bullet_style),
    Paragraph("<b>2. Projection (&pi;):</b> A unary operator that selects specific attribute columns, discarding the rest and removing duplicates from the result set. For example, &pi;<sub>Name, Roll</sub>(Students) extracts only the Name and Roll columns.", answer_bullet_style),
    Paragraph("<b>3. Union (&cup;):</b> Combines rows from two relations. The relations must be union-compatible (have same number of columns with matching domain types). Discards duplicates.", answer_bullet_style),
    Paragraph("<b>4. Set Difference (&minus;):</b> Finds rows that are present in the first relation R but absent in the second relation S (R and S must be union-compatible).", answer_bullet_style),
    Paragraph("<b>5. Cartesian Product (&times;):</b> Combines every row of relation R with every row of relation S, producing all possible row combinations. If R has m rows and S has n rows, the product has m times n rows.", answer_bullet_style),
    Paragraph("<b>6. Rename (&rho;):</b> Alters the logical attribute names or the table identifier name.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.26", "May 2018, Dec 2020", "What is relational algebra? List and explain the fundamental operations of relational algebra.", q26_ans))

# Q27 (Q.3)
q27_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The application of selection, projection, and natural join operations in relational algebra is described below:", answer_body_style),
    Paragraph("<b>1. Selection (&sigma;):</b> A unary operator that filters rows based on a boolean criteria, extracting subset rows from a table. For example, &sigma;<sub>Salary &gt; 50000</sub>(Employee) returns rows where Salary exceeds 50000.", answer_bullet_style),
    Paragraph("<b>2. Projection (&pi;):</b> A unary operator that selects specific attribute columns, discarding the rest and removing duplicates from the result set. For example, &pi;<sub>Name, Salary</sub>(Employee) outputs only the Name and Salary columns.", answer_bullet_style),
    Paragraph("<b>3. Natural Join (&bowtie;):</b> A binary operator that combines rows from two tables by matching values in their common columns. It automatically eliminates duplicate join columns in the output relation. For example, Employee &bowtie; Department combines employee rows with their matching department details using the common `Dept_ID` column.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.27", "Dec 2020", "Explain the following relational algebra operations: (i) Natural join operation, (ii) Selection and projection operation.", q27_ans))

# Q28 (Q.4)
q28_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("An Entity-Relationship (ER) diagram represents the database schema visually using rectangles (entities), circles (attributes), and diamonds (relationships).", answer_body_style),
]
er_lib_img = get_image_flowable('er_diagram_library.png', width=380, height=220)
if er_lib_img:
    q28_ans.append(er_lib_img)
    q28_ans.append(Spacer(1, 4))
q28_ans.extend([
    Paragraph("<b>Library ER Schema Elements:</b>", answer_bold_style),
    Paragraph("• <b>Entities &amp; Attributes:</b> Book (Book_ID, Title, Author, Price), Member (Member_ID, Name, Email, Phone), and Publisher (Publisher_ID, Name, City).", answer_bullet_style),
    Paragraph("• <b>Relationships &amp; Cardinality:</b>", answer_bullet_style),
    Paragraph("1. <b>Borrows (Many-to-Many):</b> Multiple members can borrow multiple books. Cardinality is M:N.", answer_bullet_style),
    Paragraph("2. <b>Publishes (One-to-Many):</b> One publisher publishes multiple books, but a book belongs to only one publisher. Cardinality is 1:N.", answer_bullet_style),
])
elements.extend(make_dbms_qa("Q.28", "May 2018, Dec 2020", "Define ER diagram. Draw an ER diagram for a library management system. Assume relevant entities and attributes.", q28_ans))

# Q29 (Q.5)
q29_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Constraints enforce rules on database tables to guarantee accuracy and validity. Fundamental constraints are compared below:", answer_body_style),
    Spacer(1, 4),
    tk_table,
]
elements.extend(make_dbms_qa("Q.29", "June 2020", "List various types of constraints in a database. Explain any two in detail.", q29_ans))

# Q30 (Q.6)
q30_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Generalization and Specialization are advanced abstraction techniques used in extended ER models:", answer_body_style),
    Paragraph("• <b>Specialization (Top-Down Approach):</b> The process of breaking down a high-level entity into multiple lower-level sub-entities based on distinct characteristics. For example, we start with a high-level entity `Employee`. Based on job roles, we specialize it down into `Salaried_Staff` (monthly pay) and `Hourly_Contractors` (hourly pay) sub-entities.", answer_bullet_style),
    Paragraph("• <b>Generalization (Bottom-Up Approach):</b> The process of combining multiple lower-level entities that share common features into a single, unified high-level entity. For example, we start with distinct entities `Car`, `Truck`, and `Motorcycle`. Since they all share attributes like `Vehicle_ID`, `Model`, and `Fuel_Type`, we generalize them into a single high-level entity `Vehicle`.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.30", "June 2020", "Describe generalization and specialization with examples.", q30_ans))

# Q31 (Q.7)
q31_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Mapping constraints (or cardinality ratios) define the maximum number of relationship instances an entity can participate in. They are:", answer_body_style),
    Paragraph("• <b>1. One-to-One (1:1):</b> An entity in A is associated with at most one entity in B. (e.g. A pilot flies at most one airplane).", answer_bullet_style),
    Paragraph("• <b>2. One-to-Many (1:N):</b> An entity in A is associated with any number of entities in B, but B is associated with at most one in A. (e.g. A department employs multiple employees).", answer_bullet_style),
    Paragraph("• <b>3. Many-to-One (N:1):</b> An entity in A is associated with at most one in B, but B is associated with any number in A. (e.g. Multiple students major in one department).", answer_bullet_style),
    Paragraph("• <b>4. Many-to-Many (M:N):</b> Entities in both sets can associate with any number of entities in the other. (e.g. Doctors and Patients).", answer_bullet_style),
    Paragraph("• <b>Hospital ER Schema:</b>", answer_body_style),
    Paragraph("1. <b>Doctor Entity:</b> Doc_ID (Primary Key), Name, Specialization.", answer_bullet_style),
    Paragraph("2. <b>Patient Entity:</b> Pat_ID (Primary Key), Name, Disease.", answer_bullet_style),
    Paragraph("3. <b>Treats Relationship (M:N):</b> Connects Doctor and Patient, indicating a many-to-many relationship.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.31", "November 2019", "Explain the different types of mapping constraints. Draw an ER diagram for a hospital with doctors and patients.", q31_ans))

# Q32 (Q.8)
q32_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Indicating Relationships:</b> Relationships are drawn as <b>diamond boxes</b> on the link lines connecting related entity rectangles. The cardinality ratio is written next to the lines (e.g. 1 and N).", answer_bullet_style),
    Paragraph("• <b>Weak Entity:</b> A weak entity does not possess a primary key and depends entirely on an identifying relationship with a strong parent entity. If the parent is deleted, the weak entity is deleted.", answer_bullet_style),
    Paragraph("• <b>Representation:</b> Drawn as a <b>double rectangle</b> box, and its identifying relationship is drawn as a <b>double diamond</b>.", answer_bullet_style),
    Paragraph("• <b>Example:</b> `Dependent` of an Employee. The `Dependent` is identified by the parent's `Emp_ID` combined with the dependent's `Name`.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.32", "November 2019", "How is a relationship between entities indicated in an ER diagram? What is a weak entity, how is it represented, and give an example?", q32_ans))

# Q33 (Q.9)
q33_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("The differences between strong and weak entity sets are defined below:", answer_body_style),
    Paragraph("• <b>Strong Entity Set:</b> Possesses a primary key that uniquely identifies each entity row inside the set. It stands independently without requiring relationships with other tables. Drawn as a standard single rectangle box (e.g. `Employee` with `Emp_ID`).", answer_bullet_style),
    Paragraph("• <b>Weak Entity Set:</b> Does not have a primary key and cannot be uniquely identified on its own. It depends on an identifying relationship with a strong parent entity to exist. It uses a partial key (discriminator) drawn with a dashed underline. Drawn as a double rectangle (e.g. `Dependent` of an Employee).", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.33", "November 2019", "Write a short note on weak and strong entity sets.", q33_ans))

# Q34 (Q.10)
q34_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Relational Algebra</b> is a formal theoretical query language for relational databases. It operates on relations as mathematical sets, providing operators to filter rows (selection), extract columns (projection), combine tables (joins and Cartesian products), and rename relations. It provides a formal framework for database engine query processing and optimization.", answer_body_style),
]
elements.extend(make_dbms_qa("Q.34", "May 2019", "Write a short note on relational algebra.", q34_ans))

# Q35 (Q.11)
q35_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In the relational database model, key theoretical terms are defined as follows:", answer_body_style),
    Paragraph("• <b>(i) Domain:</b> The set of all valid, atomic values permitted for a specific attribute. It acts as a data type filter. For example, positive integers between 16 and 35.", answer_bullet_style),
    Paragraph("• <b>(ii) Double (Tuple):</b> In database theory, 'Double' is a typo representing a <b>Tuple</b> (a single row in a table representing a single data record or relationship instance).", answer_bullet_style),
    Paragraph("• <b>(iii) Schema:</b> The structural definition of a relation table. It lists the table name and its attribute columns. For example, `Student(Roll: INT, Name: VARCHAR)`.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.35", "", "Explain the following terms: (i) Domains, (ii) Double (Tuple), (iii) Schemas.", q35_ans))

# Q36 (Q.12)
q36_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("An ER Diagram for a <b>University Database</b> defines academic entities and their associations:", answer_body_style),
    Paragraph("• <b>Entities &amp; Attributes:</b>", answer_body_style),
    Paragraph("1. <b>Department:</b> Dept_ID (Primary Key), Name, Office_Room.", answer_bullet_style),
    Paragraph("2. <b>Instructor:</b> Inst_ID (Primary Key), Name, Salary.", answer_bullet_style),
    Paragraph("3. <b>Course:</b> Course_ID (Primary Key), Title, Credits.", answer_bullet_style),
    Paragraph("4. <b>Student:</b> Roll_No (Primary Key), Name, Year.", answer_bullet_style),
    Paragraph("• <b>Relationships:</b>", answer_body_style),
    Paragraph("1. <b>Member_Of (Many-to-One):</b> Instructors and Students belong to a Department.", answer_bullet_style),
    Paragraph("2. <b>Teaches (One-to-Many):</b> An instructor teaches multiple courses, but a course has one instructor.", answer_bullet_style),
    Paragraph("3. <b>Enrolls (Many-to-Many):</b> Students enroll in courses (cardinality M:N).", answer_bullet_style),
    Paragraph("4. <b>Offers (One-to-Many):</b> A department offers multiple courses.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.36", "", "Draw an ER diagram of a University by determining entities of interest and relationships.", q36_ans))

# Q37 (Q.13)
q37_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Joins combine rows from two tables by matching values in their common columns. The major types of joins are:", answer_body_style),
    Paragraph("• <b>1. Inner Join (Natural Join):</b> Combines rows from two tables that have matching values in their common columns, discarding non-matching rows.", answer_bullet_style),
    Paragraph("• <b>2. Left Outer Join:</b> Keeps all rows from the left table, plus matching rows from the right table. Non-matching right columns are set to NULL.", answer_bullet_style),
    Paragraph("• <b>3. Right Outer Join:</b> Keeps all rows from the right table, plus matching rows from the left table. Non-matching left columns are set to NULL.", answer_bullet_style),
    Paragraph("• <b>4. Full Outer Join:</b> Keeps all rows from both tables, filling NULLs on either side where matches are missing.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.37", "May 2018", "Explain various types of joins with examples.", q37_ans))

# Q38 (Q.14)
q38_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Integrity constraints enforce database consistency rules. They include:", answer_body_style),
    Paragraph("• <b>1. Domain Constraint:</b> Restricts attribute values to a predefined domain (e.g. `Age` must be positive integer).", answer_bullet_style),
    Paragraph("• <b>2. Entity Integrity:</b> Primary keys cannot accept NULL values, ensuring every row is identifiable.", answer_bullet_style),
    Paragraph("• <b>3. Referential Integrity:</b> Foreign keys must point to a valid existing primary key row in a parent table, or be set to NULL.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.38", "May 2018", "What are integrity constraints? Explain various types of integrity constraints with examples.", q38_ans))

# Q39 (Q.15)
q39_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("• <b>Join Operation:</b> Combines tables horizontally by matching values in common columns. An <b>Inner Join</b> discards unmatched rows. An <b>Outer Join</b> keeps unmatched rows, padding the missing values with <b>NULL</b>.", answer_bullet_style),
    Paragraph("• <b>Union Operation:</b> Combines rows vertically from two union-compatible relations. It appends the rows of the second table to the first table, removing duplicate entries.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.39", "June 2017", "Explain clearly JOIN and UNION operations. Bring out the difference between Natural Join and Outer Join.", q39_ans))

# Q40 (Q.16)
q40_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In relational algebra, operators are categorized as fundamental or derived:", answer_body_style),
    Paragraph("• <b>Fundamental Operators:</b> Selection (&sigma;), Projection (&pi;), Union (&cup;), Set Difference (&minus;), Cartesian Product (&times;), Rename (&rho;).", answer_bullet_style),
    Paragraph("• <b>Derived Operators:</b> Natural Join (&bowtie;), Intersection (&cap;), Division (&divide;), and Theta Join. These can be mathematically formulated using combinations of the fundamental operators.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.40", "June 2017", "Discuss the different relational algebra operations.", q40_ans))

# Q41 (Q.17)
q41_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("For the musical company problem description, the ER diagram and relational schema are defined as follows:", answer_body_style),
    Paragraph("<b>1. Entities and Attributes:</b>", answer_bold_style),
    Paragraph("• <b>Musician:</b> Mus_ID (Primary Key), Name, Address, and phone number (Multi-valued attribute, drawn as double oval).", answer_bullet_style),
    Paragraph("• <b>Instrument:</b> Inst_ID (Primary Key), Name, Musical_Key.", answer_bullet_style),
    Paragraph("• <b>Album:</b> Alb_ID (Primary Key), Title, Format, Producer_ID (Foreign Key).", answer_bullet_style),
    Paragraph("• <b>Song:</b> Song_ID (Primary Key), Title, Author.", answer_bullet_style),
    Paragraph("<b>2. Relationships &amp; Cardinality:</b>", answer_bold_style),
    Paragraph("• <b>Plays (Many-to-Many):</b> Musician and Instrument (M:N cardinality).", answer_bullet_style),
    Paragraph("• <b>Performs (Many-to-Many):</b> Musician and Song (M:N cardinality).", answer_bullet_style),
    Paragraph("• <b>Produces (One-to-Many):</b> A musician produces multiple albums. Cardinality is 1:N.", answer_bullet_style),
    Paragraph("• <b>Contains (One-to-Many):</b> An album contains multiple songs.", answer_bullet_style),
    Spacer(1, 4),
    Paragraph("<b>3. Relational Schema Mapping:</b>", answer_bold_style),
    Paragraph("• `Musician(Mus_ID, Name, Address)`<br/>"
              "• `Musician_Phones(Mus_ID, Phone_No)` (Multi-valued attribute split into separate table)<br/>"
              "• `Instrument(Inst_ID, Name, Musical_Key)`<br/>"
              "• `Album(Alb_ID, Title, Format, Producer_Mus_ID)` (Foreign key points to Musician)<br/>"
              "• `Song(Song_ID, Title, Author, Alb_ID)` (Foreign key points to Album)<br/>"
              "• `Plays(Mus_ID, Inst_ID)` (Many-to-many bridge table)<br/>"
              "• `Performs(Mus_ID, Song_ID)` (Many-to-many bridge table)", code_style),
]
elements.extend(make_dbms_qa("Q.41", "December 2017", "Draw an ER diagram and map it to a relational schema for the Musicians company database.", q41_ans))

# Q42 (Q.18)
q42_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("An ER Diagram for a <b>Hospital Management System</b> organizes medical and patient records:", answer_body_style),
    Paragraph("• <b>Entities &amp; Attributes:</b>", answer_body_style),
    Paragraph("1. <b>Doctor:</b> Doc_ID (Primary Key), Name, Specialization, Phone.", answer_bullet_style),
    Paragraph("2. <b>Patient:</b> Pat_ID (Primary Key), Name, Age, Disease.", answer_bullet_style),
    Paragraph("3. <b>Ward:</b> Ward_No (Primary Key), Bed_Count, Type.", answer_bullet_style),
    Paragraph("4. <b>Medicine:</b> Med_ID (Primary Key), Name, Price, Expiry_Date.", answer_bullet_style),
    Paragraph("5. <b>Billing:</b> Bill_ID (Primary Key), Amount, Payment_Mode, Date.", answer_bullet_style),
    Paragraph("• <b>Relationships:</b>", answer_body_style),
    Paragraph("1. <b>Treats (Many-to-Many):</b> A doctor treats multiple patients.", answer_bullet_style),
    Paragraph("2. <b>Admits (One-to-Many):</b> A ward admits multiple patients.", answer_bullet_style),
    Paragraph("3. <b>Generates (One-to-One):</b> A patient registration generates exactly one bill.", answer_bullet_style),
    Paragraph("4. <b>Prescribes (Many-to-Many):</b> A doctor prescribes medicines to patients.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.42", "June 2017", "Draw an ER diagram for a Hospital Management System with at least 5 entities.", q42_ans))

# Q43 (Q.19)
q43_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Constraints enforce rules on data inside tables to maintain accuracy and reliability. Key database constraints are compared below:", answer_body_style),
    Spacer(1, 4),
    tk_table,
]
elements.extend(make_dbms_qa("Q.43", "December 2017", "Define Domain Integrity, Entity Integrity, and Referential Integrity constraints.", q43_ans))

# Q44 (Q.20)
q44_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Referential Integrity</b> is a database consistency rule. It requires that a foreign key column inside a child table must match a valid, existing primary key value inside its parent table. This prevents orphan rows. Database engines enforce referential integrity using constraints and cascading triggers (such as `ON DELETE CASCADE`), ensuring that deleting a parent record automatically deletes or updates its children.", answer_body_style),
]
elements.extend(make_dbms_qa("Q.44", "", "Define the term referential integrity in detail.", q44_ans))

# Q45 (Q.21)
q45_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("Generalization and Specialization are advanced abstraction techniques used in extended ER models:", answer_body_style),
    Paragraph("• <b>Specialization (Top-Down Approach):</b> The process of breaking down a high-level entity into multiple lower-level sub-entities based on distinct characteristics. For example, we start with a high-level entity `Employee`. Based on job roles, we specialize it down into `Salaried_Staff` (monthly pay) and `Hourly_Contractors` (hourly pay) sub-entities.", answer_bullet_style),
    Paragraph("• <b>Generalization (Bottom-Up Approach):</b> The process of combining multiple lower-level entities that share common features into a single, unified high-level entity. For example, we start with distinct entities `Car`, `Truck`, and `Motorcycle`. Since they all share attributes like `Vehicle_ID`, `Model`, and `Fuel_Type`, we generalize them into a single high-level entity `Vehicle`.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.45", "June 2022", "Differentiate specialization and generalization with the help of examples.", q45_ans))

# Q46 (Q.22)
q46_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("In the relational database model, keys are critical constraints used to identify rows and link tables. They include:", answer_body_style),
    Paragraph("• <b>1. Super Key:</b> Any set of one or more attributes that can uniquely identify a row inside a table.", answer_bullet_style),
    Paragraph("• <b>2. Candidate Key:</b> A minimal superkey (contains no redundant attributes).", answer_bullet_style),
    Paragraph("• <b>3. Primary Key:</b> The candidate key chosen by the DBA to uniquely identify rows. It cannot accept NULL values.", answer_bullet_style),
    Paragraph("• <b>4. Alternate Key:</b> Candidate keys that were not chosen as the primary key.", answer_bullet_style),
    Paragraph("• <b>5. Foreign Key:</b> A column in a table that points to the primary key of another table, establishing referential integrity links.", answer_bullet_style),
]
elements.extend(make_dbms_qa("Q.46", "June 2022", "Explain in detail about various key constraints used in a database system.", q46_ans))

# Q47 (Q.23)
q47_ans = [
    Paragraph("<b>Answer:</b>", answer_bold_style),
    Paragraph("<b>Referential Integrity</b> is a database consistency rule. It requires that a foreign key column inside a child table must match a valid, existing primary key value inside its parent table. This prevents orphan rows. Database engines enforce referential integrity using constraints and cascading triggers (such as `ON DELETE CASCADE`), ensuring that deleting a parent record automatically deletes or updates its children.", answer_body_style),
]
elements.extend(make_dbms_qa("Q.47", "", "Describe the concept of Referential Integrity.", q47_ans))

# Build Document using NumberedCanvas for dynamic footer page counting
doc.build(elements, canvasmaker=NumberedCanvas)

print(f"DBMS Premium Solved Question Bank PDF generated successfully: {pdf_path}")
