"""Ex037 Power Using Loop
"""

base, exp = 2, 5
r = 1
for _ in range(exp): r *= base
print(f"{base}^{exp} = {r}")
