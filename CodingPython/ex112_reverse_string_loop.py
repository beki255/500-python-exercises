"""Ex112 Reverse String Loop
"""

s="hello"
rev=""
for c in s: rev=c+rev
print(f"Reverse: {rev}")
