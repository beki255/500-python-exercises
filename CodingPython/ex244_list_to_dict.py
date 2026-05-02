"""Ex244 List To Dict
"""

lst=["a","b","c"]
d={i:lst[i] for i in range(len(lst))}
print(f"Dict: {d}")
