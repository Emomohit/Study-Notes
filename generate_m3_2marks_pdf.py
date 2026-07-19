import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'ariali.ttf'))
font_name = "Arial"
font_name_bold = "Arial-Bold"
font_name_italic = "Arial-Italic"

class NumberedCanvas(canvas.Canvas):
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
        
        # Header (page 2 and later)
        if self._pageNumber > 1:
            self.setFont(font_name_bold, 8)
            self.setFillColor(colors.HexColor('#1E3A8A'))
            self.drawString(40, 805, "EMo Learners")
            self.setFont(font_name, 8)
            self.setFillColor(colors.HexColor('#4B5563'))
            self.drawString(100, 805, " |   Mathematics-3 (M3) MST-2: TOP 15 — 2 MARKS")
            
            self.setStrokeColor(colors.HexColor('#E5E7EB'))
            self.setLineWidth(0.5)
            self.line(40, 797, 555, 797)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor('#E5E7EB'))
        self.setLineWidth(0.75)
        self.line(40, 45, 555, 45)
        
        self.setFont(font_name, 8.5)
        self.setFillColor(colors.HexColor('#4B5563'))
        self.drawString(40, 30, "Document Exclusively Curated by ")
        
        self.setFont(font_name_bold, 8.5)
        self.setFillColor(colors.HexColor('#0D9488'))
        self.drawString(178, 30, "EMo Learners")
        
        self.setFont(font_name, 8.5)
        self.setFillColor(colors.HexColor('#4B5563'))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_text)
        
        self.restoreState()

pdf_path = "M3_TOP_15_2_Marks_MST2.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=60,
    bottomMargin=60
)

styles = getSampleStyleSheet()

normal_style = ParagraphStyle(
    'NormalStyle', fontName=font_name, fontSize=10, leading=17, textColor=colors.HexColor('#1F2937'), spaceBefore=5, spaceAfter=5
)
bold_style = ParagraphStyle(
    'BoldStyle', fontName=font_name_bold, fontSize=10, leading=17, textColor=colors.HexColor('#1F2937'), spaceBefore=5, spaceAfter=5
)
section_header_style = ParagraphStyle(
    'SectionHeaderStyle', fontName=font_name_bold, fontSize=11.5, leading=15, textColor=colors.white, keepWithNext=True
)

def make_section_banner(title_text):
    banner_table = Table([[Paragraph(title_text, section_header_style)]], colWidths=[515])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1E3A8A')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return KeepTogether([Spacer(1, 10), banner_table, Spacer(1, 8)])

def make_q_block(num_str, q_text, ans_lines, tags=""):
    flowables = []
    
    q_para = Paragraph(f"<b>{num_str}</b> {q_text} <font color='#888888'><i>{tags}</i></font>", ParagraphStyle('QText', parent=normal_style, fontName=font_name_bold, textColor=colors.HexColor('#1E3A8A')))
    flowables.append(q_para)
    
    for line in ans_lines:
        ans_para = Paragraph(line, ParagraphStyle('AnsText', parent=normal_style, leftIndent=15, textColor=colors.HexColor('#2D3748')))
        flowables.append(ans_para)
    
    flowables.append(Spacer(1, 12))
    return [KeepTogether(flowables)]

elements = []

# Title Panel
header_data = [
    [Paragraph("<b><font color='#0D9488'>EMo Learners</font> &nbsp;|&nbsp; Premium Short Answer Bank</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=16, leading=22, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>MATHEMATICS-3 (M3) MST-2: TOP 15 — 2 MARKS</b>", ParagraphStyle('HSub', fontName=font_name_bold, fontSize=11.5, leading=16, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
]

header_table = Table(header_data, colWidths=[515])
header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#0D9488')),
]))
elements.append(header_table)
elements.append(Spacer(1, 15))


# UNIT 3
elements.append(make_section_banner("Unit 3 — Numerical Methods (4 Qs)"))

elements.extend(make_q_block("1.", "State the RK-4 formula for dy/dx = f(x,y)", [
    "<b>Answer:</b>",
    "y<sub>n+1</sub> = y<sub>n</sub> + (1/6) (k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)",
    "Where:",
    "&bull; k<sub>1</sub> = h f(x<sub>n</sub>, y<sub>n</sub>)",
    "&bull; k<sub>2</sub> = h f(x<sub>n</sub> + h/2, y<sub>n</sub> + k<sub>1</sub>/2)",
    "&bull; k<sub>3</sub> = h f(x<sub>n</sub> + h/2, y<sub>n</sub> + k<sub>2</sub>/2)",
    "&bull; k<sub>4</sub> = h f(x<sub>n</sub> + h, y<sub>n</sub> + k<sub>3</sub>)"
], "— Pure recall, foundation for every Unit 3 Part-C question. High."))

