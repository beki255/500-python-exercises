"""Ex049 Seconds To Dhm
"""

s=100000
d=s//86400
h=(s%86400)//3600
m=s%60
print(f"{d}d {h}h {m}m")
