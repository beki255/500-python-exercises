"""Ex259 Count Consonants Str
"""

s="hello world"
print(f"Consonants: {sum(1 for c in s if c.isalpha() and c not in "aeiou")}")
