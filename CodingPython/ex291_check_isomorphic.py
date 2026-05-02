"""Ex291 Check Isomorphic
"""

s1,s2="egg","add"
d1={c:i for i,c in enumerate(s1)}; d2={c:i for i,c in enumerate(s2)}
print(f"Isomorphic: {list(d1.values())==list(d2.values())}")
