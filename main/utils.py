import os
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from django.conf import settings

def generate_bed_booking_receipt_pdf(booking):
    """
    Generates a professional PDF receipt for bed booking.
    """
    pdf_filename = f"BedBooking_{booking.booking_id}_{booking.student.first_name.replace(' ', '_')}_receipt.pdf"
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(name='CenteredTitle', parent=styles['Title'], alignment=TA_CENTER, fontSize=16))
    styles.add(ParagraphStyle(name='CenteredSubtitle', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='CenteredInfo', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, textColor=colors.darkgray))

    elements = []

    # Add logo
    logo_path = os.path.join(settings.MEDIA_ROOT, 'mut_logo.png')
    if os.path.exists(logo_path):
        try:
            logo = RLImage(logo_path, width=2 * inch, height=2 * inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 12))
        except Exception as e:
            print(f"Error loading logo: {e}")

    # Add receipt header
    elements.append(Paragraph("Bed Booking Receipt", styles['CenteredTitle']))
    elements.append(Spacer(1, 12))

    # Booking details
    details_table_data = [
        ['Booking ID', f"# {booking.booking_id}"],
        ['Student Name', f"{booking.student.first_name} {booking.student.last_name}"],
        ['Registration Number', booking.registration_number],
        ['Email', booking.student.email],
        ['Hostel', booking.hostel.name],
        ['Room', booking.room.room_number], 
        ['Bed Number', booking.bed.bed_number],
        ['Amount Paid', f"KSH {booking.amount}"],
    ]

    table = Table(details_table_data, colWidths=[2 * inch, 4 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add QR code
    qr_code = qr.QrCodeWidget(f"Booking ID: {booking.booking_id} | Student: {booking.student.first_name} | Hostel: {booking.hostel.name}")
    qr_drawing = Drawing(2 * inch, 2 * inch)
    qr_drawing.add(qr_code)
    elements.append(qr_drawing)
    elements.append(Spacer(1, 12))

    # Footer
    elements.append(Paragraph("Thank you for booking with us!", styles['CenteredInfo']))
    elements.append(Spacer(1, 12))

    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer, pdf_filename

def send_bed_booking_receipt_email(booking):
    """
    Sends an email with the generated bed booking receipt PDF.
    """
    pdf_buffer, pdf_filename = generate_bed_booking_receipt_pdf(booking)

    subject = f"Booking Confirmation - {booking.hostel.name}"
    message = f"""
    Dear {booking.student.first_name} {booking.student.last_name},

    Thank you for booking a bed in {booking.hostel.name}.
    Please find your receipt attached to this email.

    Booking Details:
    - Booking ID: {booking.booking_id}
    - Hostel: {booking.hostel.name}
    - Room No: { booking.room.room_number }
    - Bed No: {booking.bed.bed_number}
    - Amount Paid: KSH {booking.amount}

    If you have any questions, feel free to contact us.

    Best regards,
    The Hostel Management Team
    """

    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email]
    )
    email.attach(pdf_filename, pdf_buffer.read(), 'application/pdf')
    email.send()
