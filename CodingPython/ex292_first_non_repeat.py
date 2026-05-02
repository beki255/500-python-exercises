"""Ex292 First Non Repeat
"""

s="swiss"
for c in s:
    if s.count(c)==1: print(f"First non-repeat: {c}"); break
