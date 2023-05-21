# 100 Questions

### Challenge Details

I love doing practice papers! There are a 100 questions, but the answers to some are more important than others...

### Key Concepts

Blind SQLi

### Solution

- Realise that Q42 gives flag + input field is vulnerable to SQLi (`2'--` is correct for Q1)
- [Blind injection](https://portswigger.net/web-security/sql-injection/blind#:~:text=Exploiting%20blind%20SQL%20injection%20by%20triggering%20conditional%20responses) (`2' AND SUBSTRING((SELECT Answer FROM QNA WHERE ID=42), 1, 1) = 'g` is correct for Q1 => first letter of flag is `g`)

### Learning Objectives

- Testing for SQLi vulnerability
- Blind SQLi

### Flag

grey{1_c4N7_533}
