import numpy as np
import cProfile

# Based on https://medium.com/karuna-sehgal/a-simplified-explanation-of-merge-sort-77089fe03bb2

    

def merge_sort(sub_array: np.array):
    if sub_array.size <= 1:
        return sub_array


    left, right = np.array_split(sub_array, 2)

    return merge(merge_sort(left), merge_sort(right))

def merge(left: np.array, right: np.array):
    index_left   = 0
    index_right  = 0
    index_result = 0

    size_left   = left.size
    size_right  = right.size
    size_result = size_left + size_right

    result = np.empty(size_result, dtype=left.dtype)

    while index_left < size_left and index_right < size_right and index_result < size_result:
        if left[index_left] < right[index_right]:
            result[index_result] = left[index_left]
            index_left += 1
        else:
            result[index_result] = right[index_right]
            index_right += 1

        index_result += 1

    return np.concatenate((result[:index_result], left[index_left:], right[index_right:]))



def main():
    array = np.array([2, 5, 1, 3, 7, 4, 2, 3, 9, 8, 6, 3])
    print(array)
    pr = cProfile.Profile()
    pr.enable()
    sorted_array = merge_sort(array)
    pr.disable()
    print(sorted_array)
    pr.print_stats()

if __name__ == "__main__":
    main()

