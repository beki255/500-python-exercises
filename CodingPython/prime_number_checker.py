
number = int(input("Enter a positive number: "))

# Ensuring the input is valid
if number <= 0:
    print("Please enter a positive number.")
else:
    # Initializing a flag to determine if the number is prime
    is_prime = True

    # A prime number must be greater than 1 and only divisible by 1 and itself
    if number == 1:
        is_prime = False
    else:
        # Checking divisors from 2 to the square root of the number
        for i in range(2, int(number**0.5) + 1):
            if number % i == 0:
                is_prime = False
                break

    # Outputting the result
    if is_prime:
        print(f"{number} is a prime number.")
    else:
        print(f"{number} is not a prime number.")