"""Ex148 Collatz Sequence
"""

n=27
seq=[n]
while n!=1: n=n//2 if n%2==0 else 3*n+1; seq.append(n)
print(f"Collatz: {seq[:10]}...")
