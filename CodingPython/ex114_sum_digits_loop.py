"""Ex114 Sum Digits Loop
"""

n=1234
s=0
while n>0: s+=n%10; n//=10
print(f"Sum: {s}")
