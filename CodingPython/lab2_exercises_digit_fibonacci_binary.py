'''1. write a modular program that accept a postive number from  keybord 
and pass a number as an argument of afunction  to display the sum
of each individual digts and the number of digits 
 -------------------------------------------------'''

num=int(input("enter a positive number:"))
def digit_sum(n): 
    sum=0
    c=0
    while n>0:
        digit=n%10
        n=n//10
        c=c+1
        sum=sum+digit
    print(" the sum is :", sum)
    print("the no of digit is:", c)
digit_sum(num)    
        
'''2. write a modular program  that accept a postive number from the keyboard and 
pass the number as an argument of a function to display the fibonacci of the
accepted number 
-------------------------------------------------------'''

n=int(input("enter a postive number:"))
def fibonacci(n):
    if n==0 or n==1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
fab=fibonacci(n)    
print(f" the fibonacci number of {n} is {fab}")    


'''3. rewrite the above question to display the sum of each of the fibonacci 
values till the accepted number fibonacci. 
--------------------------------------------------'''

n=int(input("enter a postive number:"))
def fibonacci(n):
    if n==0 or n==1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
sum=0
for i in range(n+1):
    sum=sum + fibonacci(i)
print(f" the  fibonacci sum upto  number of {n} is {sum}")    
          

'''4. write a modular program that accept a decimal number and display in its 
 equivalent binary number.
 ---------------------------------------------------- '''
 
n=int(input("enter a decimal number:"))
def digit_sum(n):
    binary=[]
    while n>0:
        dig=n%2
        binary.append(dig)
        n=n//2
    binary=binary[::-1]
    print(" the binary equivalent value is:")
    for i in binary:
        print(i,end="")
digit_sum(n)        
