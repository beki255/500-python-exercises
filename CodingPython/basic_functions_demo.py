#1
def greetings (name):
    message = name + ', welcome to Python for Everyone!'
    return message
print(greetings('Asabeneh'))
#2
def add_ten(num):
   ten = 10
   return num + ten
print(add_ten(90))
#3
def square_number(x):
  return x * x
print(square_number(2))
#4
def area_of_circle (r):
   PI = 3.14
   area = PI * (r ** 2)
   return area
print(area_of_circle(10))

#5
def sum_of_numbers(n):
   total = 0
   for i in range(n+1):
       total+=i
   return total
print(sum_of_numbers(10))
print(sum_of_numbers(100))

#6
def weight_of_object (mass, gravity):
    weight = str(mass * gravity)+ ' N' # the value has to be changed to a string first
    return weight
print('Weight of an object in Newtons: ', weight_of_object(100, 9.81))    

#7 
def print_fullname(firstname, lastname):
   space = ' '
   full_name = firstname + space + lastname
   print(full_name)
print_fullname( lastname='Yetayeh' , firstname = 'Asabeneh') #  order does not matter
#8
def add_two_numbers (num1, num2):
   total = num1 + num2
   print(total)
add_two_numbers(num2 = 3, num1 = 2) # Order does not matter


#9 Returning a boolean: Example:
def is_even (n):
   if n % 2 == 0:
      print('even')
   else:
       print("odd")   
   return True                             # return stops further execution of the function, similar to break
print(is_even(10)) # True
print(is_even(7)) # False