import logging, fitz


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