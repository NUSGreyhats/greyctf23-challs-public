# GreyCat trial

This challenge is inspired from [this lecture from Terry Tao](https://www.youtube.com/watch?v=pp06oGD4m00). At the end of the video, Tao mentioned a theorem that he proves, called the [Green-Tao theorem](https://en.wikipedia.org/wiki/Green%E2%80%93Tao_theorem). The theorem states "for every natural number k, there exist arithmetic progressions of primes with k terms"

The challenge is about finding the appropriate arithmetic sequence of primes such that it satisfies the three trials. There is a site containing all the records of primes in arithmetic progression, [http://primerecords.dk/aprecords.htm](http://primerecords.dk/aprecords.htm). 

You would want to look at `AP-k with minimal end` section for the solution of the challenge. For the highest chance of passing the trials, I would recommend the `AP-26` sequence, to maximize the probability that you pass the second trial. In particular, the parameters `a, b` are:

```py
a = 3486107472997423 
b = 371891575525470
```

There is a small bit of RNG, so keep sending the parameters until you succeeds.