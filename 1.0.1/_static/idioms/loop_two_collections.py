# Good
names = ["raymond", "rachel", "matthew"]
colors = ["red", "green", "blue", "yellow"]

for name, color in zip(names, colors):
    print(f"{name} --> {color}")

# Bad
names = ["raymond", "rachel", "matthew"]
colors = ["red", "green", "blue", "yellow"]

n = min(len(names), len(colors))
for i in range(n):
    print(f"{names[i]} --> {colors[i]}")
