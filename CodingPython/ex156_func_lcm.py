"""Ex156 Func Lcm
"""

import math
def lcm(a,b): return abs(a*b)//math.gcd(a,b)
print(lcm(12,15))
