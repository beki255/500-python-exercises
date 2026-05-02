"""Ex187 Func Cap Words
"""

def cap(s): return " ".join(w.capitalize() for w in s.split())
print(cap("hello world"))
