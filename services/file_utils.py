from PIL import Image, ImageDraw
import io
import os

def detect_mode_from_filename(name: str) -> str:
    n = name.lower()
    if n.endswith((".pdf", ".png", ".jpg", ".jpeg")):
        return "2D"
    if n.endswith((".step", ".stp")):
        return "3D"
    return "2D"

def get_uploaded_bytes_and_name(uploaded_file):
    if uploaded_file is None:
        return None, None
    data = uploaded_file.getvalue()
    return data, uploaded_file.name

def load_image_from_bytes(file_bytes, file_name):
    if file_bytes is None or file_name is None:
        return Image.new("RGB", (1100, 650), color=(245, 245, 245))

    name = file_name.lower()

    if name.endswith((".png", ".jpg", ".jpeg")):
        return Image.open(io.BytesIO(file_bytes)).convert("RGB")

    if name.endswith(".pdf"):
        img = Image.new("RGB", (1100, 650), color=(245, 245, 245))
        d = ImageDraw.Draw(img)
        d.rectangle([20, 20, 1080, 630], outline=(60, 60, 60), width=3)
        d.text((40, 40), "2D preview (mock)", fill=(30, 30, 30))
        d.text((40, 70), "PDF rendering not added yet", fill=(80, 80, 80))
        d.text((40, 100), f"Uploaded: {file_name}", fill=(80, 80, 80))
        return img

    img = Image.new("RGB", (1100, 650), color=(245, 245, 245))
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, 1080, 630], outline=(60, 60, 60), width=3)
    d.text((40, 40), "2D preview (mock)", fill=(30, 30, 30))
    d.text((40, 70), f"Uploaded: {file_name}", fill=(80, 80, 80))
    return img

def load_mock_3d_image():
    path = os.path.join("assets", "mock_3d_preview.png")
    try:
        return Image.open(path).convert("RGB")
    except Exception:
        img = Image.new("RGB", (1100, 650), color=(245, 245, 245))
        d = ImageDraw.Draw(img)
        d.rectangle([20, 20, 1080, 630], outline=(60, 60, 60), width=3)
        d.text((40, 40), "3D preview (mock)", fill=(30, 30, 30))
        d.text((40, 70), "Missing assets/mock_3d_preview.png", fill=(80, 80, 80))
        return img
