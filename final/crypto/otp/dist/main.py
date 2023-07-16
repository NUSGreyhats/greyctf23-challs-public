from secrets import randbelow
from Crypto.Util.number import getPrime

FLAG = <REDACTED>

p = getPrime(1024)
n = 6
g = 3**20

def checkToken(token):
    if (len(token) != n):
        return False
    for i in token:
        if (not (32 <= i.bit_length() <= 1023)):
            return False
    return True

def checkOTP(inputOTP, realOTP):
    if (len(inputOTP) != n):
        return False
    for i in range(n):
        if (inputOTP[i] != realOTP[i]):
            return False
    return True

def sendOtp(otp):
    # We implement this next year
    pass

r = randbelow(p)
otp = [randbelow(2**16) for _ in range(n)]
priv = [randbelow(p) for _ in range(n)]
pub = [pow(g, priv[i], p) for i in range(n)]
    
print("p:", p)
print("pub:", pub)
print()
print(f"Welcome stranger, please insert your token to generate otp ({n} integers separated by comma):")

token = list(map(int, input().split(',')))

if (not checkToken(token)):
    print("Token bad x.x")
    exit(0)

tokenHash = sum([priv[i] * token[i] for i in range(n)])
otpHash = [pow(g, r, p)] + [(pow(pub[i], r, p) * pow(g, otp[i], p)) % p for i in range(n)]

print("Generating OTP....")

print("Token Hash:", tokenHash)
print("OTP Hash:", otpHash)

print("Sending OTP....")

sendOtp(otp)
print(sum([token[i] * otp[i] for i in range(n)]))

print(f"Now insert your otp ({n} integers separated by comma):")

inputOtp = list(map(int, input().split(',')))

if (checkOTP(inputOtp, otp)):
    print("Welcome Admin!", FLAG)
else:
    print("Wrong OTP, exiting")
