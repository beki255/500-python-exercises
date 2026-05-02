"""Ex271 Remove Punctuation
"""

import string
s="Hello, World!"
clean="".join(c for c in s if c not in string.punctuation)
print(f"Clean: {clean}")
