students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 90, 'age': 22},
    {'name': 'Charlie', 'grade': 75, 'age': 19},
    {'name': 'David', 'grade': 88, 'age': 21},
    {'name': 'Eve', 'grade': 95, 'age': 20},
    {'name': 'Frank', 'grade': 70, 'age': 23},
    {'name': 'Grace', 'grade': 80, 'age': 18},
    {'name': 'Heidi', 'grade': 85, 'age': 21},
    {'name': 'Ivan', 'grade': 60, 'age': 24},
    {'name': 'Judy', 'grade': 92, 'age': 22}
]
def compare(a, b, keys):
    for key in keys:
        if a[key] < b[key]:
            return -1
        elif a[key] > b[key]:
            return 1
    return 0
def selection_sort_multi(data, keys):
    n = len(data)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if compare(data[j], data[min_index], keys) < 0:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
    return data
user_input = input("Sort by keys (e.g., name,grade,age): ").strip().lower()
sort_keys = [key.strip() for key in user_input.split(',') if key.strip() in ['name', 'grade', 'age']]

if sort_keys:
    sorted_students = selection_sort_multi(students.copy(), sort_keys)
    print(f"{'Name':<10} {'Grade':<5} {'Age':<3}")
    print("-" * 22)
    for student in sorted_students:
        print(f"{student['name']:<10} {student['grade']:<5} {student['age']:<3}")
else:
    print("Invalid input. Please enter any combination of 'name', 'grade', 'age'.")
    