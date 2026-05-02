"""Ex132 Palindrome Loop
"""

n=12321
t,rev=12321,0
while t>0: rev=rev*10+t%10; t//=10
print(f"Palindrome: {rev==n}")
