# Good
customers = ["Marry", "Brain", "Peter", "Batman"]
for customer in reversed(customers):
    print(customer)

# Bad
customers = ["Marry", "Brain", "Peter", "Batman"]
for index in range(len(customers) - 1, -1, -1):
    print(customers[index])
