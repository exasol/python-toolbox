# Good
template = """
{heading} - from: {date}
---------------------------------
{users}
"""
output = template.format(
    heading="User Overview",
    date=datetime.now().strftime("%Y-%m-%d"),
    users="\n".join(
        (
            f"Firstname: {user.first_name}, Lastname: {user.last_name}, Age: {user.age}"
            for user in users
        )
    ),
)

# Bad
heading = "User Overview"
date = datetime.now().strftime("%Y-%m-%d")
output = f"{heading} - from: {date}" + "\n"
output += "---------------------------------" + "\n"
for user in users:
    output += (
        f"Firstname: {user.first_name}, Lastname: {user.last_name}, Age: {user.age}\n"
    )
