import logging, fitz
import os

from helper.new_name import generate_new_name


def get_metadata(target_pdf: str) -> dict:
    try:
        # Open the PDF file
        doc = fitz.open(target_pdf)

        # Get the metadata
        metadata = doc.metadata
        return metadata
    except Exception as e:
        logging.exception("An error occurred while getting metadata.")
        return None


def update_pdf_metadata(target_pdf: str, metadata):
    try:
        # Open the existing PDF
        pdf_document = fitz.open(target_pdf)

        # Update the keywords
        existing_keywords = metadata.get("keywords", "")

        # Append the new keywords if existing keywords are present
        if existing_keywords:
            updated_keywords = "version +1.0"
        else:
            updated_keywords = "version 1.0"

        # Update the metadata dictionary
        metadata["keywords"] = updated_keywords

        # Set the updated metadata
        pdf_document.set_metadata(metadata)

        # Generate new name file
        new_name = generate_new_name()
        output_pdf = os.path.join("Files/Output", f"{new_name}.pdf")

        # Save the modified PDF to a new file
        pdf_document.save(output_pdf)

        # Close the PDF document
        pdf_document.close()

        return output_pdf
    except Exception as e:
        logging.exception("An error occurred while updating PDF metadata.")
        return None
