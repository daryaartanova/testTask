import pdfplumber

def pdf_to_dict(file_path) -> dict:
    with pdfplumber.open(FILEPATH) as pdf:
        first_page = pdf.pages[0]
        text_lines = first_page.extract_text().split("\n")

    dict_output = {}
    skip_line = False

    for line_number in range(1, len(text_lines)):
        if skip_line == True:
            skip_line = False
            continue

        if text_lines[line_number].strip() == "":   # in case the line is empty
            continue

        line_parts = text_lines[line_number].split(":")
        key_1 = line_parts[0].strip()               # if line isn't empty it always starts with a key name

        if key_1.startswith("DESCRIPTION") or key_1.startswith("CERT SOURCE") or key_1.startswith('Qty'):
            value_1 = line_parts[1].strip()
            dict_output.update({key_1: value_1})
        elif key_1.startswith("TAGGED BY"):         # TAGGED BY is a barcode, but this line has another key - NOTES
            key_2 = line_parts[1].strip()
            value_2 = text_lines[line_number + 1].strip() # value for NOTES is in the next line
            skip_line = True                              # as we've already procecced the next line, we'll skip it
            dict_output.update({key_2: value_2})
        elif len(line_parts) == 3:                  # most lines satisfy this pattern
            if len(line_parts[1].split()) == 1:
                value_1 = ""
                key_2 = line_parts[1].strip()
            else:
                value_1, key_2 = [x.strip() for x in line_parts[1].split()]
            value_2 = line_parts[2].strip()
            dict_output.update({key_1: value_1})
            dict_output.update({key_2: value_2})
    return dict_output


FILEPATH = r"C:\Users\lilys\PycharmProjects\testTask\test_task.pdf"

parced_file = pdf_to_dict(FILEPATH)