"""Ex237 Rotate List
"""

lst=[1,2,3,4,5]; k=2
rot=lst[-k:]+lst[:-k]
print(f"Rotated: {rot}")
