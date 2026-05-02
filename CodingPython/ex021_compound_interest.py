"""Ex021 Compound Interest
"""

p, r, t = 1000, 5, 2
ci = p * (1 + r/100) ** t - p
print(f"CI: {ci}")
