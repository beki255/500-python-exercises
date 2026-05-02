"""Ex068 Check Armstrong Num
"""

n=153
d=len(str(n))
print(f"Armstrong: {sum(int(c)**d for c in str(n))==n}")
