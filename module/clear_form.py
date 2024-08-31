import logging, os
from PyPDF2 import PdfReader, PdfWriter
from helper.new_name import generate_new_name


def clear_pdf_form(target_pdf: str) -> str:
    try:
        new_name = generate_new_name()
        output_pdf = os.path.join("Files/Pre", f"{new_name}.pdf")
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

        # Read the existing PDF
        reader = PdfReader(target_pdf)
        writer = PdfWriter()

        # Clear form fields by removing the /Annots key from each page
        for page in reader.pages:
            if "/Annots" in page:
                del page["/Annots"]  # Remove annotations including form fields
            writer.add_page(page)

        # Write the modified PDF to the output file
        with open(output_pdf, "wb") as outputStream:
            writer.write(outputStream)
        return output_pdf
    except Exception as e:
        logging.exception(e)
        return None
