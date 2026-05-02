"""Ex055 Check Leap Year
"""

year=2024
is_leap=(year%4==0 and year%100!=0) or (year%400==0)
print(f"Leap: {is_leap}")
