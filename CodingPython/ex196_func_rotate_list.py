"""Ex196 Func Rotate List
"""

def rot(lst,k): k%=len(lst); return lst[-k:]+lst[:-k]
print(rot([1,2,3,4,5],2))
