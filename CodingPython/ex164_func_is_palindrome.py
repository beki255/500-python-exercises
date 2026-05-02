"""Ex164 Func Is Palindrome
"""

def is_pal(s): return str(s)==str(s)[::-1]
print(is_pal("racecar"))
