"""Ex171 Func Leap Year
"""

def leap(y): return (y%4==0 and y%100!=0) or y%400==0
print(leap(2024))
