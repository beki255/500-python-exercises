"""Ex096 Tax Bracket
"""

inc=50000
tax=2000+(inc-30000)*0.2 if inc>30000 else 0
print(f"Tax: {tax}")
