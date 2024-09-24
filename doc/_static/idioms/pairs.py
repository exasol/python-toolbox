# Good
colors = ["red", "green", "blue"]
d = dict(enumerate(colors))

# Bad
colors = ["red", "green", "blue"]
d = {}
for i, color in enumerate(colors):
    d[i] = color