elements.extend(make_q_block("2.", "Write Milne's Predictor and Corrector formulas", [
    "<b>Answer:</b>",
    "<b>Predictor Formula:</b>",
    "y<sub>n+1</sub><sup>(P)</sup> = y<sub>n-3</sub> + (4h/3) [ 2f<sub>n-2</sub> - f<sub>n-1</sub> + 2f<sub>n</sub> ]",
    "<b>Corrector Formula:</b>",
    "y<sub>n+1</sub><sup>(C)</sup> = y<sub>n-1</sub> + (h/3) [ f<sub>n-1</sub> + 4f<sub>n</sub> + f<sub>n+1</sub><sup>(P)</sup> ]"
], "— Matches Question Bank 'state predictor-corrector' style Q. High."))

elements.extend(make_q_block("3.", "Write Euler's Modified Method iterative formula", [
    "<b>Answer:</b>",
    "y<sub>n+1</sub><sup>(k+1)</sup> = y<sub>n</sub> + (h/2) [ f(x<sub>n</sub>, y<sub>n</sub>) + f(x<sub>n+1</sub>, y<sub>n+1</sub><sup>(k)</sup>) ]"
], "— Directly needed to attempt Euler's Modified numericals. Medium-High."))

elements.extend(make_q_block("4.", "State the Adams-Bashforth predictor formula", [
    "<b>Answer:</b>",
    "y<sub>n+1</sub><sup>(P)</sup> = y<sub>n</sub> + (h/24) [ 55f<sub>n</sub> - 59f<sub>n-1</sub> + 37f<sub>n-2</sub> - 9f<sub>n-3</sub> ]"
], "— Less repeated than Milne's/RK4 in PYQs but still asked. Medium."))


# UNIT 4
elements.append(make_section_banner("Unit 4 — Transform Calculus (Laplace &amp; Fourier) (6 Qs)"))

elements.extend(make_q_block("5.", "State and explain the Convolution Theorem", [
    "<b>Answer:</b>",
    "If L<sup>-1</sup>{F(s)} = f(t) and L<sup>-1</sup>{G(s)} = g(t), then:",
    "L<sup>-1</sup>{F(s)G(s)} = &int;<sub>0</sub><sup>t</sup> f(u) g(t - u) du = f * g"
], "— ★ Very High — repeated across PYQ 2023/2024/2025"))

elements.extend(make_q_block("6.", "Find L{t<sup>2</sup>e<sup>-3t</sup>}", [
    "<b>Answer:</b>",
    "We know that L{t<sup>2</sup>} = 2! / s<sup>3</sup> = 2 / s<sup>3</sup>",
    "By the First Shifting Theorem, L{e<sup>at</sup>f(t)} = F(s - a). Here, a = -3.",
    "Therefore, L{t<sup>2</sup>e<sup>-3t</sup>} = 2 / (s + 3)<sup>3</sup>"
], "— ★ Very High — exact match PYQ June 2023"))

elements.extend(make_q_block("7.", "Find L<sup>-1</sup>{ 1 / (1+s)<sup>3</sup> }", [
    "<b>Answer:</b>",
    "We know that L<sup>-1</sup>{1 / s<sup>3</sup>} = t<sup>2</sup> / 2! = t<sup>2</sup> / 2",
    "By the First Shifting Theorem in inverse form, L<sup>-1</sup>{F(s - a)} = e<sup>at</sup> f(t). Here, a = -1.",
    "Therefore, L<sup>-1</sup>{ 1 / (s + 1)<sup>3</sup> } = (1/2) t<sup>2</sup> e<sup>-t</sup>"
], "— ★ Very High — exact match PYQ June 2023"))

elements.extend(make_q_block("8.", "State First and Second Shifting Theorems", [
    "<b>Answer:</b>",
    "<b>First Shifting Theorem:</b>",
    "If L{f(t)} = F(s), then L{e<sup>at</sup>f(t)} = F(s - a)",
    "<b>Second Shifting Theorem:</b>",
    "If L{f(t)} = F(s), then L{f(t - a)u(t - a)} = e<sup>-as</sup> F(s)"
], "— Foundational; used implicitly in almost every Part C Laplace question. High."))

