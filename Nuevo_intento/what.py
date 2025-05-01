my_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

# Indices to delete
indices_to_delete = [2, 3, 7, 0]

# Sort indices in reverse order
for index in sorted(indices_to_delete, reverse=True):
    del my_list[index]

print(my_list)  # Output: ['b', 'e', 'f', 'g', 'i']