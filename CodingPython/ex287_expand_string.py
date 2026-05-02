"""Ex287 Expand String
"""

s="a3b3c3"
r="";
for i in range(0,len(s),2): r+=s[i]*int(s[i+1])
print(f"Expanded: {r}")
