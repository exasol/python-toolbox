# Good
blocks = []
for block in iter(partial(f.read, 32), ""):
    blocks.append(block)

# Bad
blocks = []
while True:
    block = f.read(32)
    if block == "":
        break
    blocks.append(block)
