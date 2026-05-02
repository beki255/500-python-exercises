"""Ex137 Count Char
"""

s="hello"; ch="l"
print(f"Count: {sum(1 for c in s if c==ch)}")
