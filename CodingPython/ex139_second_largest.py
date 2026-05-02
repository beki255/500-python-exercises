"""Ex139 Second Largest
"""

lst=[10,20,5,40,15]
lst2=sorted(set(lst),reverse=True)
print(f"Second largest: {lst2[1]}")
