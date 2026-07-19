import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
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
        
        # Header (only draw on page 2 and later)
        if self._pageNumber > 1:
            self.setFont(font_name_bold, 8)
            self.setFillColor(colors.HexColor('#1E3A8A'))
            self.drawString(40, 805, "EMo Learners")
            self.setFont(font_name, 8)
            self.setFillColor(colors.HexColor('#4B5563'))
            self.drawString(100, 805, " |   Mathematics-3 (M3) MST-2 Objective Question Bank")
            
            # Header line
            self.setStrokeColor(colors.HexColor('#E5E7EB'))
            self.setLineWidth(0.5)
            self.line(40, 797, 555, 797)
            
        # Footer (draw on all pages)
        self.setStrokeColor(colors.HexColor('#E5E7EB'))
        self.setLineWidth(0.75)
        self.line(40, 45, 555, 45)
        
        # Footer left text
        self.setFont(font_name, 8.5)
        self.setFillColor(colors.HexColor('#4B5563'))
        self.drawString(40, 30, "Document Exclusively Curated by ")
        
        # Highlight "EMo Learners" in bold teal
        self.setFont(font_name_bold, 8.5)
        self.setFillColor(colors.HexColor('#0D9488'))
        self.drawString(178, 30, "EMo Learners")
        
        # Footer right text
        self.setFont(font_name, 8.5)
        self.setFillColor(colors.HexColor('#4B5563'))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_text)
        
        self.restoreState()

pdf_path = "M3_IMp_objective_MST2.pdf"

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
    'NormalStyle', fontName=font_name, fontSize=9.5, leading=16.5, textColor=colors.HexColor('#1F2937'), spaceBefore=5, spaceAfter=5
)
bold_style = ParagraphStyle(
    'BoldStyle', fontName=font_name_bold, fontSize=9.5, leading=16.5, textColor=colors.HexColor('#1F2937'), spaceBefore=5, spaceAfter=5
)
section_header_style = ParagraphStyle(
    'SectionHeaderStyle', fontName=font_name_bold, fontSize=10.5, leading=14, textColor=colors.white, keepWithNext=True
)

def make_section_banner(title_text):
    banner_table = Table([[Paragraph(title_text, section_header_style)]], colWidths=[515])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1E3A8A')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return KeepTogether([Spacer(1, 10), banner_table, Spacer(1, 8)])

def make_mcq(num_str, q_text, options, ans_text, exp_text):
    flowables = []
    
    q_para = Paragraph(f"<b>{num_str}</b> {q_text}", ParagraphStyle('QText', parent=normal_style, fontName=font_name_bold, textColor=colors.HexColor('#1E3A8A')))
    flowables.append(q_para)
    
    for opt in options:
        opt_para = Paragraph(opt, ParagraphStyle('OptText', parent=normal_style, leftIndent=15))
        flowables.append(opt_para)
        
    ans_para = Paragraph(f"<b>Answer: {ans_text}</b>", ParagraphStyle('AnsText', parent=normal_style, fontName=font_name_bold, textColor=colors.HexColor('#0D9488'), spaceBefore=3))
    flowables.append(ans_para)
    
    exp_para = Paragraph(f"<i>Explanation: {exp_text}</i>", ParagraphStyle('ExpText', parent=normal_style, textColor=colors.HexColor('#4B5563'), spaceBefore=2))
    flowables.append(exp_para)
    
    flowables.append(Spacer(1, 12))
    return [KeepTogether(flowables)]

elements = []

