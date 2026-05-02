"""Ex075 Spy Number
"""

n=22
ds=sum(int(d) for d in str(n))
dp=eval("*".join(str(n)))
print(f"Spy: {ds==dp}")
