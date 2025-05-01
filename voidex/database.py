from pathlib import Path
import shutil
from typing import Any, Self, Dict, Optional, List, Union, ClassVar
import hashlib

from pydantic import BaseModel, ConfigDict, model_validator, ValidationError


# HACK: DATA_DIR is forced to be local for now

# from voidex.paths import DATA_DIR
from voidex.paths import APP_DIR

DATA_DIR = APP_DIR.parent / "data"

# Storage Paths
PDF_DIR = DATA_DIR / "pdfs"
MD_DIR = DATA_DIR / "mds"

# Create PDF storage if not present
PDF_DIR.mkdir(exist_ok=True)

# If MD storage present, delete
if MD_DIR.exists():
    shutil.rmtree(MD_DIR, ignore_errors=True)

# Create/recreate MD storage
MD_DIR.mkdir(exist_ok=True)

# PDF-Markdown mapping
pdf_to_md: dict[str, tuple[Path, Path]] = {}

# Add to mapping
for pdf_path in PDF_DIR.glob("*.pdf"):

    # Get name
    name = pdf_path.name[:-4]

    # Create Markdown path
    md_path = MD_DIR / f"{name}.md"

    # Add entry
    pdf_to_md[name] = (pdf_path, md_path)


def convert_pdfs_to_mds(overwrite: bool = False):
    import pymupdf4llm

    print(f"Converting {len(pdf_to_md)} PDFs to MDs...")
    print(f"Allow overwrite: {overwrite}")
    successes = fails = skips = 0
    indent = " " * 2
    # For each pdf, create a markdown file
    for name, values in pdf_to_md.items():
        print(f"Processing `{name}.pdf`:")
        pdf_path, md_path = values

        # Handle if file exists
        if overwrite:
            print(indent + "MD file exists. Overwriting...")
        elif md_path.exists():
            print(indent + "MD file exists. Skipping...")
            skips += 1
            continue
        else:
            print(indent + "MD file missing. Creating...")

        # Try and convert PDF to MD
        try:
            # Open and convert
            print(indent + "Converting PDF to MD text... ", end="")
            md_text = pymupdf4llm.to_markdown(pdf_path)
            print("Success.")

            # Write MD text to file
            print(indent + f"Writing MD text to `{name}`.md... ", end="")
            md_path.write_bytes(md_text.encode())
            print("Success.")
            successes += 1

        except Exception as _:
            # Failed to convert or write to file
            print("Failed.")
            fails += 1

    print(f"Completed {successes + fails + skips} files.")
    print(indent + f"{successes} successes")
    print(indent + f"{fails} failures")
    print(indent + f"{skips} skips")


if __name__ == "__main__":
    print(f"Contents of {PDF_DIR}:\n{list(map(str, PDF_DIR.iterdir()))}\n")
    print(f"Contents of {MD_DIR}:\n{list(map(str, MD_DIR.iterdir()))}\n")
    [
        print(f"Name: {name}\nPDF: {paths[0]}\nMD: {paths[1]}\n\n")
        for name, paths in pdf_to_md.items()
    ]

    convert_pdfs_to_mds()
