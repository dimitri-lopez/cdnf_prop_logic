#!/usr/bin/env python3


def iterate_number_bases(arr, numbers = None, indices = None):
    if len(arr) == 0: return []
    if indices is None:
        indices = [0] * len(arr);
        numbers = []
        return iterate_number_bases(arr, numbers, indices)

    # increment things that overflowed
    for i in reversed(range(len(indices))):
        if i == 0: continue
        if indices[i] >= arr[i]:
            indices[i] = 0
            indices[i - 1] += 1
    # base case, check if all indices are greater
    if indices[0] >= arr[0]: return numbers

    number = []
    for i in range(len(indices)):
        number.append(indices[i])
    numbers.append(number)

    indices[-1] += 1 # increment the last number
    return iterate_number_bases(arr, numbers, indices) # recurse

# arr = [1, 2, 3, 4]
# numbers = []
# print(iterate_number_bases(arr))
