# ============================================
# AYANFE AI V2 — FILE & IMAGE SYSTEM
# ============================================

from pathlib import Path
import shutil


# Use the deployed AYANFE project directory.
# This works on Streamlit Cloud and local deployment.
PROJECT = Path(__file__).resolve().parent

UPLOAD_DIR = PROJECT / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".mp4",
    ".mov",
    ".webm"
}


def save_uploaded_file(file_path):

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

    shutil.copy2(
        source,
        destination
    )

    return {
        "success": True,
        "filename": source.name,
        "path": str(destination),
        "extension": extension
    }


def extract_pdf_text(file_path):

    from pypdf import PdfReader

    reader = PdfReader(
        str(file_path)
    )

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)


def extract_docx_text(file_path):

    from docx import Document

    document = Document(
        str(file_path)
    )

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


def extract_text_file(file_path):

    return Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )


def extract_text(file_path):

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

    extension = Path(
        file_path
    ).suffix.lower()

    return extension in {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    }


def is_video(file_path):

    extension = Path(
        file_path
    ).suffix.lower()

    return extension in {
        ".mp4",
        ".mov",
        ".webm"
    }


def get_file_info(file_path):

    path = Path(file_path)

    return {
        "filename": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "is_image": is_image(path),
        "is_video": is_video(path)
    }
