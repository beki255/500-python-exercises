"""Ex095 Peterson Number
"""

import math
n=145
print(f"Peterson: {sum(math.factorial(int(d)) for d in str(n))==n}")
