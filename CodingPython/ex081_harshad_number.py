"""Ex081 Harshad Number
"""

n=18
print(f"Harshad: {n % sum(int(d) for d in str(n)) == 0}")
