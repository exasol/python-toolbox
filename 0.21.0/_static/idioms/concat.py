# Good
names = ["Peter", "Albert", "Cleo", "Ember"]
output = ", ".join(names)

# Bad
names = ["Peter", "Albert", "Cleo", "Ember"]
output = ""
for name in names:
    output += name
    if not is_last_element(name):
        output += ", "
