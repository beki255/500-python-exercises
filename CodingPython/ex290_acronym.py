"""Ex290 Acronym
"""

s="World Health Organization"
acr="".join(w[0].upper() for w in s.split())
print(f"Acronym: {acr}")
