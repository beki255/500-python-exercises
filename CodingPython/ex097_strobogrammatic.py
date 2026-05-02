"""Ex097 Strobogrammatic
"""

n="69"
valid={"0":"0","1":"1","6":"9","8":"8","9":"6"}
print(f"Strobo: {all(c in valid for c in n)}")
