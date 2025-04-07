# Good
output = f"Firstname: {user.first_name}, Lastname: {user.last_name}, Age: {user.age}"

# Bad
output = "Firstname: {}, Lastname: {}, Age: {}".format(
    user.first_name, user.last_name, user.age
)
