"""Ex149 X Pattern
"""

n=7
for i in range(n):
    for j in range(n): print("*" if i==j or i+j==n-1 else " ",end=""); print()
