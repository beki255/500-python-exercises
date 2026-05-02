"""Ex168 Func Is Armstrong
"""

def is_arm(n): d=len(str(n)); return sum(int(c)**d for c in str(n))==n
print(is_arm(153))
