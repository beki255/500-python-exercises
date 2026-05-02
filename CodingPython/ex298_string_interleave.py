"""Ex298 String Interleave
"""

s1,s2="ab","cd"
r="".join(a+b for a,b in zip(s1,s2))+s1[len(s2):]+s2[len(s1):]
print(f"Interleaved: {r}")
