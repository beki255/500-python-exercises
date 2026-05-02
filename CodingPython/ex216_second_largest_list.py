"""Ex216 Second Largest List
"""

lst=[10,50,30,90,20]
l=sorted(set(lst),reverse=True)
print(f"Second: {l[1]}")
