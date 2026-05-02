"""Ex166 Func Count Vowels
"""

def cv(s): return sum(1 for c in s.lower() if c in "aeiou")
print(cv("hello"))
