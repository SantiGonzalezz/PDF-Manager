# ----------------------------
# Libraries
# ----------------------------

from pypdf import PdfReader, PdfWriter, PdfMerger


# Functions
def read_pdf(file_path: str) -> PdfReader:
    """
    Read a PDF from a file path and return the object to interact with
    """
    reader = PdfReader(file_path)

    return reader


def get_pdf_pages_number(reader: PdfReader) -> int:
    """
    Get the number of pages in the pdf
    """
    num_pages = len(reader.pages)

    return num_pages


def get_pdf_metadata(reader: PdfReader):
    """
    Return the dictionary like metadata of the pdf
    """
    metadata = reader.metadata

    return metadata


def extract_pdf_text(reader: PdfReader, start: int = 1, end: int = None) -> str:
    """
    Extract the text from the pdf and return it as a string
    """
    pages_number = get_pdf_pages_number(reader)

    if end is None:
        end = pages_number

    if not (start <= pages_number and end <= pages_number and start <= end):
        return Exception('There is an error in the start or end page')

    pages_text = []
    for page_num in range(start-1, end):
        page_text = reader.pages[page_num].extract_text()
        pages_text.append(page_text)

    return ' '.join(pages_text)


def split_pdf_custom_ranges(reader: PdfReader, start: int = 1, end: int = None):
    """
    Split the pdf from a start page parameter until an end page parameter and save it into a new file
    """
    pages_number = get_pdf_pages_number(reader)

    if end is None:
        end = pages_number

    if not (start <= pages_number and end <= pages_number and start <= end):
        return Exception('There is an error in the start or end page')

    filename = get_pdf_metadata(reader).title
    writer = PdfWriter()

    for page_num in range(start-1, end):
        page = reader.pages[page_num]
        writer.add_page(page)

    if filename is None:
        filename = 'output'

    new_filename = f'./Train/Output/{filename}_{start}_to_{end}.pdf'
    with open(new_filename, 'wb') as f:
        writer.write(f)


def split_pdf_fixed_ranges(reader: PdfReader, step: int = 1):
    """

    """