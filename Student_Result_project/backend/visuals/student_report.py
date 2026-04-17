import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pathlib
from models.paths import  pdf_dir, img_dir, logo_path
from io import BytesIO
from logger_config import get_logger

logger = get_logger(__name__)


def create_student_report(student):
    """
    Create a PDF report for a student in memory, return as bytes
    """
    buf = BytesIO()

    # Create PDF
    c = canvas.Canvas(buf, pagesize=letter)

    # Page Border
    c.setStrokeColor(colors.dodgerblue)
    c.setLineWidth(2)
    c.rect(30, 30, 552, 732) # Standard margin border

    # College Name / Header
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.dodgerblue)
    c.drawString(140, 730, "JSS ACADEMY OF TECHNICAL EDUCATION")
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawString(220, 715, "BENGALURU - 560060")
    
    # Header Line
    c.setStrokeColor(colors.dodgerblue)
    c.setLineWidth(1.5)
    c.line(50, 700, 560, 700)
    
    try:
        c.drawImage(logo_path, 50, 710, width=65, height=65)
    except Exception as e:
        logger.debug(f"Warning: Logo not loaded: {e}")

    # Student Info Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 675, "STUDENT PERFORMANCE REPORT")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 650, f"Name: {student.name}")
    c.drawString(50, 630, f"USN: {student.usn}")
    c.drawString(50, 610, f"Semester: {student.semester}")
    
    # Score Summary Box
    c.setFillColor(colors.aliceblue)
    c.rect(340, 600, 220, 70, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(350, 650, f"Total Marks: {student.total_marks}")
    c.drawString(350, 635, f"Percentage: {student.percentage:.2f}%")
    c.drawString(350, 620, f"SGPA: {student.sgpa:.2f}")
    c.drawString(450, 620, f"CGPA: {student.cgpa:.2f}")

    # Subject Table
    styles = getSampleStyleSheet()
    subject_style = styles["Normal"]
    subject_style.fontSize = 9
    
    header = ["#", "Subject Name & Code", "IA", "SEE", "Total", "Credits", "Status"]
    data = [header]
    
    for i, (subject_name, subject_code, ia, see, credit, status) in enumerate(
        zip(student.subject_names, student.subject_codes, student.ia_marks,
            student.see_marks, student.credits, student.pass_fail)
    ):
        subject_para = Paragraph(f"{subject_name} ({subject_code})", subject_style)
        data.append([
            str(i + 1),
            subject_para,
            str(ia),
            str(see),
            str(ia + see),
            str(credit),
            status
        ])

    # Define column widths
    col_widths = [25, 260, 35, 35, 40, 45, 65]
    
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'), # Left align subject names
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.aliceblue]),
    ]))

    # Calculate table height and draw
    width, height = letter
    w, h = table.wrapOn(c, width, height)
    # Position its top at ~555
    table.drawOn(c, 50, 555 - h)

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.line(50, 50, 560, 50)
    c.drawString(50, 40, "This is a computer-generated document. JSSATE Student Result Portal.")
    c.drawRightString(560, 40, f"USN: {student.usn} | Page 1")

    c.save()
    buf.seek(0)
    return buf.read()  # return PDF bytes