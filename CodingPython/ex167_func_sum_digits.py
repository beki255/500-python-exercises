"""Ex167 Func Sum Digits
"""

def sd(n): return sum(int(d) for d in str(abs(n)))
print(sd(1234))
