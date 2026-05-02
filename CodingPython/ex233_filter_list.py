"""Ex233 Filter List
"""

lst=[1,2,3,4,5,6,7,8,9,10]
o=list(filter(lambda x: x%2!=0, lst))
print(f"Odds: {o}")
