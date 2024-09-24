# With Generator Short Circuit
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def find_number(numbers):
    numbers = (n for n in numbers if (n % 3) == 0)
    try:
        number = next(numbers)
    except StopIteration:
        number = None
    return number


number = find_number(numbers)

# Naive Approach
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def find_number(numbers):
    for n in numbers:
        # concerns are not seperated
        if (n % 3) == 0:
            return n
    return None


number = find_number(numbers)
