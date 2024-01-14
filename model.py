# ----------------------------
# Libraries
# ----------------------------

from pypdf import PdfReader, PdfWriter, PdfMerger
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


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
    Split the pdf using fixed ranges or steps, as every 2 pages split
    """
    pages_number = get_pdf_pages_number(reader)
    filename = get_pdf_metadata(reader).title

    for page_step in range(0, pages_number, step):

        writer = PdfWriter()

        for page_num in range(page_step, page_step+step):

            if page_num >= pages_number:
                break

            page = reader.pages[page_num]
            writer.add_page(page)

        if filename is None:
            filename = 'output'

        if page_num + 1 > pages_number:
            new_filename = f'./Train/Output/{filename}_{page_step+1}_to_{page_num}.pdf'
        else:
            new_filename = f'./Train/Output/{filename}_{page_step+1}_to_{page_num+1}.pdf'

        with open(new_filename, 'wb') as f:
            writer.write(f)


def split_pdf_select_pages(reader: PdfReader, pages: str, merge: bool = True):
    """

    """

    pages_list = pages.split(',')
    pages_set = set(pages_list)

    pages_number = get_pdf_pages_number(reader)
    filename = get_pdf_metadata(reader).title

    print(pages_set)

    if merge is True:

        writer = PdfWriter()
        for page_num in range(0, pages_number+1):
            if str(page_num) in pages_set:
                print(page_num)
                writer.add_page(reader.pages[page_num-1])

        if filename is None:
            filename = 'output'

        new_filename = f'./Train/Output/{filename}_pages.pdf'

        with open(new_filename, 'wb') as f:
            writer.write(f)

    else:
        for page_num in range(0, pages_number+1):
            if str(page_num) in pages_set:
                print(page_num)
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num-1])

                if filename is None:
                    filename = 'output'

                new_filename = f'./Train/Output/{filename}_{page_num}.pdf'

                with open(new_filename, 'wb') as f:
                    writer.write(f)


def to_zip_output_folder(zip_filename: str = 'output.zip', directory_to_zip: str = './Train/Output'):
    folder = Path(f'{directory_to_zip}')

    zip_path = f'./Train/Zip/{zip_filename}'

    for file in folder.iterdir():
        print(file.name)

    with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zip:
        for file in folder.iterdir():
            zip.write(file, arcname=file.name)
