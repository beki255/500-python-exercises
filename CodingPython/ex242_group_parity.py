"""Ex242 Group Parity
"""

lst=[1,2,3,4,5,6,7,8]
e=list(filter(lambda x: x%2==0, lst)); o=list(filter(lambda x: x%2!=0, lst))
print(f"Evens: {e}, Odds: {o}")
