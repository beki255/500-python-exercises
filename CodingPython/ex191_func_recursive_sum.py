"""Ex191 Func Recursive Sum
"""

def rs(n): return n+rs(n-1) if n>1 else n
print(rs(10))
