"""Ex189 Func Perfect Num
"""

def perfect(n): return sum(i for i in range(1,n) if n%i==0)==n
print(perfect(6))
