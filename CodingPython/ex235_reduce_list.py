"""Ex235 Reduce List
"""

from functools import reduce
lst=[1,2,3,4,5]
p=reduce(lambda x,y: x*y, lst)
print(f"Product: {p}")
