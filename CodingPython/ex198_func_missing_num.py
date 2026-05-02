"""Ex198 Func Missing Num
"""

def miss(arr): n=len(arr)+1; return n*(n+1)//2-sum(arr)
print(miss([1,2,3,5]))
