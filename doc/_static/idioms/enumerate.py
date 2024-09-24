# Good
customers = ["Marry", "Thor", "Peter", "Batman"]
for index, customer in enumerate(customers):
    print(f"Customer: {customer}, Queue position: {index}")

# Bad
index = 0
customers = ["Marry", "Thor", "Peter", "Batman"]
for customer in customers:
    print(f"Customer: {customer}, Queue position: {index}")
    index += 1
