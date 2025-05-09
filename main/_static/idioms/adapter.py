# With Adapter
for first, item in loop_first([]):
    if first:
        edge_case(item)
        continue
    default(item)

# Naive Approach
is_first = True
for items in []:
    if is_first:
        edge_case(item)
        is_first = False
        continue
    default(item)
