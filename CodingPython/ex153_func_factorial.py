"""Ex153 Func Factorial
"""

def fact(n): return n*fact(n-1) if n>1 else 1
print(fact(5))
