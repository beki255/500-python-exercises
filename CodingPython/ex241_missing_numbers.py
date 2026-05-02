"""Ex241 Missing Numbers
"""

lst=[1,2,3,5,6,8,9]
full=set(range(min(lst),max(lst)+1))
print(f"Missing: {sorted(full-set(lst))}")
