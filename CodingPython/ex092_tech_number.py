"""Ex092 Tech Number
"""

n=2025
s=str(n)
h=len(s)//2
print(f"Tech: {int(s[:h] or 0)+int(s[h:])**2==n}")
