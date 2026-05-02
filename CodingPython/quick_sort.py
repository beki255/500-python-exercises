def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)  # Sort left sub-array
        quick_sort(arr, pi + 1, high)  # Sort right sub-array

def partition(arr, low, high):
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Place pivot at correct position
    return i + 1

# Example usage
arr = [4, 2, 6, 1, 3]
quick_sort(arr, 0, len(arr) - 1)
print(arr)