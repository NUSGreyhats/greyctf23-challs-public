import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO
import os
from base64 import b64decode


def b64_to_np_img(b64_img: str) -> np.array:
    """Convert a b64 image to np.array"""
    # Load b64 image into pillow
    b64_img = BytesIO(b64decode(b64_img))
    img = Image.open(b64_img)
    # Convert to np.array
    return img_to_np(img)


def img_to_np(img: Image.Image) -> np.array:
    """Convert an image to a numpy array"""
    return np.array(img)


def load_valid_faces():
    imgs = os.listdir("./auth_faces")
    acc = []
    for img in imgs:
        img = Image.open(f"./auth_faces/{img}")
        img = img_to_np(img)
        acc.extend(face_recognition.face_encodings(img))
    return acc


# Extract Faces
def extract_faces(b64_img: str) -> list:
    """Extract faces from the image"""
    # Convert the b64 image to a numpy array
    img = b64_to_np_img(b64_img)
    return extract_faces_np(img)


def extract_faces_np(img: np.array) -> list:
    """Extract faces from the image"""
    # Get the locations of the faces
    return face_recognition.face_encodings(img)
