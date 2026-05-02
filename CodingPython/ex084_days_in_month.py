"""Ex084 Days In Month
"""

m,y=2,2024
days=29 if m==2 and (y%4==0) else 31 if m in [1,3,5,7,8,10,12] else 30
print(f"Days: {days}")
