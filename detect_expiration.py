import pytesseract
from PIL import Image
import re
from datetime import datetime, timedelta

def detect_expiration_date(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    # Regular expression to find date in format DD/MM/YYYY or similar
    date_match = re.search(r'(\d{2}/\d{2}/\d{4})|(\d{2}-\d{2}-\d{4})', text)
    if date_match:
        date_str = date_match.group()
        try:
            expiration_date = datetime.strptime(date_str, '%d/%m/%Y')
            return expiration_date
        except ValueError:
            try:
                expiration_date = datetime.strptime(date_str, '%d-%m-%Y')
                return expiration_date
            except ValueError:
                return None
    return None