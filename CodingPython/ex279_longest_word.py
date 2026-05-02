"""Ex279 Longest Word
"""

s="Hello world python programming"
words=s.split()
print(f"Longest: {max(words,key=len)}")
