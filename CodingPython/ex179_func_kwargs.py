"""Ex179 Func Kwargs
"""

def info(**kw):
    for k,v in kw.items(): print(f"{k}: {v}")
info(name="Alice",age=25)
