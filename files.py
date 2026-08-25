
# ============================================
# AYANFE AI V2 — FILE & IMAGE SYSTEM
# ============================================

from pathlib import Path
import shutil

PROJECT = Path("/content/drive/MyDrive/AYANFE_AI_V2")
UPLOAD_DIR = PROJECT / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}


def save_uploaded_file(file_path):
    """
    Save a file into AYANFE's permanent upload folder.
    """

    source = Path(file_path)

    if not source.exists():
        return {
            "success": False,
            "error": "File does not exist."
        }

    extension = source.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return {
            "success": False,
            "error": f"Unsupported file type: {extension}"
        }

    destination = UPLOAD_DIR / source.name

    shutil.copy2(source, destination)

    return {
        "success": True,
        "filename": source.name,
        "path": str(destination),
        "extension": extension
    }


def extract_pdf_text(file_path):
    """
    Extract text from a PDF.
    """

    from pypdf import PdfReader

    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)


def extract_docx_text(file_path):
    """
    Extract text from a DOCX document.
    """

    from docx import Document

    document = Document(str(file_path))

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


def extract_text_file(file_path):
    """
    Read a normal text file.
    """

    return Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )


def extract_text(file_path):
    """
    Automatically extract text from supported documents.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(path)

    if extension == ".docx":
        return extract_docx_text(path)

    if extension == ".txt":
        return extract_text_file(path)

    return None


def is_image(file_path):
    """
    Check whether a file is an image.
    """

    extension = Path(file_path).suffix.lower()

    return extension in {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    }


def get_file_info(file_path):
    """
    Return basic information about a file.
    """

    path = Path(file_path)

    return {
        "filename": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "is_image": is_image(path)
    }
