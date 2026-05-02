"""Ex119 Count Vowels
"""

s="hello world"
print(f"Vowels: {sum(1 for c in s if c in "aeiou")}")
