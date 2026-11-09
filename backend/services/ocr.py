from pathlib import Path
import io
import os
import fitz
import pytesseract
from pytesseract import TesseractNotFoundError
from PIL import Image, ImageOps, ImageEnhance
from dotenv import load_dotenv

load_dotenv()

TESSERACT_CMD = os.getenv("TESSERACT_CMD")

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}

def _prepare_image(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("L")
    return ImageEnhance.Contrast(image).enhance(1.6)

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract English text from a supported image or PDF."""
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix or 'unknown'}")

    cmd = os.getenv("TESSERACT_CMD", "").strip()
    if cmd:
        pytesseract.pytesseract.tesseract_cmd = cmd

    chunks = []
    try:
        if suffix == ".pdf":
            document = fitz.open(stream=file_bytes, filetype="pdf")
            if document.is_encrypted:
                raise ValueError("Password-protected PDFs are not supported.")
            if len(document) > 30:
                raise ValueError("PDF exceeds the 30-page starter limit.")
            for page_number, page in enumerate(document, start=1):
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                text = pytesseract.image_to_string(_prepare_image(image), lang="eng")
                chunks.append(f"[Page {page_number}]\\n{text.strip()}")
        else:
            image = Image.open(io.BytesIO(file_bytes))
            chunks.append(pytesseract.image_to_string(_prepare_image(image), lang="eng").strip())
    except TesseractNotFoundError as exc:
        raise RuntimeError("Tesseract not found. Install it or set TESSERACT_CMD in .env.") from exc
    except (fitz.FileDataError, OSError) as exc:
        raise ValueError("Could not read file. Check that it is a valid PDF or image.") from exc

    result = "\\n\\n".join(part for part in chunks if part).strip()
    if not result:
        raise ValueError("OCR returned no text. Try a clearer, higher-resolution scan.")
    return result
