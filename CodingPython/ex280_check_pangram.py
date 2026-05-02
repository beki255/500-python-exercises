"""Ex280 Check Pangram
"""

import string
s="The quick brown fox"
alphabet=set(string.ascii_lowercase)
print(f"Pangram: {set(s.lower())>=alphabet}")
