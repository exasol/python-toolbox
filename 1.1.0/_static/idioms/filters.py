# With Filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
odd = filter(lambda n: n % 2, numbers)
even = (number for number in numbers if not number % 2)

print(f"Sum of odd values: {sum(odd)}")
print(f"Sum of even values: {sum(even)}")

# Naive Approach
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
odd = 0
even = 0

for number in numbers:
    if number % 2:
        odd += number
    else:
        even += number

print(f"Sum of odd values: {odd}")
print(f"Sum of even values: {even}")
