"""Ex090 Magic Number
"""

n=123
s=n
while s>9: s=sum(int(d) for d in str(s))
print(f"Magic: {s==1}")
