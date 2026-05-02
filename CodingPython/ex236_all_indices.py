"""Ex236 All Indices
"""

lst=[1,2,3,2,4,2,5]
idx=[i for i,x in enumerate(lst) if x==2]
print(f"Indices of 2: {idx}")
