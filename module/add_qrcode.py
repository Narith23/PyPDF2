import logging
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

from helper.new_name import generate_new_name


def add_image_to_pdf(target_pdf, position) -> str:
    try:
        # Passwords
        user_password = "viewpassword"  # Password required to open the document
        owner_password = "editpassword"  # Password required for editing the document

        # Parameter
        new_name = generate_new_name()
        output_pdf = os.path.join("Files/Pre", f"{new_name}.pdf")
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

        qr_code_path = "Files/QrCode/QrCode.png"

        # Read the existing PDF
        existing_pdf = PdfReader(target_pdf)
        output = PdfWriter()

        # Iterate over all pages in the existing PDF
        for page_number in range(len(existing_pdf.pages)):
            # Use 'mediabox' to get page dimensions
            page_width = float(existing_pdf.pages[page_number].mediabox[2])
            page_height = float(existing_pdf.pages[page_number].mediabox[3])

            # Create a new PDF in memory for the current page
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))

            # Define the position and size for the QR code
            desired_qr_width = 60  # desired width of the QR code in points
            desired_qr_height = 60  # desired height of the QR code in points

            if (
                "ImageQRCode_af_image" in position
                and "position" in position["ImageQRCode_af_image"]
            ):
                desired_qr_width = float(
                    position["ImageQRCode_af_image"]["position"]["width"]
                )
                desired_qr_height = float(
                    position["ImageQRCode_af_image"]["position"]["height"]
                )
                page_width = float(position["ImageQRCode_af_image"]["position"]["left"])
                page_height = float(position["ImageQRCode_af_image"]["position"]["top"])
            else:
                page_width = page_width - desired_qr_width - 15
                page_height = page_height - desired_qr_height - 15

            # Draw the QR code image on the canvas without cropping
            can.drawImage(
                qr_code_path,
                page_width,
                page_height,
                width=desired_qr_width,
                height=desired_qr_height,
            )
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)

            # Read the created PDF
            new_pdf = PdfReader(packet)

            # Get the current page from the original PDF
            page = existing_pdf.pages[page_number]

            # Merge the new PDF with the current page of the existing PDF
            page.merge_page(new_pdf.pages[0])

            # Add the modified page to the output writer
            output.add_page(page)

            # output.encrypt(
            #     user_password, 
            #     owner_password, 
            #     use_128bit=True # 128-bit encryption
            # )

        # Write the modified PDF to the output file
        with open(output_pdf, "wb") as outputStream:
            output.write(outputStream)

        return output_pdf

    except Exception as e:
        logging.exception(e)
        return None
