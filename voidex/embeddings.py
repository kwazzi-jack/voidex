from pathlib import Path
import pymupdf
import re
import csv
import os

from voidex.database import initialize_pdf_storage


# def pdfs_to_markdown()

# # Example usage
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv

#     load_dotenv()

#     pdfs = initialize_pdf_storage(os.getenv("PDF_DIR"))
#     print(f"{pdfs=}")

#     text = extract_text_from_pdf(pdfs["1101.1764.pdf"])
#     print(f"{text=}")
