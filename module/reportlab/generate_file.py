import os

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from helper.new_name import generate_new_name


def generate_new_file(file_size: dict | str) -> str:
    new_name = generate_new_name() + ".pdf"
    new_name_file = os.path.join("Files/Pre", new_name)
    os.makedirs(os.path.dirname(new_name_file), exist_ok=True)

    c = canvas.Canvas(new_name_file, pagesize=A4)
    width, height = A4  # Dimensions for A4 size
    width = int(width)
    height = int(height)

    # Title Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "# 910 : Testing audit log")

    # Document type and status
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, "Document type: FreeForm - Normal")

    # Creator and Created Date
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 90, "duch dinarith (Creator)")
    c.drawString(50, height - 110, "Created since: 11 Sep 2024, 05:06 PM")

    # Approval Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 140, "Approvals")

    # Line for separation
    c.line(50, height - 145, width - 50, height - 145)

    # Approval Steps
    approvers = [
        ("Mr. Chea Socheat", "Head of Billing & Software Development", "", "Pending"),
        (
            "Ms. Sea Kunthea",
            "Billing Operation Officer - 11 Sep 2024, 05:06 PM",
            "Billing Operation Officer - 11 Sep 2024, 05:06 PM",
            "Rejected",
        ),
        (
            "Ms. Men Phalla",
            "Deputy Billing & Software Develop Manager - 11 Sep 2024, 05:10 PM",
            "",
            "Approved",
        ),
    ]

    y_position = height - 170
    for approver, title, comment, status in approvers:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(70, y_position, approver)
        c.setFont("Helvetica", 8)
        c.drawString(70, y_position - 15, title)
        c.drawString(70, y_position - 25, f"Comment: {comment}")
        c.setFont("Helvetica", 8)

        if status == "Approved":
            c.setFillColor(colors.green)
            c.drawImage(
                "Files/Images/Approved.png",
                width - 140,
                y_position - 5,
                width=70,
                height=17,
            )
        elif status == "Rejected":
            c.setFillColor(colors.red)
            c.drawImage(
                "Files/Images/Rejected.png",
                width - 140,
                y_position - 5,
                width=70,
                height=17,
            )
        else:
            c.setFillColor(colors.grey)
        # c.drawString(width - 100, y_position - 5, status)

        c.setFillColor(colors.black)

        # Draw circle for status
        c.circle(55, y_position - 5, 5, fill=0)
        y_position -= 40

    # Comments Section
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_position - 20, "Comments")
    c.setFont("Helvetica", 8)
    c.drawString(50, y_position - 40, "string")

    # Save the PDF
    c.save()

    return new_name_file
