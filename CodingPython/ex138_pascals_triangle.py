"""Ex138 Pascals Triangle
"""

n=5
for i in range(n):
    val=1
    for j in range(i+1): print(val,end=" "); val=val*(i-j)//(j+1)
    print()
