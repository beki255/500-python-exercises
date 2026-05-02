"""Ex147 Max Consecutive Ones
"""

s="11011101111"
mc,count=0,0
for c in s:
    if c=="1": count+=1; mc=max(mc,count)
    else: count=0
print(f"Max 1s: {mc}")
