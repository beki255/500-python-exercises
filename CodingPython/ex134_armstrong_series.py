"""Ex134 Armstrong Series
"""

for num in range(1,1001):
    d=len(str(num))
    if sum(int(c)**d for c in str(num))==num: print(num,end=" ")
print()
