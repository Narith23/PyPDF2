from datetime import datetime
import uuid


def generate_new_name() -> str:
    # Generate new name file
    new_name_file = (
        str(round(datetime.now().timestamp()))
        + "_"
        + str(datetime.now().microsecond)
        + "_"
        + uuid.uuid4().hex[:6].upper()
    )
    return new_name_file
