"""Ex121 Primes Up To N
"""

n=50
primes=[i for i in range(2,n+1) if all(i%j!=0 for j in range(2,int(i**0.5)+1))]
print(f"Primes: {primes}")
