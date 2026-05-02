"""Ex188 Func Second Largest
"""

def sl(lst): return sorted(set(lst),reverse=True)[1]
print(sl([10,20,5,40,15]))
