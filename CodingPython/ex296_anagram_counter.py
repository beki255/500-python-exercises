"""Ex296 Anagram Counter
"""

from collections import Counter
s1,s2="listen","silent"
print(f"Anagram: {Counter(s1)==Counter(s2)}")
