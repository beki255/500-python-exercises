"""Ex099 Lucky Number
"""

n=123
t=sum(int(d) for d in str(n))
print(f"Lucky: {t%9==0}")
