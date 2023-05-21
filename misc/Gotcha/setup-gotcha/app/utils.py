from random import uniform
from io import BytesIO
from PIL import Image, ImageDraw
from base64 import b64encode

letter_set = "ABCDEFGHIKLMNOPQRSTVWXYZ"

def generate_captcha() -> str:
    """Generate captcha"""
    return "".join([letter_set[int(uniform(0, len(letter_set)))] for _ in range(4)])


def draw_captcha(text: str) -> Image:
    """Draw the captcha on the image"""
    interleaf = [l + " " for l in text]
    img = Image.new("RGB", (100, 30), color=(255, 255, 255))
    txt = ImageDraw.Draw(img)
    txt.text((5, 5), ''.join(interleaf).strip(), fill=(0, 0, 0))
    return img.resize((200, 60))


def convert_img_to_b64(img: Image) -> str:
    """Transform image to base64"""
    buffered_io = BytesIO()
    img.save(buffered_io, format="PNG")
    return b64encode(buffered_io.getvalue()).decode()
