"""Ex248 Pair Sum
"""

lst=[1,2,3,4,5]; t=7
p=[(x,t-x) for x in lst if (t-x) in lst and x<=t-x]
print(f"Pairs: {set(p)}")
