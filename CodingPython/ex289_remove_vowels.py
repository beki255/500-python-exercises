"""Ex289 Remove Vowels
"""

s="hello world"
r="".join(c for c in s if c not in "aeiou")
print(f"No vowels: {r}")
