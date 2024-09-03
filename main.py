import os
from datetime import datetime

from module.pypdf2.add_qrcode import add_image_to_pdf
from module.pypdf2.add_text_and_image_to_pdf import add_text_and_image_to_pdf
from module.pypdf2.clear_form import clear_pdf_form
from module.pypdf2.metadata import get_metadata, update_pdf_metadata
from module.pypdf2.get_position import get_form_field_positions


# Metadata
metadata = dict()


def validate_pdf_file(file_path: str):
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Error: The file is not a PDF.")


def extract_form_field_positions(target_pdf: str, data_dict: dict, metadata: dict) -> str:
    # Validation file target_pdf
    if os.path.exists(target_pdf) is False:
        print(f"File not found: {target_pdf}")

    # Get File Name
    name = os.path.basename(target_pdf)
    if not name.lower().endswith(".pdf"):
        print("Error: The file is not a PDF.")

    # Step 1 - Get Metadata from PDF
    print("==========================================")
    print("Step 1 - Get Metadata from PDF")
    print("==========================================")
    print("")
    metadata_dict = get_metadata(target_pdf)
    if metadata_dict:
        metadata_dict.update(metadata)
        print("Done!", metadata_dict)
    else:
        metadata_dict = metadata
        print("Done!")
    print("")

    # Step 2 - Get positions fields from PDF
    print("==========================================")
    print("Step 2 - Get positions fields from PDF")
    print("==========================================")
    print("")
    get_positions = get_form_field_positions(target_pdf, data_dict)
    if get_positions:
        data_dict = get_positions
        print("Done!")
    print("")

    # Step 3 - Clear PDF form
    print("==========================================")
    print("Step 3 - Clear PDF form")
    print("==========================================")
    print("")
    clear_pdf = clear_pdf_form(target_pdf)
    if clear_pdf:
        # os.remove(target_pdf)
        target_pdf = clear_pdf
        print("Done!")
    else:
        print("Done!")
    print("")

    # Step 4 - Add QR Code to PDF
    print("==========================================")
    print("Step 4 - Add QR Code to PDF")
    print("==========================================")
    print("")
    add_qr_to_pdf = add_image_to_pdf(target_pdf, get_positions)
    if add_qr_to_pdf:
        os.remove(target_pdf)
        target_pdf = add_qr_to_pdf
        print("Done!")
    else:
        print("Done!")
    print("")

    # Step 5 - Add Text and Image to PDF
    print("==========================================")
    print("Step 5 - Add Text and Image to PDF")
    print("==========================================")
    print("")
    add_text_and_image = add_text_and_image_to_pdf(target_pdf, data_dict, metadata_dict)
    if add_text_and_image:
        os.remove(target_pdf)
        print("Done!")
    else:
        print("Done!")
    print("")

    return target_pdf


target_pdf = "Files/Library/1725346969_854488_E49C67.pdf"
data_dict = dict(
    Requestor=dict(value="John Doe", action=None),
    RequestorDate=dict(
        value=datetime.now().strftime("%d/%m/%Y %H:%M:%S %p"), action=None
    ),
)

metadata = dict(
    keywords=dict(
        doc_id=123,
        version=1.0,
    ),
    systemDocument=True,
)

extract_form_field_positions(target_pdf, data_dict, metadata)
