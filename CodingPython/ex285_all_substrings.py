"""Ex285 All Substrings
"""

s="abc"
subs=[s[i:j] for i in range(len(s)) for j in range(i+1,len(s)+1)]
print(f"Subs: {subs}")
