from datetime import datetime
from io import BytesIO
import os
import random
import string
import uuid
import pikepdf
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from PyPDF2 import PdfReader, PdfWriter

from helper.config import FONT_LOCATION, IMAGE_APPROVE_PATH_FILE, IMAGE_REJECT_PATH_FILE


def add_text_and_image_to_pdf(target_pdf: str, data_dict: dict, metadata: dict):
    # Register the custom font
    custom_font_name = "KhmerOSBattambang"
    pdfmetrics.registerFont(TTFont(custom_font_name, FONT_LOCATION))

    # Validation file target_pdf
    if os.path.exists(target_pdf) is False:
        print(f"File not found: {target_pdf}")

    # Read the existing PDF
    existing_pdf = PdfReader(target_pdf)
    output = PdfWriter()

    # Iterate over all pages in the existing PDF
    for page_number in range(len(existing_pdf.pages)):
        # Use 'mediabox' to get page dimensions
        page_width = float(existing_pdf.pages[page_number].mediabox[2])
        page_height = float(existing_pdf.pages[page_number].mediabox[3])

        # Check if there's any data for the current page
        page_num = {
            key: value
            for key, value in data_dict.items()
            if "position" in value
            and "page" in value["position"]
            and value["position"]["page"] == page_number
        }

        if not page_num:
            # If no data is intended for this page, just add the original page to the output
            output.add_page(existing_pdf.pages[page_number])
            continue

        # Create a new PDF in memory for the current page
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        can.setFont("KhmerOSBattambang", 8)  # Set the font size to 8

        # Add text or images based on the data for this specific page
        for key, value in page_num.items():
            if "SignBy" in key:
                if value["position"]["left"] > 0 and value["position"]["top"] > 0:
                    can.drawImage(
                        (
                            IMAGE_APPROVE_PATH_FILE
                            if value["action"] == "approve"
                            else IMAGE_REJECT_PATH_FILE
                        ),
                        value["position"]["left"],
                        value["position"]["top"],
                        width=value["position"]["width"],
                        height=value["position"]["height"],
                    )
            else:
                if value["position"]["left"] > 0 and value["position"]["top"] > 0:
                    # Check text width
                    text_width = can.stringWidth(
                        value["value"], fontName="KhmerOSBattambang", fontSize=8
                    )

                    # Center the text
                    x = (
                        value["position"]["left"]
                        + (value["position"]["width"] - text_width) / 2
                    )
                    # Draw the text at the specified position
                    can.drawString(x, value["position"]["top"] + 5, value["value"])

        can.save()
        packet.seek(0)

        # Read the new PDF data
        new_pdf = PdfReader(packet)

        # Get the current page from the original PDF
        page = existing_pdf.pages[page_number]

        # Merge the new PDF with the current page of the existing PDF
        page.merge_page(new_pdf.pages[0])

        # Add the modified page to the output writer
        output.add_page(page)

        # Convert all metadata values to strings
        metadata = {key: str(value) for key, value in metadata.items()}

        # Add metadata to the output PDF
        output.add_metadata(metadata)

    # Make new name file
    extension = target_pdf.rsplit(".", 1)[-1]
    new_name_file = (
        str(round(datetime.now().timestamp()))
        + "_"
        + str(datetime.now().microsecond)
        + "_"
        + uuid.uuid4().hex[:6].upper()
        + "."
        + extension
    )
    new_file = os.path.join("Files/Pre", new_name_file)
    os.makedirs(os.path.dirname(new_file), exist_ok=True)

    # Write the modified PDF to the output file
    with open(new_file, "wb") as outputStream:
        output.write(outputStream)

    # Add Security to PDF File Use PIKEPDF
    new_name_file = (
        str(round(datetime.now().timestamp()))
        + "_"
        + str(datetime.now().microsecond)
        + "_"
        + uuid.uuid4().hex[:6].upper()
        + "."
        + extension
    )
    output_file = os.path.join("Files/Output", new_name_file)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Generate Strong Password
    user_password = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    print("User Password: ", user_password)
    owner_password = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    print("Owner Password: ", owner_password)

    # Open the PDF file
    with pikepdf.open(new_file) as file:
        # Set permissions using correct flags
        permissions = pikepdf.Permissions(
            accessibility=False,  # Disable text extraction for accessibility
            extract=False,  # Disable text and graphics extraction
            modify_annotation=False,  # Disable annotation modifications
            modify_assembly=False,  # Disable document assembly
            modify_form=False,  # Disable form modification
            print_lowres=False,  # Disable low-resolution printing
            print_highres=False,  # Disable high-resolution printing
        )

        # Encrypt the PDF with passwords and permissions
        file.save(
            output_file,
            encryption=pikepdf.Encryption(
                user=user_password, owner=owner_password, allow=permissions
            ),
        )
    os.remove(new_file)
    return output_file
