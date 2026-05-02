# Real-world dataset: Sorted oil prices (in birr)
oil_price = [250, 300, 560, 1100, 1500]  

# Test Case: Searching for an existing price
key = 1100  

# Binary Search Implementation
top = len(oil_price) - 1  
bottom = 0  
found = False  
index = -1  

while not found and top >= bottom:
    middle = (top + bottom) // 2  
    if key == oil_price[middle]:  
        found = True
        index = middle
    elif key < oil_price[middle]:  
        top = middle - 1
    else:  
        bottom = middle + 1

# Output the result
if index == -1:
    print(f"The price of oil {key} is not found!")
else:
    print(f"The price of oil {key} is found at index position: {index}")