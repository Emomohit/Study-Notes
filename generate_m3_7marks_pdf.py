import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
            self.drawString(100, 805, " |   Mathematics-3 (M3) MST-2: TOP 13 — 7 MARKS")
            
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

pdf_path = "M3_TOP_13_7_Marks_MST2.pdf"

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
    [Paragraph("<b><font color='#0D9488'>EMo Learners</font> &nbsp;|&nbsp; Premium Descriptive Question Bank</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=16, leading=22, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>MATHEMATICS-3 (M3) MST-2: TOP 13 — 7 MARKS</b>", ParagraphStyle('HSub', fontName=font_name_bold, fontSize=11.5, leading=16, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
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

elements.extend(make_q_block("1.", "RK-4 Method — solve dy/dx = x+y (or similar), y(0)=1, find y(0.1)/y(0.2), h=0.1", [
    "<b>Also commonly asked as:</b> dy/dx = (y<sup>2</sup> - x<sup>2</sup>) / (y<sup>2</sup> + x<sup>2</sup>), y(0)=1, h=0.2",
    "<b>Scoring Breakdown:</b>",
    "&bull; State x<sub>0</sub>, y<sub>0</sub>, h, f(x,y) &rarr; compute k<sub>1</sub> (1 mark)",
    "&bull; Compute k<sub>2</sub>, k<sub>3</sub> (2.5 marks)",
    "&bull; Compute k<sub>4</sub> and final y<sub>n+1</sub> (3.5 marks)"
], "— P &approx; 95%"))

elements.extend(make_q_block("2.", "Milne's Predictor-Corrector Method", [
    "<b>Classic form:</b> dy/dx = x - y<sup>2</sup>, given y(0), y(0.1), y(0.2), y(0.3), find y(0.4)",
    "<b>Also seen as:</b> 5xy + y<sup>2</sup> - 2 = 0, y(4)=1, ... find y(4.4) (exact PYQ + QB match)",
    "<b>Scoring Breakdown:</b>",
    "&bull; Tabulate x<sub>n</sub>, y<sub>n</sub>, f<sub>n</sub>",
    "&bull; Predictor formula (label clearly) &rarr; predicted slope f<sub>4</sub><sup>(P)</sup>",
    "&bull; Corrector formula &rarr; final corrected value"
], "— P &approx; 95%"))

elements.extend(make_q_block("3.", "Euler's Modified Method (iterative convergence)", [
    "<b>Problem:</b> dy/dx = x+y, y(0)=1, find y(0.2), h=0.1 (or dy/dx = 1-y / x+siny variants)",
    "<b>Scoring Breakdown:</b>",
    "&bull; Predictor y<sub>1</sub><sup>(0)</sup>",
    "&bull; Iterate corrector until 2 consecutive values agree to 4 decimals",
    "&bull; Repeat same process for step 2 (to find y(0.2))"
], "— P &approx; 90%"))

elements.extend(make_q_block("4.", "Taylor's Series Method with exact-solution comparison", [
    "<b>Problem:</b> dy/dx = 2y + 3e<sup>x</sup>, y(0)=0, find y(0.2), compare with exact solution",
    "<b>Scoring Breakdown:</b>",
    "&bull; Differentiate successively for y'(0), y''(0), y'''(0), y<sup>(4)</sup>(0)",
    "&bull; Substitute in Taylor expansion",
    "&bull; Solve exact linear ODE (IF = e<sup>-2x</sup>)",
    "&bull; Compare, show error is negligible"
], "— P &approx; 85%"))


# UNIT 4
elements.append(make_section_banner("Unit 4 — Laplace &amp; Fourier Transforms (5 Qs)"))

elements.extend(make_q_block("5.", "Convolution Theorem — state, prove, and evaluate L<sup>-1</sup>{ s / (s<sup>2</sup>+a<sup>2</sup>)<sup>2</sup> }", [
    "<b>Scoring Breakdown:</b>",
    "&bull; State theorem (1 mark)",
    "&bull; Prove via double integral / change of variables (3 marks)",
    "&bull; Set F(s) = s/(s<sup>2</sup>+a<sup>2</sup>) &rarr; f(t) = cos(at), G(s) = 1/(s<sup>2</sup>+a<sup>2</sup>) &rarr; g(t) = (1/a)sin(at)",
    "&bull; Convolution integral with trig identity 2cosA sinB &rarr; evaluate to (t/2a)sin(at) (3 marks)"
], "— P &approx; 95%"))

elements.extend(make_q_block("6.", "Solve (D<sup>2</sup>+9)y = cos(2t), y(0)=1, y(&pi;/2)=-1 via Laplace", [
    "<b>Scoring Breakdown:</b>",
    "&bull; Take LT: [s<sup>2</sup>Y(s) - sy(0) - y'(0)] + 9Y(s) = s/(s<sup>2</sup>+4)",
    "&bull; Substitute y(0)=1, let y'(0)=c",
    "&bull; Partial fractions &rarr; invert",
    "&bull; Use t=&pi;/2, y=-1 to solve for c (= 12/5)"
], "— P &approx; 90%"))

elements.extend(make_q_block("7.", "L<sup>-1</sup>{ s / [ (s<sup>2</sup>+1)(s<sup>2</sup>+4) ] } via convolution", [
    "<b>Notes:</b> Same convolution-theorem family as Q5, but simpler denominator.",
    "Good backup/alternate question."
], "— P &approx; 85%"))

elements.extend(make_q_block("8.", "Evaluate &int;<sub>0</sub><sup>&infin;</sup> (cos(at) - cos(bt))/t dt OR &int;<sub>0</sub><sup>&infin;</sup> e<sup>-t</sup> sin<sup>2</sup>(t)/t dt (division-by-t property)", [
    "<b>Scoring Breakdown:</b>",
    "&bull; Write f(t) = sin<sup>2</sup>(t) = (1 - cos(2t))/2, find F(s)",
    "&bull; Apply L{f(t)/t} = &int;<sub>s</sub><sup>&infin;</sup> F(u) du",
    "&bull; Integrate/simplify to log form",
    "&bull; Substitute s=1 for final numeric answer (for the e<sup>-t</sup> case)"
], "— P &approx; 85%"))

elements.extend(make_q_block("9.", "Fourier Sine Transform of e<sup>-ax</sup>/x; deduce &int;<sub>0</sub><sup>&infin;</sup> (e<sup>-ax</sup> sin(sx))/x dx = tan<sup>-1</sup>(s/a)", [
    "<b>Scoring Breakdown:</b>",
    "&bull; Set up I(s), differentiate under integral sign (Leibniz)",
    "&bull; Standard exponential-cosine formula",
    "&bull; Integrate w.r.t. s",
    "&bull; Evaluate constant at s=0"
], "— P &approx; 80%"))


# UNIT 5
elements.append(make_section_banner("Unit 5 — Probability &amp; Statistics (4 Qs)"))

elements.extend(make_q_block("10.", "Fit Poisson Distribution: r: 0-4, f: 122, 60, 15, 2, 1 (e<sup>-0.5</sup> = 0.6065)", [
    "<b>Scoring Breakdown:</b>",
    "&bull; Create Table (x, f, fx) &rarr; N = 200, &Sigma;fx = 100",
    "&bull; Mean &lambda; = 100/200 = 0.5",
    "&bull; Calculate T(0) = 200 &times; e<sup>-0.5</sup> &approx; 121",
    "&bull; Use recurrence relation T(x+1) = T(x) &times; [&lambda; / (x+1)] for remaining values"
], "— P &approx; 95%"))

elements.extend(make_q_block("11.", "Derive Mean and Variance of Poisson Distribution (= &lambda; both)", [
    "<b>Scoring Breakdown:</b>",
    "&bull; Mean via E[X] = &Sigma; x&middot;P(x)",
    "&bull; Cancel x with x!, recognize e<sup>&lambda;</sup> series &rarr; &lambda;",
    "&bull; Variance via E[X(X-1)] + E[X] - (E[X])<sup>2</sup>",
    "&bull; &lambda;<sup>2</sup> + &lambda; - &lambda;<sup>2</sup> = &lambda;"
], "— P &approx; 85%"))

elements.extend(make_q_block("12.", "Given f(x) = cx<sup>2</sup>, 0 &lt; x &lt; 1 — find c, and P(1/3 &lt; X &lt; 1/2)", [
    "<b>Scoring Breakdown:</b>",
    "&bull; &int;<sub>0</sub><sup>1</sup> cx<sup>2</sup> dx = 1 &rarr; c = 3",
    "&bull; P = &int;<sub>1/3</sub><sup>1/2</sup> 3x<sup>2</sup> dx = [x<sup>3</sup>]",
    "&bull; Careful fraction arithmetic &rarr; (1/8) - (1/27) = 19/216 &approx; 0.088"
], "— P &approx; 85%"))

elements.extend(make_q_block("13.", "Normal Distribution: mean = 65.5\", SD = 6.2\", find % between 54.8\" and 68.8\"", [
    "<b>Scoring Breakdown:</b>",
    "&bull; Use Z = (X - &mu;) / &sigma; &rarr; Z<sub>1</sub> = -1.73, Z<sub>2</sub> = +0.53",
    "&bull; Split area across mean &rarr; sum table values (0.4582 + 0.2019)",
    "&bull; Total area = 0.6601 &rarr; 66.01%"
], "— P &approx; 85%"))

doc.build(elements, canvasmaker=NumberedCanvas)
print(f"PDF generated successfully: {pdf_path}")
