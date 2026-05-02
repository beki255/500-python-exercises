"""Ex045 Check Armstrong
"""

n = 153
digits = len(str(n))
print(f"Armstrong: {sum(int(d)**digits for d in str(n)) == n}")
