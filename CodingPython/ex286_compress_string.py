"""Ex286 Compress String
"""

s="aaabbbcccaaa"
r=""; cnt=1
for i in range(len(s)):
    if i+1<len(s) and s[i]==s[i+1]: cnt+=1
    else: r+=s[i]+str(cnt); cnt=1
print(f"Compressed: {r}")
