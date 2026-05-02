"""Ex195 Func Find Mode
"""

from collections import Counter
def mode(lst): return Counter(lst).most_common(1)[0][0]
print(mode([1,2,2,3,3,3]))
