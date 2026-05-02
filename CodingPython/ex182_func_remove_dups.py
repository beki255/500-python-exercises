"""Ex182 Func Remove Dups
"""

def rd(lst): return list(dict.fromkeys(lst))
print(rd([1,2,2,3,3]))
