"""Ex192 Func Lcm List
"""

import math
def lcm_lst(lst):
    r=lst[0]
    for n in lst[1:]: r=abs(r*n)//math.gcd(r,n)
    return r
print(lcm_lst([2,3,4]))
