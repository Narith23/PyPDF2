import logging, fitz


def get_form_field_positions(target_pdf, data_dict: dict) -> dict:
    try:
        # Open the PDF file
        doc = fitz.open(target_pdf)
        # Iterate over each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_height = page.rect.height  # Get the height of the page

            # Get the form fields (widgets) on the page
            for field in page.widgets():
                rect = field.rect  # This gives you the position of the field
                name = field.field_name  # This gives you the name of the field

                # Check if the field name is in the data_dict
                if name in data_dict:
                    # Convert PyMuPDF coordinates to Adobe Acrobat coordinates
                    top = page_height - rect.y1
                    bottom = page_height - rect.y0
                    left = rect.x0
                    right = rect.x1

                    data_dict[name]["position"] = dict(
                        page=page_num, top=top, bottom=bottom, left=left, right=right, width=right - left, height=bottom - top
                    )
        return data_dict
    except Exception as e:
        logging.exception("An error occurred while getting form field positions.")
