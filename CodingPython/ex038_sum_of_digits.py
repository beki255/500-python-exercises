"""Ex038 Sum Of Digits
"""

n = 1234
s = sum(int(d) for d in str(n))
print(f"Sum digits: {s}")
