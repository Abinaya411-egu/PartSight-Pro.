"""Image validation, conversion, and overlay helpers."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Optional, Union

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_FORMATS = {"JPEG", "PNG"}
MAX_IMAGE_BYTES = 20 * 1024 * 1024


class ImageValidationError(ValueError):
    """Raised when an uploaded image cannot be used for inspection."""


def filename_extension(filename: str) -> str:
    return Path(filename or "").suffix.lower()


def is_allowed_filename(filename: str) -> bool:
    return filename_extension(filename) in ALLOWED_EXTENSIONS


def load_image_bytes(source: Union[bytes, bytearray, BytesIO, Any]) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if hasattr(source, "getvalue"):
        return source.getvalue()
    if hasattr(source, "read"):
        data = source.read()
        if hasattr(source, "seek"):
            try:
                source.seek(0)
            except Exception:
                pass
        return data
    raise ImageValidationError("Unsupported image input. Provide image bytes or a file-like object.")


def validate_image(
    source: Union[bytes, bytearray, BytesIO, Any],
    filename: str = "upload.jpg",
) -> Image.Image:
    if not is_allowed_filename(filename):
        raise ImageValidationError(
            f"Unsupported file type '{filename}'. Upload a JPG, JPEG, or PNG image."
        )

    raw = load_image_bytes(source)
    if not raw:
        raise ImageValidationError("The uploaded file is empty.")
    if len(raw) > MAX_IMAGE_BYTES:
        raise ImageValidationError("The uploaded image exceeds the 20 MB limit.")

    try:
        image = Image.open(BytesIO(raw))
        image.load()
    except UnidentifiedImageError as exc:
        raise ImageValidationError("The file is not a valid image or is corrupted.") from exc
    except OSError as exc:
        raise ImageValidationError(f"The image could not be opened: {exc}") from exc

    if image.format not in ALLOWED_FORMATS:
        raise ImageValidationError(
            f"Image format '{image.format}' is not supported. Use JPG, JPEG, or PNG."
        )
    return image


def to_rgb(image: Image.Image) -> Image.Image:
    if image.mode == "RGB":
        return image.copy()
    if image.mode in {"RGBA", "LA", "P"}:
        background = Image.new("RGB", image.size, (255, 255, 255))
        converted = image.convert("RGBA")
        background.paste(converted, mask=converted.split()[-1])
        return background
    return image.convert("RGB")


def image_to_jpeg_bytes(image: Image.Image) -> bytes:
    rgb = to_rgb(image)
    buffer = BytesIO()
    rgb.save(buffer, format="JPEG", quality=95)
    return buffer.getvalue()


def parse_bbox(bbox: Any) -> Optional[list[int]]:
    if bbox is None:
        return None
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        return None
    try:
        x1, y1, x2, y2 = (int(round(float(v))) for v in bbox)
    except (TypeError, ValueError):
        return None
    if x2 <= x1 or y2 <= y1:
        return None
    return [x1, y1, x2, y2]


def clamp_bbox(bbox: list[int], width: int, height: int) -> Optional[list[int]]:
    x1, y1, x2, y2 = bbox
    x1 = max(0, min(width - 1, x1))
    y1 = max(0, min(height - 1, y1))
    x2 = max(0, min(width, x2))
    y2 = max(0, min(height, y2))
    if x2 <= x1 or y2 <= y1:
        return None
    return [x1, y1, x2, y2]


def draw_predictions(
    image: Image.Image,
    predictions: list[dict[str, Any]],
) -> Image.Image:
    """Return a copy of the image with valid bounding boxes drawn on it."""
    annotated = to_rgb(image)
    draw = ImageDraw.Draw(annotated)
    width, height = annotated.size
    line = max(2, width // 220)
    try:
        font = ImageFont.load_default()
    except OSError:
        font = None

    for index, pred in enumerate(predictions, start=1):
        bbox = parse_bbox(pred.get("bbox"))
        if bbox is None:
            continue
        bbox = clamp_bbox(bbox, width, height)
        if bbox is None:
            continue
        x1, y1, x2, y2 = bbox
        draw.rectangle([x1, y1, x2, y2], outline="#E74C3C", width=line)
        class_name = str(pred.get("class_name") or f"det-{index}")
        try:
            confidence = float(pred.get("confidence"))
            label = f"{class_name} {confidence:.2f}"
        except (TypeError, ValueError):
            label = class_name
        text_box = draw.textbbox((x1, y1), label, font=font)
        text_height = text_box[3] - text_box[1]
        label_top = max(0, y1 - text_height - 4)
        draw.rectangle(
            [x1, label_top, x1 + (text_box[2] - text_box[0]) + 8, label_top + text_height + 4],
            fill="#E74C3C",
        )
        draw.text((x1 + 4, label_top + 2), label, fill="#FFFFFF", font=font)
    return annotated
