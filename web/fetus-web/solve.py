import re
import requests

BASE_URL='http://34.124.157.94:12325'
Part1_regex = r'Flag part 1: (.*)-->'
Part2_regex = r'Flag part 2: (.*)'


with requests.Session() as s:
    resp = s.get(f"{BASE_URL}")
    p1 = re.findall(Part1_regex, resp.content.decode())
    flag = p1[0]

    resp2 = s.get(f"{BASE_URL}/assets/js/main.js")
    p2 = re.findall(Part2_regex, resp2.content.decode())
    flag += p2[0]

print("Flag:", flag)

