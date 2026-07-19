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
        
        # 1. Header (only draw on page 2 and later)
        if self._pageNumber > 1:
            self.setFont(font_name_bold, 8)
            self.setFillColor(colors.HexColor('#1E3A8A')) # Deep Navy
            self.drawString(40, 805, "EMo Learners")
            self.setFont(font_name, 8)
            self.setFillColor(colors.HexColor('#4B5563')) # Medium Gray
            self.drawString(100, 805, " |   Analysis and Design of Algorithms (ADA)")
            self.drawRightString(555, 805, "Unit 1 & Unit 2 Objective Questions")
            
            # Header line
            self.setStrokeColor(colors.HexColor('#E5E7EB')) # Light grey
            self.setLineWidth(0.5)
            self.line(40, 797, 555, 797)
            
        # 2. Footer (draw on all pages)
        self.setStrokeColor(colors.HexColor('#E5E7EB'))
        self.setLineWidth(0.75)
        self.line(40, 45, 555, 45)
        
        # Footer left text (with EMo Learners brand highlighted)
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
pdf_path = "ADA_Unit_1_2_Question_Bank.pdf"

# Set up standard doc with comfortable margins
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=60,  # Extra room for header
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
    textColor=colors.HexColor('#1E3A8A') # Deep Navy
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
    leading=14.5,
    textColor=colors.HexColor('#1F2937') # Charcoal dark gray
)

bold_style = ParagraphStyle(
    'BoldStyle',
    fontName=font_name_bold,
    fontSize=9.5,
    leading=14.5,
    textColor=colors.HexColor('#1F2937')
)

section_header_style = ParagraphStyle(
    'SectionHeaderStyle',
    fontName=font_name_bold,
    fontSize=10.5,
    leading=14,
    textColor=colors.white,
    keepWithNext=True
)

answer_style = ParagraphStyle(
    'AnswerStyle',
    fontName=font_name_bold,
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#0D9488') # Teal highlight for answers
)

solution_style = ParagraphStyle(
    'SolutionStyle',
    fontName=font_name,
    fontSize=9,
    leading=13.5,
    textColor=colors.HexColor('#374151') # Slate gray for solutions
)

def make_section_banner(title_text):
    banner_table = Table([[Paragraph(title_text, section_header_style)]], colWidths=[515])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1E3A8A')), # Deep Navy
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return KeepTogether([Spacer(1, 10), banner_table, Spacer(1, 8)])

def make_options_table(opt_a, opt_b, opt_c, opt_d, style):
    max_len = max(len(opt_a), len(opt_b), len(opt_c), len(opt_d))
    
    p_a = Paragraph(f"<b>A.</b> {opt_a}", style)
    p_b = Paragraph(f"<b>B.</b> {opt_b}", style)
    p_c = Paragraph(f"<b>C.</b> {opt_c}", style)
    p_d = Paragraph(f"<b>D.</b> {opt_d}", style)
    
    # Question text width is 495 (515 - 20 question number width)
    if max_len < 20:
        col_widths = [123.75, 123.75, 123.75, 123.75]
        data = [[p_a, p_b, p_c, p_d]]
    elif max_len < 45:
        col_widths = [247.5, 247.5]
        data = [
            [p_a, p_b],
            [p_c, p_d]
        ]
    else:
        col_widths = [495]
        data = [
            [p_a],
            [p_b],
            [p_c],
            [p_d]
        ]
        
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t

def make_solution_box(ans_text, sol_text):
    ans_html = f"<b>Answer:</b> {ans_text}"
    sol_html = f"<b>Solution:</b> {sol_text}"
    
    content = [
        Paragraph(ans_html, answer_style),
        Spacer(1, 3),
        Paragraph(sol_html, solution_style)
    ]
    
    box_table = Table([[content]], colWidths=[495])
    box_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')), # Slate 50 background
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINELEFT', (0, 0), (0, -1), 3, colors.HexColor('#0D9488')), # Teal left border
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')), # Light border around other sides
    ]))
    return box_table

