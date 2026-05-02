"""Ex093 Kaprekar Number
"""

n=45
s=str(n**2)
h=len(s)//2
print(f"Kaprekar: {int(s[:h] or 0)+int(s[h:])==n}")
