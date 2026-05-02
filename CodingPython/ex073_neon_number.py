"""Ex073 Neon Number
"""

n=9
s=sum(int(d) for d in str(n**2))
print(f"Neon: {s==n}")
