"""Ex284 Balanced Parens
"""

s="((()))"
stack=[]; bal=True
for c in s:
    if c=="(": stack.append(c)
    elif c==")":
        if not stack: bal=False; break
        stack.pop()
print(f"Balanced: {bal and not stack}")
