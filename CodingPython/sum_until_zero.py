sum = 0 
while True:
     number = float(input("Enter a number (enter 0 to stop): "))
     if number == 0:
        break 
     sum += number  

print(f"The total sum of all accepted values is: {sum}")
