"""Ex193 Func Gcd List
"""

def gcd_lst(lst):
    r=lst[0]
    for n in lst[1:]:
        while n: r,n=n,r%n
    return r
print(gcd_lst([48,18,24]))