elements.extend(make_q_block("9.", "Find L{t cos(at)}", [
    "<b>Answer:</b>",
    "Using the property L{t f(t)} = -d/ds F(s):",
    "L{cos(at)} = s / (s<sup>2</sup> + a<sup>2</sup>)",
    "L{t cos(at)} = -d/ds [ s / (s<sup>2</sup> + a<sup>2</sup>) ]",
    "= - [ (s<sup>2</sup> + a<sup>2</sup>)(1) - s(2s) ] / (s<sup>2</sup> + a<sup>2</sup>)<sup>2</sup>",
    "= (s<sup>2</sup> - a<sup>2</sup>) / (s<sup>2</sup> + a<sup>2</sup>)<sup>2</sup>"
], "— High — PYQ June 2023"))

elements.extend(make_q_block("10.", "Find the Fourier Sine Transform of f(x) = 1/x", [
    "<b>Answer:</b>",
    "F<sub>s</sub>{1/x} = &int;<sub>0</sub><sup>&infin;</sup> f(x) sin(sx) dx = &int;<sub>0</sub><sup>&infin;</sup> (sin(sx) / x) dx",
    "Using the standard Dirichlet integral result:",
    "F<sub>s</sub>{1/x} = &pi;/2"
], "— Standard Dirichlet-integral type. Medium."))


# UNIT 5
elements.append(make_section_banner("Unit 5 — Concept of Probability &amp; Statistics (5 Qs)"))

elements.extend(make_q_block("11.", "Find c for f(x) = cx<sup>2</sup>, 0 &lt; x &lt; 1 as a valid PDF", [
    "<b>Answer:</b>",
    "For a valid PDF, the total area under the curve must be 1.",
    "&int;<sub>0</sub><sup>1</sup> cx<sup>2</sup> dx = 1",
    "c [ x<sup>3</sup> / 3 ]<sub>0</sub><sup>1</sup> = 1",
    "c (1/3 - 0) = 1 &rArr; c / 3 = 1 &rArr; <b>c = 3</b>"
], "— ★ Very High — exact match PYQ Dec 2025 + Question Bank"))

elements.extend(make_q_block("12.", "State four properties of the Normal Distribution curve", [
    "<b>Answer:</b>",
    "&bull; It is bell-shaped and perfectly symmetrical about its mean (&mu;).",
    "&bull; The Mean, Median, and Mode are all equal and located at the center of the distribution.",
    "&bull; The curve is asymptotic to the horizontal x-axis (it approaches but never touches it).",
    "&bull; The total area under the probability density curve is equal to 1."
], "— High"))

elements.extend(make_q_block("13.", "Write short note on Exponential Distribution — PDF and Mean", [
    "<b>Answer:</b>",
    "The Exponential Distribution is a continuous probability distribution often used to model waiting times or lifetimes.",
    "<b>Probability Density Function (PDF):</b> f(x) = &lambda;e<sup>-&lambda;x</sup> for x &ge; 0",
    "<b>Theoretical Mean (Expected Value):</b> Mean = 1 / &lambda;"
], "— ★ Very High"))

elements.extend(make_q_block("14.", "Poisson distribution: If P(X=1) = P(X=2), find the mean &lambda;", [
    "<b>Answer:</b>",
    "The Poisson probability formula is P(X=k) = (e<sup>-&lambda;</sup> &lambda;<sup>k</sup>) / k!",
    "Given P(X=1) = P(X=2):",
    "(e<sup>-&lambda;</sup> &lambda;<sup>1</sup>) / 1! = (e<sup>-&lambda;</sup> &lambda;<sup>2</sup>) / 2!",
    "&lambda; = &lambda;<sup>2</sup> / 2 &rArr; &lambda;<sup>2</sup> - 2&lambda; = 0",
    "Since &lambda; > 0, we have <b>&lambda; = 2</b>. Thus, the mean is 2."
], "— Medium-High — clean, fast numeric type"))

elements.extend(make_q_block("15.", "Binomial distribution: Mean = 4, Variance = 3, find n and p", [
    "<b>Answer:</b>",
    "For a Binomial distribution B(n, p):",
    "Mean = np = 4",
    "Variance = npq = 3",
    "We know that q = Variance / Mean = 3 / 4 = 0.75",
    "Since p + q = 1, p = 1 - 0.75 = 0.25",
    "Substitute p into Mean: n(0.25) = 4 &rArr; <b>n = 16</b>"
], "— Medium-High — same family as the 7-mark 9P(X=4)=P(X=2) type, good 2-mark variant"))


doc.build(elements, canvasmaker=NumberedCanvas)
print(f"PDF generated successfully: {pdf_path}")
