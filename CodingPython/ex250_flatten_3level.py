"""Ex250 Flatten 3Level
"""

from collections import deque
n=[1,[2,[3,4],5],6]
def f(lst):
    r=[]
    for i in lst: r.extend(f(i) if isinstance(i,list) else [i])
    return r
print(f"Flat: {f(n)}")
