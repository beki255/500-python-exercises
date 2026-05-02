"""Ex131 Factorial Series
"""

for i in range(1,6):
    f=1
    for j in range(1,i+1): f*=j
    print(f"{i}!={f}")