# Header
header_data = [
    [Paragraph("<b><font color='#0D9488'>EMo Learners</font> &nbsp;|&nbsp; Premium Solved Question Bank</b>", ParagraphStyle('HBrand', fontName=font_name_bold, fontSize=15, leading=20, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>MATHEMATICS-3 (M3) MST-2 IMPORTANT OBJECTIVE QUESTIONS</b>", ParagraphStyle('HSub', fontName=font_name_bold, fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#1E3A8A')))],
    [Paragraph("<b>RGPV Syllabus Focus Pattern — Units 3, 4, &amp; 5</b>", ParagraphStyle('HSub2', fontName=font_name_bold, fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#1F2937')))],
]

header_table = Table(header_data, colWidths=[515])
header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#0D9488')),
]))
elements.append(header_table)
elements.append(Spacer(1, 15))


elements.append(make_section_banner("Unit 3: Numerical Methods \u2013 3 (Ordinary &amp; Partial Differential Equations)"))

elements.extend(make_mcq("1.", "The local truncation error of the Runge-Kutta 4th order (RK-4) method is of the order:", ["(a) O(h<sup>2</sup>)", "(b) O(h<sup>3</sup>)", "(c) O(h<sup>4</sup>)", "(d) O(h<sup>5</sup>)"], "(d) O(h<sup>5</sup>)", "The local truncation error per step is O(h<sup>5</sup>), while the overall global cumulative error across the interval is O(h<sup>4</sup>)."))

elements.extend(make_mcq("2.", "In Euler's basic method for solving dy/dx = f(x, y), the global order of convergence is:", ["(a) O(h)", "(b) O(h<sup>2</sup>)", "(c) O(h<sup>3</sup>)", "(d) O(h<sup>4</sup>)"], "(a) O(h)", "Euler's method is a first-order numerical method; it truncates Taylor series terms containing h<sup>2</sup> and higher."))

elements.extend(make_mcq("3.", "How many prior starting values are required to apply Milne's predictor-corrector method?", ["(a) 1", "(b) 2", "(c) 3", "(d) 4"], "(d) 4", "Milne's method requires four consecutive initial data points (y<sub>0</sub>, y<sub>1</sub>, y<sub>2</sub>, y<sub>3</sub>) to predict the fifth value y<sub>4</sub>."))

elements.extend(make_mcq("4.", "To generate the initial starting values required for Milne's or Adams-Bashforth predictor-corrector methods, which method is most commonly used?", ["(a) Bisection Method", "(b) Runge-Kutta 4th Order Method", "(c) Gauss Elimination Method", "(d) Simpson's Rule"], "(b) Runge-Kutta 4th Order Method", "Since predictor-corrector methods are not self-starting, high-accuracy single-step methods like RK-4 or Taylor series are used to compute the first few points."))

elements.extend(make_mcq("5.", "Euler's Modified method is geometrically derived based on which numerical integration rule?", ["(a) Rectangular Rule", "(b) Trapezoidal Rule", "(c) Simpson's 1/3 Rule", "(d) Simpson's 3/8 Rule"], "(b) Trapezoidal Rule", "It improves Euler's approximation by taking the average of the slopes at the beginning and the end of the interval (x<sub>n</sub>, x<sub>n+1</sub>)."))

elements.extend(make_mcq("6.", "In the Adams-Bashforth predictor formula, the polynomial interpolation is based on:", ["(a) Newton's Forward Difference Formula", "(b) Newton's Backward Difference Formula", "(c) Lagrange's Interpolation Formula", "(d) Stirling's Central Difference Formula"], "(b) Newton's Backward Difference Formula", "The method uses past computed derivative values (f<sub>n</sub>, f<sub>n-1</sub>, f<sub>n-2</sub>, f<sub>n-3</sub>), making backward differences the mathematical foundation."))

elements.extend(make_mcq("7.", "Which of the following numerical methods for differential equations is classified as a &quot;self-starting&quot; method?", ["(a) Milne's Predictor-Corrector Method", "(b) Adams-Bashforth Method", "(c) Adams-Moulton Method", "(d) Runge-Kutta Method"], "(d) Runge-Kutta Method", "Single-step methods like RK-4 only require the single immediate previous point (x<sub>n</sub>, y<sub>n</sub>) to compute the next step."))

elements.extend(make_mcq("8.", "In the Runge-Kutta 4th order method, the intermediate slope k<sub>2</sub> is evaluated at the coordinates:", ["(a) (x<sub>0</sub>, y<sub>0</sub>)", "(b) (x<sub>0</sub> + h, y<sub>0</sub> + k<sub>1</sub>)", "(c) (x<sub>0</sub> + h/2, y<sub>0</sub> + k<sub>1</sub>/2)", "(d) (x<sub>0</sub> + h/2, y<sub>0</sub> + k<sub>2</sub>/2)"], "(c) (x<sub>0</sub> + h/2, y<sub>0</sub> + k<sub>1</sub>/2)", "k<sub>2</sub> represents the estimate of the slope at the midpoint of the interval using the initial slope k<sub>1</sub>."))

elements.extend(make_mcq("9.", "In the Bender-Schmidt explicit finite difference method for the 1D heat equation &part;u/&part;t = c<sup>2</sup> &part;<sup>2</sup>u/&part;x<sup>2</sup>, the mesh ratio &alpha; = c<sup>2</sup>k/h<sup>2</sup> is chosen as:", ["(a) &alpha; = 1", "(b) &alpha; = 1/2", "(c) &alpha; = 1/4", "(d) &alpha; = 2"], "(b) &alpha; = 1/2", "Setting &alpha; = 0.5 eliminates the central temperature term u<sub>i</sub><sup>j</sup>, reducing the recurrence relation to the simple arithmetic mean of adjacent spatial points."))

elements.extend(make_mcq("10.", "The Crank-Nicholson method used for solving parabolic partial differential equations (heat equation) is classified as an:", ["(a) Explicit method with conditional stability", "(b) Implicit method with unconditional stability", "(c) Explicit method with unconditional stability", "(d) Implicit method with conditional stability"], "(b) Implicit method with unconditional stability", "It averages the spatial second derivatives at time levels j and j+1, resulting in a robust implicit system that converges for any mesh size ratio."))

elements.extend(make_mcq("11.", "The standard five-point finite difference approximation formula is primarily used to solve:", ["(a) Wave Equation", "(b) Heat Equation", "(c) Laplace and Poisson Equations", "(d) First-order ODEs"], "(c) Laplace and Poisson Equations", "It replaces &nabla;<sup>2</sup>u = 0 by relating the potential at a grid point (i, j) directly to its four immediate orthogonal neighbors."))

elements.extend(make_mcq("12.", "What is the sufficient mathematical condition for the convergence of the Taylor Series method for ODEs?", ["(a) The function f(x, y) must be continuous only", "(b) The function f(x, y) must be analytic (possess continuous derivatives of all orders)", "(c) The step size h must be greater than 1", "(d) The differential equation must be linear"], "(b) The function f(x, y) must be analytic", "Taylor series expansion requires evaluating higher-order analytical derivatives (y'', y''', y<sup>(4)</sup>, etc.) at the initial point."))

elements.extend(make_mcq("13.", "In finite difference methods for PDEs, the central difference approximation for the second derivative &part;<sup>2</sup>u/&part;x<sup>2</sup> has an error order of:", ["(a) O(h)", "(b) O(h<sup>2</sup>)", "(c) O(h<sup>3</sup>)", "(d) O(h<sup>4</sup>)"], "(b) O(h<sup>2</sup>)", "Central difference formulas cancel out odd-order error terms in the Taylor series expansion, yielding second-order spatial accuracy."))


elements.append(make_section_banner("Unit 4: Transform Calculus (Laplace &amp; Fourier Transforms)"))

elements.extend(make_mcq("14.", "The Laplace transform L{1} is equal to:", ["(a) 1", "(b) s", "(c) 1/s", "(d) 1/s<sup>2</sup>"], "(c) 1/s", "Evaluated via the definition &int;<sub>0</sub><sup>&infin;</sup> 1 &middot; e<sup>-st</sup>dt = [-e<sup>-st</sup>/s]<sub>0</sub><sup>&infin;</sup> = 1/s for s &gt; 0."))

elements.extend(make_mcq("15.", "The value of L{e<sup>at</sup>} is:", ["(a) 1/(s+a)", "(b) 1/(s-a)", "(c) a/(s<sup>2</sup>+a<sup>2</sup>)", "(d) s/(s<sup>2</sup>-a<sup>2</sup>)"], "(b) 1/(s-a)", "Direct integration of &int;<sub>0</sub><sup>&infin;</sup> e<sup>-(s-a)t</sup>dt converges to 1/(s-a) when s &gt; a."))

elements.extend(make_mcq("16.", "What is the Laplace transform of sin(at)?", ["(a) s/(s<sup>2</sup>+a<sup>2</sup>)", "(b) a/(s<sup>2</sup>+a<sup>2</sup>)", "(c) a/(s<sup>2</sup>-a<sup>2</sup>)", "(d) s/(s<sup>2</sup>-a<sup>2</sup>)"], "(b) a/(s<sup>2</sup>+a<sup>2</sup>)", "Standard elementary transform formula; remember that sine carries the constant a in the numerator, while cosine carries s."))

elements.extend(make_mcq("17.", "What is the Laplace transform of t<sup>n</sup> (where n is a positive integer)?", ["(a) n/s<sup>n</sup>", "(b) n!/s<sup>n</sup>", "(c) n!/s<sup>n+1</sup>", "(d) (n+1)!/s<sup>n</sup>"], "(c) n!/s<sup>n+1</sup>", "Derived using Gamma function integration &Gamma;(n+1) = n!."))

elements.extend(make_mcq("18.", "According to the First Shifting Theorem, if L{f(t)} = F(s), then L{e<sup>at</sup>f(t)} equals:", ["(a) F(s+a)", "(b) F(s-a)", "(c) e<sup>-as</sup>F(s)", "(d) aF(s)"], "(b) F(s-a)", "Multiplying by an exponential in the time domain translates (shifts) the function by a units in the frequency domain."))

elements.extend(make_mcq("19.", "If L{f(t)} = F(s), then the Laplace transform of the first derivative L{f'(t)} is:", ["(a) sF(s) - f(0)", "(b) sF(s) + f(0)", "(c) F(s)/s - f(0)", "(d) s<sup>2</sup>F(s) - sf(0)"], "(a) sF(s) - f(0)", "This fundamental operational property converts differential equations into algebraic equations."))

elements.extend(make_mcq("20.", "According to the Convolution Theorem, the inverse Laplace transform L<sup>-1</sup>{F(s)G(s)} is given by:", ["(a) f(t)g(t)", "(b) &int;<sub>0</sub><sup>&infin;</sup> f(u)g(t-u)du", "(c) &int;<sub>0</sub><sup>t</sup> f(u)g(t-u)du", "(d) &int;<sub>0</sub><sup>t</sup> f(u)g(u)du"], "(c) &int;<sub>0</sub><sup>t</sup> f(u)g(t-u)du", "The multiplication of two transforms in the s-domain corresponds strictly to the definite convolution integral over the interval [0, t] in the time domain."))

elements.extend(make_mcq("21.", "If L{f(t)} = F(s), then multiplication by time L{t &middot; f(t)} equals:", ["(a) d/ds F(s)", "(b) -d/ds F(s)", "(c) &int;<sub>s</sub><sup>&infin;</sup> F(u)du", "(d) -s &middot; F(s)"], "(b) -d/ds F(s)", "Differentiating the Laplace integral with respect to parameter s brings down a factor of -t."))

elements.extend(make_mcq("22.", "If L{f(t)} = F(s) and lim<sub>t &rarr; 0</sub> f(t)/t exists, then division by time L{f(t)/t} equals:", ["(a) -d/ds F(s)", "(b) &int;<sub>0</sub><sup>s</sup> F(u)du", "(c) &int;<sub>s</sub><sup>&infin;</sup> F(u)du", "(d) 1/s F(s)"], "(c) &int;<sub>s</sub><sup>&infin;</sup> F(u)du", "Division by t in the time domain corresponds to integration from s to infinity in the frequency domain."))

elements.extend(make_mcq("23.", "The Laplace transform of the Unit Step Function (Heaviside function) u(t-a) is:", ["(a) 1/(s-a)", "(b) e<sup>-as</sup>/s", "(c) e<sup>-as</sup>", "(d) e<sup>as</sup>/s"], "(b) e<sup>-as</sup>/s", "By definition, &int;<sub>a</sub><sup>&infin;</sup> 1 &middot; e<sup>-st</sup>dt = e<sup>-as</sup>/s, which serves as the building block for the Second Shifting Theorem."))

elements.extend(make_mcq("24.", "The Laplace transform of the Dirac Delta impulse function &delta;(t-a) is:", ["(a) 1", "(b) 1/s", "(c) e<sup>-as</sup>", "(d) e<sup>as</sup>"], "(c) e<sup>-as</sup>", "The sifting property of the impulse function evaluates the integrand e<sup>-st</sup> precisely at the spike location t=a."))

elements.extend(make_mcq("25.", "The inverse Laplace transform L<sup>-1</sup>{1/(s-a)<sup>2</sup>} is:", ["(a) e<sup>at</sup>", "(b) t e<sup>at</sup>", "(c) t<sup>2</sup> e<sup>at</sup> / 2", "(d) t e<sup>-at</sup>"], "(b) t e<sup>at</sup>", "Since L{t} = 1/s<sup>2</sup>, applying the First Shifting Theorem directly yields 1/(s-a)<sup>2</sup>."))

elements.extend(make_mcq("26.", "What is the value of the Fourier Sine Transform of f(x) = 1/x?", ["(a) 0", "(b) &pi;", "(c) &pi;/2", "(d) 1"], "(c) &pi;/2", "Evaluated using the standard Dirichlet integral &int;<sub>0</sub><sup>&infin;</sup> sin(sx)/x dx = &pi;/2 for all s &gt; 0."))

elements.extend(make_mcq("27.", "In Fourier Transform theory, the kernel for the Fourier Cosine Transform is:", ["(a) e<sup>-isx</sup>", "(b) sin(sx)", "(c) cos(sx)", "(d) e<sup>isx</sup>"], "(c) cos(sx)", "The cosine transform isolates the even-function symmetry over the positive real domain [0, &infin;)."))


elements.append(make_section_banner("Unit 5: Concept of Probability &amp; Statistics"))

elements.extend(make_mcq("28.", "For any valid continuous Probability Density Function (PDF) f(x) defined over (-&infin;, &infin;), the total integrated area under the curve must equal:", ["(a) 0", "(b) 0.5", "(c) 1", "(d) &infin;"], "(c) 1", "This represents the fundamental axiom of probability; the certainty of the sample space occurring is 100% or 1."))

elements.extend(make_mcq("29.", "In a Binomial Distribution B(n, p), the theoretical mean (expected value) is:", ["(a) npq", "(b) np", "(c) &radic;(npq)", "(d) p/n"], "(b) np", "The expected number of successes across n independent Bernoulli trials with success probability p is directly n &times; p."))

elements.extend(make_mcq("30.", "What is the variance of a Binomial Distribution B(n, p)?", ["(a) np", "(b) np<sup>2</sup>", "(c) npq", "(d) &radic;(npq)"], "(c) npq", "Where q = 1-p is the probability of failure. Note that for any binomial distribution, the variance is strictly less than the mean."))

elements.extend(make_mcq("31.", "Which of the following is the defining characteristic feature of a Poisson Distribution?", ["(a) Mean &gt; Variance", "(b) Mean &lt; Variance", "(c) Mean = Variance", "(d) Mean = Standard Deviation"], "(c) Mean = Variance", "In a Poisson process with parameter &lambda;, both the expected value and the variance are identically equal to &lambda;."))

elements.extend(make_mcq("32.", "If a random variable X follows a Poisson distribution such that P(X=1) = P(X=2), what is the value of the mean &lambda;?", ["(a) 1", "(b) 2", "(c) 0.5", "(d) 4"], "(b) 2", "Using the probability law (e<sup>-&lambda;</sup>&lambda;<sup>1</sup>)/1! = (e<sup>-&lambda;</sup>&lambda;<sup>2</sup>)/2! &rArr; &lambda; = &lambda;<sup>2</sup>/2 &rArr; &lambda; = 2."))

elements.extend(make_mcq("33.", "In a standard Normal Distribution curve, what percentage of the total data area falls within one standard deviation of the mean (&mu; - &sigma; to &mu; + &sigma;)?", ["(a) 50.00%", "(b) 68.26%", "(c) 95.44%", "(d) 99.73%"], "(b) 68.26%", "This is the empirical 68-95-99.7 rule for bell-shaped Gaussian distributions."))

elements.extend(make_mcq("34.", "What is the shape and geometric symmetry of a Normal Distribution curve?", ["(a) Rectangular and asymmetric", "(b) Bell-shaped and symmetric about the mean &mu;", "(c) Exponential and positively skewed", "(d) U-shaped and symmetric about the origin"], "(b) Bell-shaped and symmetric about the mean &mu;", "The curve is perfectly symmetrical, meaning the Mean, Median, and Mode all coincide at the peak &mu;."))

elements.extend(make_mcq("35.", "If a continuous random variable X follows an Exponential Distribution with parameter &lambda; &gt; 0, its probability density function for x &ge; 0 is:", ["(a) &lambda; e<sup>-&lambda;x</sup>", "(b) e<sup>-&lambda;x</sup>", "(c) (1/&lambda;) e<sup>-&lambda;x</sup>", "(d) &lambda;<sup>2</sup> e<sup>-&lambda;x</sup>"], "(a) &lambda; e<sup>-&lambda;x</sup>", "The parameter &lambda; must multiply the exponential term to ensure the total area under the curve integrates exactly to 1."))

elements.extend(make_mcq("36.", "What is the theoretical mean (expected value) of an Exponential Distribution with parameter &lambda;?", ["(a) &lambda;", "(b) &lambda;<sup>2</sup>", "(c) 1/&lambda;", "(d) 1/&lambda;<sup>2</sup>"], "(c) 1/&lambda;", "Evaluated via integration by parts: &int;<sub>0</sub><sup>&infin;</sup> x &middot; &lambda; e<sup>-&lambda;x</sup>dx = 1/&lambda;."))

elements.extend(make_mcq("37.", "Which continuous probability distribution is uniquely known for possessing the &quot;Memoryless Property&quot;?", ["(a) Normal Distribution", "(b) Binomial Distribution", "(c) Exponential Distribution", "(d) Uniform Distribution"], "(c) Exponential Distribution", "P(X &gt; s+t | X &gt; s) = P(X &gt; t), meaning the remaining waiting time is entirely independent of how much time has already elapsed."))

elements.extend(make_mcq("38.", "When a normal random variable X ~ N(&mu;, &sigma;<sup>2</sup>) is converted into the Standard Normal Variate Z = (X - &mu;)/&sigma;, what are the new mean and variance of Z?", ["(a) Mean = &mu;, Variance = &sigma;<sup>2</sup>", "(b) Mean = 1, Variance = 0", "(c) Mean = 0, Variance = 1", "(d) Mean = 0, Variance = &sigma;"], "(c) Mean = 0, Variance = 1", "Standardizing centers the distribution at origin zero and normalizes the spread to unit variance (Z ~ N(0, 1))."))

elements.extend(make_mcq("39.", "For any Binomial Distribution B(n, p), which mathematical inequality between Mean and Variance holds universally true?", ["(a) Mean &lt; Variance", "(b) Mean &gt; Variance", "(c) Mean = Variance", "(d) Mean &le; Variance"], "(b) Mean &gt; Variance", "Since Variance = Mean &times; q, and the failure probability q = (1-p) is strictly less than 1 (for 0 &lt; p &lt; 1), multiplying by q always reduces the value."))

elements.extend(make_mcq("40.", "If f(x) = k defined over the interval 0 &lt; x &lt; 5 is a valid probability density function of a uniform random variable, what must be the value of the constant k?", ["(a) 1", "(b) 5", "(c) 0.2", "(d) 0.5"], "(c) 0.2", "The total area of the rectangular distribution must be unity: &int;<sub>0</sub><sup>5</sup> k dx = 1 &rArr; 5k = 1 &rArr; k = 1/5 = 0.2."))

doc.build(elements, canvasmaker=NumberedCanvas)
print(f"PDF generated successfully: {pdf_path}")
