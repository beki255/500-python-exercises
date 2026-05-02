"""Ex297 Longest Prefix
"""

words=["flower","flow","flight"]
prefix=""
for i in range(len(words[0])):
    if all(i<len(w) and w[i]==words[0][i] for w in words): prefix+=words[0][i]
    else: break
print(f"Common prefix: {prefix}")
