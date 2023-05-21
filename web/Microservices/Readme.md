# Microservices

### Challenge Details

I just learnt about microservices.
That means my internal server is safe now right?

I'm still making my website but you can have a free preview [here (insert url)](#)

### Key Concepts

1. Server Side Request Forgery (SSRF)
2. Exploiting differences in Flask and FastAPI

### Solution

1. Make use of multiple of the same arguments in Flask gateway to pivot into FastAPI gateway
2. Enter the URL of the homepage into the FastAPI gateway
3. The FastAPI gateway will return the flag

```
http://localhost:3000/?service=admin_page&service=home_page&url=http://home_page
```

### Learning Objectives

1. Understanding the difference between Flask and FastAPI
2. Learning how to exploit Server Side Request Forgery (SSRF)

### Flag
`grey{d0ubl3_ch3ck_y0ur_3ndp0ints_in_m1cr0s3rv1c3s}`
