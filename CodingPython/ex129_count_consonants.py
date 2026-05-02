"""Ex129 Count Consonants
"""

s="hello"
print(f"Consonants: {sum(1 for c in s if c.isalpha() and c not in "aeiou")}")
