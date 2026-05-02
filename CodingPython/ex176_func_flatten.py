"""Ex176 Func Flatten
"""

def flat(lst):
    r=[]
    for i in lst: r.extend(flat(i) if isinstance(i,list) else [i])
    return r
print(flat([1,[2,3],4]))
