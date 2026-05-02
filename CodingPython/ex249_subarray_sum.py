"""Ex249 Subarray Sum
"""

lst=[1,2,3,4,5]; k=3
sa=[lst[i:i+k] for i in range(len(lst)-k+1)]
print(f"Subarrays: {sa}")
