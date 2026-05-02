"""Ex150 Missing Number
"""

arr=[1,2,3,5,6,7,8]
n=len(arr)+1
print(f"Missing: {n*(n+1)//2-sum(arr)}")
