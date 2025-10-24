from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Image,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import uuid


def generate_authorisation_pdf(
    reappraisal_service_id, appraiser, branch, bank_name, director_name="Krishnaraj K"
):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=100,  # extra space for footer
    )
    PAGE_WIDTH, PAGE_HEIGHT = A4
    usable_width = PAGE_WIDTH - doc.leftMargin - doc.rightMargin
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    elements = []

    # --- generate unique Document ID (UUID) ---
    document_id = str(uuid.uuid4())
    # --- Logo (optional) ---
    logo_path = "assets/PhobosHeader.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=usable_width, height=0.8 * inch)
        elements.append(logo)
        elements.append(Spacer(1, 34))

    # --- Date ---
    today = datetime.today().strftime("%b %d, %Y")  # Add date and time
    elements.append(Paragraph(today, normal))
    elements.append(Spacer(1, 16))

    # --- Recipient ---
    elements.append(
        Paragraph(
            f"The Branch Manager,<br/><br/>{bank_name},<br/><br/>{branch['branch_name']}",
            normal,
        )
    )
    elements.append(Spacer(1, 34))

    # --- Body ---
    body_text = f"""
    Dear Sir/Madam,<br/><br/>
    Phobos Gold Technologies Pvt. Ltd., Bangalore, has been empaneled to provide the service of Gold Loan Re-appraisal for various branches of {bank_name}.<br/><br/>
    Phobos Gold, hereby authorizes <b>Mr.{appraiser['full_name']}</b> to do reappraisal of Gold at your branch.<br/><br/>
    KYC will be available with him for verification.<br/><br/>
    Kindly permit Mr. {appraiser['full_name']} to perform the gold reappraisal services.
    """
    elements.append(Paragraph(body_text, normal))
    elements.append(Spacer(1, 34))

    # --- Table ---
    data = [
        ["Name of Appraiser", "Aadhaar No.", "Pancard No.", "Contact No."],
        [
            appraiser["full_name"],
            appraiser["aadhaar"],
            appraiser["pan"],
            appraiser["phone"],
        ],
    ]

    table = Table(data, colWidths=[1.8 * inch, 1.8 * inch, 1.8 * inch, 1.8 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 34))

    # --- Signature ---
    elements.append(Paragraph("Thank you,", normal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Yours sincerely,", normal))
    elements.append(Spacer(1, 10))

    sig_path = "assets/signature.png"
    if os.path.exists(sig_path):
        signature = Image(sig_path, width=1.5 * inch, height=0.5 * inch)
        signature.hAlign = "LEFT"
        elements.append(signature)

    elements.append(Paragraph(f"<br/>{director_name}<br/><br/>Director", normal))

    # ---------------- Footer Function ----------------
    def draw_footer(canvas, doc):
        canvas.saveState()
        width, height = A4

        # --- Disclaimer ---
        disclaimer_style = ParagraphStyle(
            "Disclaimer", parent=normal, fontSize=8, textColor=colors.red, alignment=1
        )
        disclaimer_text = (
            "Disclaimer: This authorization letter is valid only until the completion of the specified re-appraisal. "
            "Any future re-appraisals will require a new authorization letter."
        )
        p = Paragraph(disclaimer_text, disclaimer_style)
        w, h = p.wrap(width - 80, 50)
        p.drawOn(canvas, 40, 100)

        # --- Line (above footer text) ---
        canvas.setStrokeColor(colors.darkgoldenrod)
        canvas.setLineWidth(1)
        canvas.line(40, 100, width - 40, 100)

        # --- Footer company info ---
        footer_text = f"""
        <b><font color="{colors.darkgoldenrod.hexval()}">PHOBOSGOLD TECHNOLOGIES PRIVATE LIMITED</font></b><br/>
        #202, 2nd floor, Anand chambers, no: 14/1, old(35/A), 14th cross (elephant rock road), Jayanagar 3rd block, Bangalore 560011,<br/>
        Mob: 7892851151.<br/>
        Mail: info@phobosgoldinc.com
        """
        footer_style = ParagraphStyle("Footer", parent=normal, fontSize=9, alignment=1)
        p = Paragraph(footer_text, footer_style)
        w, h = p.wrap(width - 80, 80)
        p.drawOn(canvas, 40, 50)

        # --- Metadata footer (tiny text, bottom of page) ---
        metadata_style = ParagraphStyle(
            "Metadata",
            parent=normal,
            fontSize=6,
            textColor=colors.grey,
            alignment=TA_CENTER,  # center text inside the paragraph
        )

        metadata_text = (
            f"This document was automatically generated by PhobosGold Technologies Private Limited, "
            f"on {datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p')} "
            f"to confirm the assignment of the above-named appraiser for appraisal/reappraisal services.<br/>"
            f"Assignment ID: {reappraisal_service_id} &nbsp;&nbsp; "
            f"Document ID: {document_id}"
        )

        p = Paragraph(metadata_text, metadata_style)

        # smaller available width so centering is visible
        available_width = width - 200
        w, h = p.wrap(available_width, 40)

        x = (width - w) / 2
        y = 10

        p.drawOn(canvas, x, y)

        canvas.restoreState()

    # Build PDF with footer
    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)

    buffer.seek(0)
    return buffer, document_id