def make_question(num_str, text_str, opt_table, sol_box):
    q_style = ParagraphStyle(
        'QStyle',
        parent=normal_style,
        fontName=font_name_bold,
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor('#1E3A8A') # Deep Navy for question index
    )
    
    p_num = Paragraph(f"<b>{num_str}</b>", q_style)
    p_text = Paragraph(text_str, ParagraphStyle('QText', parent=normal_style, fontSize=10, leading=14.5))
    
    row_data = [[p_num, p_text]]
    q_table = Table(row_data, colWidths=[20, 495])
    q_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    # Combine question, options, and solution box in a KeepTogether to avoid orphaned pages
    flowables = [
        q_table,
        Spacer(1, 4),
        opt_table,
        Spacer(1, 6),
        sol_box,
        Spacer(1, 12)
    ]
    return KeepTogether(flowables)

elements = []

# ==========================================
# 1. EXAM HEADER PANEL (Page 1)
# ==========================================
header_data = [
    [Paragraph("<b>EMo Learners</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.HexColor('#0D9488')))],
    [Paragraph("<b>PROFESSIONAL QUESTION BANK</b>", ParagraphStyle('HSub', fontName=font_name_bold, fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>Analysis and Design of Algorithms (ADA)</b>", ParagraphStyle('HSub2', fontName=font_name_bold, fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1F2937')))],
    [Paragraph("<b>Unit 1 &amp; Unit 2 Objective Questions</b>", ParagraphStyle('HDesc', fontName=font_name_bold, fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor('#4B5563')))]
]

header_table = Table(header_data, colWidths=[515])
header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
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
        Paragraph("<b>Subject:</b> Analysis and Design of Algorithms", normal_style),
        Paragraph("<b>Total Questions:</b> 24", normal_style)
    ],
    [
        Paragraph("<b>Scope:</b> Unit 1 (Complexity Analysis, Sorting, Searching, Divide-and-Conquer) &amp; Unit 2 (Greedy Approach)", normal_style),
        Paragraph("<b>Document Status:</b> Verified Question Bank", normal_style)
    ]
]
info_table = Table(info_data, colWidths=[360, 155])
info_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('LINEBELOW', (0, 1), (-1, 1), 0.75, colors.HexColor('#E2E8F0')),
]))
elements.append(info_table)
elements.append(Spacer(1, 10))

# ==========================================
# 3. SECTION HEADER
# ==========================================
elements.append(make_section_banner("Unit 1 & Unit 2: Core Algorithm Design & Analysis MCQs"))

