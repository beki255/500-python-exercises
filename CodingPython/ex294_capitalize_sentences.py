"""Ex294 Capitalize Sentences
"""

s="hello. world. python."
r=". ".join(sent.capitalize() for sent in s.split(". ") if sent)
print(f"Capitalized: {r}")
