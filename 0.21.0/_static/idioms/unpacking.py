# Good
person = "John", "Doe", 42, "john.doe@example.net"

firstname, lastname, age, email = person
# Bad
person = "John", "Doe", 42, "john.doe@example.net"

firstname = person[0]
lastname = person[1]
age = person[2]
email = person[3]