# ==========================================
# 4. QUESTION LIST DATA (Parsed with Unicode and clean tags)
# ==========================================
questions_data = [
    {
        "num": "1.",
        "text": "What is the worst-case time for merge sort to sort an array of <i>n</i> elements?",
        "options": ["<i>O</i>(log <i>n</i>)", "<i>O</i>(<i>n</i>)", "<i>O</i>(<i>n</i> log <i>n</i>)", "<i>O</i>(<i>n</i><sup>2</sup>)"],
        "answer": "C. <i>O</i>(<i>n</i> log <i>n</i>)",
        "solution": "Merge sort consistently divides the array in half and merges them, taking <i>O</i>(<i>n</i> log <i>n</i>) time in all cases."
    },
    {
        "num": "2.",
        "text": "What is the worst-case time for quick sort to sort an array of <i>n</i> elements?",
        "options": ["<i>O</i>(log <i>n</i>)", "<i>O</i>(<i>n</i>)", "<i>O</i>(<i>n</i> log <i>n</i>)", "<i>O</i>(<i>n</i><sup>2</sup>)"],
        "answer": "D. <i>O</i>(<i>n</i><sup>2</sup>)",
        "solution": "This occurs when the array is already sorted and the smallest or largest element is consistently chosen as the pivot."
    },
    {
        "num": "3.",
        "text": "In a selection sort of <i>n</i> elements, how many times is the swap function called in the complete execution of the algorithm?",
        "options": ["1", "<i>n</i> - 1", "<i>n</i> log <i>n</i>", "<i>n</i><sup>2</sup>"],
        "answer": "B. <i>n</i> - 1",
        "solution": "Selection sort makes exactly one swap for each position in the array as it builds the sorted portion."
    },
    {
        "num": "4.",
        "text": "Selection sort and quick sort both fall into the same category of sorting algorithms. What is this category?",
        "options": ["<i>O</i>(<i>n</i> log <i>n</i>) sorts", "Divide-and-conquer sorts", "Interchange sorts", "Average time is quadratic"],
        "answer": "C. Interchange sorts",
        "solution": "Both algorithms fundamentally rely on swapping or interchanging elements based on comparisons to arrange them."
    },
    {
        "num": "5.",
        "text": "What is the Best-case time for Binary Search to sort an array of <i>n</i> elements? (Note: Binary Search is a searching algorithm)",
        "options": ["<i>O</i>(log <i>n</i>)", "<i>O</i>(1)", "<i>O</i>(<i>n</i> log <i>n</i>)", "<i>O</i>(<i>n</i><sup>2</sup>)"],
        "answer": "B. <i>O</i>(1)",
        "solution": "The best case occurs when the middle element of the array is the exact target element on the very first comparison."
    },
    {
        "num": "6.",
        "text": "Consider the following array - 23, 32, 45, 69, 72, 73, 89, 97. Which algorithm out of the following options uses the least number of comparisons (among the array elements) to sort the above array in ascending order?",
        "options": ["Selection Sort", "Merge Sort", "Insertion Sort", "Quick Sort"],
        "answer": "C. Insertion Sort",
        "solution": "The given array is already sorted. Insertion sort takes <i>O</i>(<i>n</i>) comparisons for an already sorted array, which is the minimum among the options."
    },
    {
        "num": "7.",
        "text": "The Master Theorem (Main Recurrence Theorem)",
        "options": [
            "is used to prove correctness of algorithms", 
            "gives general solutions to time recurrences for divide-and-conquer algorithms", 
            "gives intractability results", 
            "is proven by temporal logic"
        ],
        "answer": "B. gives general solutions to time recurrences for divide-and-conquer algorithms",
        "solution": "The Master Theorem provides a cookbook method for solving recurrences of the form <i>T</i>(<i>n</i>) = <i>aT</i>(<i>n</i>/<i>b</i>) + <i>f</i>(<i>n</i>) arising in divide-and-conquer algorithms."
    },
    {
        "num": "8.",
        "text": "Knapsack is a(n) ____ problem.",
        "options": ["non-optimization vector, matrix or graph", "optimization", "state-space search", "behavior-of-program"],
        "answer": "B. optimization",
        "solution": "The goal is to maximize profit/value while keeping the total weight under a specific capacity."
    },
    {
        "num": "9.",
        "text": "The binary search uses which approach to algorithm design?",
        "options": ["divide and conquer", "greedy", "brute force", "dynamic programming"],
        "answer": "A. divide and conquer",
        "solution": "It repeatedly divides the search interval in half."
    },
    {
        "num": "10.",
        "text": "Graph path search involves finding a:",
        "options": ["set of vertices", "sequence of vertices", "set of edges", "minimal set of edges"],
        "answer": "B. sequence of vertices",
        "solution": "A path in a graph is defined as an ordered sequence of vertices connected by edges."
    },
    {
        "num": "11.",
        "text": "What is the time complexity of Huffman Coding?",
        "options": ["<i>O</i>(log <i>n</i>)", "<i>O</i>(<i>n</i>)", "<i>O</i>(<i>n</i> log <i>n</i>)", "<i>O</i>(<i>n</i><sup>2</sup>)"],
        "answer": "C. <i>O</i>(<i>n</i> log <i>n</i>)",
        "solution": "Building the initial min-heap takes <i>O</i>(<i>n</i>), and extracting the two minimum elements <i>n</i> - 1 times takes <i>O</i>(<i>n</i> log <i>n</i>)."
    },
    {
        "num": "12.",
        "text": "Consider a job scheduling problem with 4 jobs J<sub>1</sub>, J<sub>2</sub>, J<sub>3</sub>, J<sub>4</sub> and with corresponding deadlines: (<i>d</i><sub>1</sub>, <i>d</i><sub>2</sub>, <i>d</i><sub>3</sub>, <i>d</i><sub>4</sub>) = (4, 2, 4, 2). Which of the following is not a feasible schedule without violating any job schedule?",
        "options": [
            "J<sub>3</sub>, J<sub>2</sub>, J<sub>1</sub>, J<sub>4</sub>", 
            "J<sub>4</sub>, J<sub>1</sub>, J<sub>2</sub>, J<sub>3</sub>", 
            "J<sub>4</sub>, J<sub>2</sub>, J<sub>1</sub>, J<sub>3</sub>", 
            "J<sub>2</sub>, J<sub>4</sub>, J<sub>1</sub>, J<sub>3</sub>"
        ],
        "answer": "A. J<sub>3</sub>, J<sub>2</sub>, J<sub>1</sub>, J<sub>4</sub>",
        "solution": "In option A, Job J<sub>4</sub> is executed in the 4th time slot, but its deadline is 2. Therefore, it violates the deadline constraint."
    },
    {
        "num": "13.",
        "text": "Which asymptotic notation is used to represent the lower bound of an algorithm's running time?",
        "options": ["Big-Oh (<i>O</i>)", "Big-Omega (Ω)", "Theta (Θ)", "Little-oh (<i>o</i>)"],
        "answer": "B. Big-Omega (Ω)",
        "solution": "It provides the minimum time an algorithm will take for large inputs (asymptotically tight lower bound)."
    },
    {
        "num": "14.",
        "text": "What is the time complexity of Strassen’s Matrix Multiplication algorithm?",
        "options": ["<i>O</i>(<i>n</i><sup>3</sup>)", "<i>O</i>(<i>n</i><sup>2</sup>)", "<i>O</i>(<i>n</i><sup>2.81</sup>)", "<i>O</i>(<i>n</i> log <i>n</i>)"],
        "answer": "C. <i>O</i>(<i>n</i><sup>2.81</sup>)",
        "solution": "Strassen's algorithm reduces the 8 recursive multiplications to 7, leading to a recurrence of <i>T</i>(<i>n</i>) = 7<i>T</i>(<i>n</i>/2) + <i>O</i>(<i>n</i><sup>2</sup>), which solves to <i>O</i>(<i>n</i><sup>log<sub>2</sub>7</sup>) ≈ <i>O</i>(<i>n</i><sup>2.81</sup>)."
    },
    {
        "num": "15.",
        "text": "Which of the following algorithmic strategies is best suited to solve the Fractional Knapsack problem optimally?",
        "options": ["Dynamic Programming", "Greedy Strategy", "Divide and Conquer", "Backtracking"],
        "answer": "B. Greedy Strategy",
        "solution": "Taking items sorted by the highest profit-to-weight ratio (value density) yields the optimal solution for the fractional version."
    },
    {
        "num": "16.",
        "text": "Which data structure is primarily utilized in Kruskal's algorithm to efficiently check for cycles in a graph?",
        "options": ["Min-Heap", "Queue", "Disjoint Set (Union-Find)", "Stack"],
        "answer": "C. Disjoint Set (Union-Find)",
        "solution": "It keeps track of the connected components and quickly verifies if adding an edge connects two already connected vertices."
    },
    {
        "num": "17.",
        "text": "What is the recurrence relation for the standard Merge Sort algorithm?",
        "options": [
            "<i>T</i>(<i>n</i>) = <i>T</i>(<i>n</i>/2) + <i>O</i>(1)", 
            "<i>T</i>(<i>n</i>) = 2<i>T</i>(<i>n</i>/2) + <i>O</i>(1)", 
            "<i>T</i>(<i>n</i>) = 2<i>T</i>(<i>n</i>/2) + <i>O</i>(<i>n</i>)", 
            "<i>T</i>(<i>n</i>) = <i>T</i>(<i>n</i> - 1) + <i>O</i>(<i>n</i>)"
        ],
        "answer": "C. <i>T</i>(<i>n</i>) = 2<i>T</i>(<i>n</i>/2) + <i>O</i>(<i>n</i>)",
        "solution": "The array is split into two halves of size <i>n</i>/2, and merging them takes linear <i>O</i>(<i>n</i>) time."
    },
    {
        "num": "18.",
        "text": "Which of the following sorting algorithms is considered \"stable\"?",
        "options": ["Quick Sort", "Heap Sort", "Selection Sort", "Merge Sort"],
        "answer": "D. Merge Sort",
        "solution": "A stable sort maintains the relative order of equal elements. Merge sort preserves this order during the merge phase."
    },
    {
        "num": "19.",
        "text": "Dijkstra’s Algorithm is used to solve which of the following problems?",
        "options": ["Minimum Spanning Tree", "Single-Source Shortest Path", "All-Pairs Shortest Path", "Maximum Flow"],
        "answer": "B. Single-Source Shortest Path",
        "solution": "It finds the shortest paths from one specific source vertex to all other vertices in a graph with non-negative edge weights."
    },
    {
        "num": "20.",
        "text": "If an algorithm has a time complexity of Θ(<i>n</i><sup>2</sup>), this implies that:",
        "options": [
            "Its worst-case is <i>O</i>(<i>n</i><sup>2</sup>) but best case could be <i>O</i>(<i>n</i>).", 
            "Its running time grows exactly quadratically for all cases.", 
            "Its running time is bounded both above and below by a quadratic function.", 
            "It is faster than an <i>O</i>(<i>n</i> log <i>n</i>) algorithm."
        ],
        "answer": "C. Its running time is bounded both above and below by a quadratic function.",
        "solution": "Theta notation (Θ) signifies an asymptotically tight bound, meaning the upper and lower bounds grow at the same rate."
    },
    {
        "num": "21.",
        "text": "In Prim’s Algorithm for finding a Minimum Spanning Tree, which data structure is optimal for selecting the next edge with the minimum weight?",
        "options": ["Priority Queue (Min-Heap)", "Stack", "Hash Table", "Linked List"],
        "answer": "A. Priority Queue (Min-Heap)",
        "solution": "It efficiently allows extraction of the minimum edge weight connecting the current tree to unvisited vertices in <i>O</i>(log <i>V</i>) time."
    },
    {
        "num": "22.",
        "text": "According to the Master Theorem, if <i>T</i>(<i>n</i>) = <i>aT</i>(<i>n</i>/<i>b</i>) + <i>f</i>(<i>n</i>) and <i>f</i>(<i>n</i>) = <i>O</i>(<i>n</i><sup><i>c</i></sup>) where <i>c</i> &lt; log<sub><i>b</i></sub><i>a</i>, then the time complexity is:",
        "options": ["Θ(<i>f</i>(<i>n</i>))", "Θ(<i>n</i><sup>log<sub><i>b</i></sub><i>a</i></sup>)", "Θ(<i>n</i><sup><i>c</i></sup> log <i>n</i>)", "Θ(<i>n</i> log <i>n</i>)"],
        "answer": "B. Θ(<i>n</i><sup>log<sub><i>b</i></sub><i>a</i></sup>)",
        "solution": "This is Case 1 of the Master Theorem, where the work at the leaves of the recursion tree dominates the total work."
    },
    {
        "num": "23.",
        "text": "What type of tree is constructed during the generation of Huffman Codes?",
        "options": ["Binary Search Tree", "AVL Tree", "Full Binary Prefix Tree", "B-Tree"],
        "answer": "C. Full Binary Prefix Tree",
        "solution": "Huffman coding builds a binary tree from the bottom up where all characters are leaves, ensuring no code is a prefix of another."
    },
    {
        "num": "24.",
        "text": "The optimal binary merge pattern problem can be efficiently solved using which approach?",
        "options": ["Divide and Conquer", "Greedy Strategy", "Dynamic Programming", "Backtracking"],
        "answer": "B. Greedy Strategy",
        "solution": "By always choosing to merge the two smallest files first, usually implemented with a min-heap, we achieve the optimal merging cost."
    }
]

# Generate MCQ flowables
for q in questions_data:
    opt_table = make_options_table(q["options"][0], q["options"][1], q["options"][2], q["options"][3], normal_style)
    sol_box = make_solution_box(q["answer"], q["solution"])
    question_flowable = make_question(q["num"], q["text"], opt_table, sol_box)
    elements.append(question_flowable)

# Build Document using NumberedCanvas for dynamic footer
doc.build(elements, canvasmaker=NumberedCanvas)

print(f"PDF generated successfully: {pdf_path}")
