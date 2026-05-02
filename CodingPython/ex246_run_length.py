"""Ex246 Run Length
"""

s="aaabbbcccaaa"
l=[]; c=1
for i in range(len(s)):
    if i+1<len(s) and s[i]==s[i+1]: c+=1
    else: l.append([s[i],c]); c=1
print(f"RLE: {l}")
