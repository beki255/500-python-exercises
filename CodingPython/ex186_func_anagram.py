"""Ex186 Func Anagram
"""

def anagram(s1,s2): return sorted(s1.lower())==sorted(s2.lower())
print(anagram("listen","silent"))
