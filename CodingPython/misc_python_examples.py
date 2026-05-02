'''print ("First line\nSecond line")
     
Ask for the user’s first name and 
display the output message
name=input("please enter your first name")
print("hello",name) 
print("bereket",end=" ")
print('sahlemariam')
print("python","cpp")
print("python","cpp",sep='####')
a=200
b=13
print(a/b)
print(format(a/b,'.3f'))
# inserting comma separators
print(format(2354,',f'))
print(format(23,'0%'))
print(format(2354,',d'))
result = 2 + 5 * 6 / 2  #2 + (5 * 6) / 2
print(result) # Output: 17.0
if 9>6:
 print("ok")
 a = 330
b = 3300
print("A") if a > b else  print("=") if a == b else print("B")
q=23
w=200
if q>w:
    pass
print("hhhhhh")
fruits = ["apple", "banana", "cherry"]
for f in fruits:
 print(f)a=list(input("enter multiple integer values separated by space").split())
print("list of student:",a)
b,c=map(int,input("enter two integer separeted by space:").split())
print(b,c)
d,e=map(int,input("enter two no separeted by space:") .split())
print(d,e)

pets = ["dog", "cat", "rabbit"]
pets[1] # Remove last item
print(pets)
print(-4%5)
nu=int(input("enter number:"))
match nu:
  case 1:
    print("one")
  case 2:
    print("two")
  case 3:
    print("three")
num1=int(input())
num2=int(input()) 
print("they are equal")if num1==num2 else print("num1 is greater than num2") if num1>num2 else print("num1 is less than num2") 
di=float(input(" enter dimeter:"))
import math
A=math.pi*((di/2)**2)
print(f" the area of the circle with diameter {di} is {A}")
initial=int(input())
p=(initial*2)/100
o=initial-p
print(f"amount the house owner wii get: {format(o,',.2f')}")
print(" the commision amount the broker wii get", format(p,',f'))''' 
a=float(input())
b=float(input())
c=float(input())
if a==0:
 print("a cannot be zero")
else:
 dis=(b**2)-(4*a*c)
 import cmath
 root1=(-b+cmath.sqrt(dis))/(2*a)
 root2=(-b-cmath.sqrt(dis))/(2*a)
 print(f"The solutions are: {root1} and {root2}")



    