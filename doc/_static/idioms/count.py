# Good
from collections import Counter

colors = ["green", "blue", "red", "green", "red", "red"]

counts = Counter(colors)

# Bad
from collections import defaultdict

colors = ["green", "blue", "red", "green", "red", "red"]

d = defaultdict(int)
for color in colors:
    d[color] += 1
