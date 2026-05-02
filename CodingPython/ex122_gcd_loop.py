"""Ex122 Gcd Loop
"""

a,b=48,18
while b: a,b=b,a%b
print(f"GCD: {a}")
