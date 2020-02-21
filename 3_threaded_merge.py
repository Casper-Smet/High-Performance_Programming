import numpy as np
import cProfile
import time

import threading

# Based on https://medium.com/karuna-sehgal/a-simplified-explanation-of-recursive_merge-sort-77089fe03bb2
class sorterThead(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)

        self.array = args[0]

    def run(self):
        self.array = recursive_merge_sort(self.array)

    def get(self):
        return self.array


def recursive_merge_sort(sub_array: np.array):
    if sub_array.size <= 1:
        return sub_array

    left, right = np.array_split(sub_array, 2)

    return merge(
                recursive_merge_sort(left), 
                recursive_merge_sort(right)
                )


    

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


def threaded_sort(array: np.array, max_threads=4):
    threads = []
    for sub_array in np.array_split(array, min(max_threads, array.size)):
        new_thread = sorterThead([sub_array])
        threads.append(new_thread)
        new_thread.start()

    result_array = threads[0].get()
    for thread in threads[1:]:
        thread.join()
        result_array = merge(result_array, thread.get())

    return result_array
        
def main():
    # array = np.array([2, 5, 1, 3, 7, 4, 2, 3, 9, 8, 6, 3])
    array = np.random.randint(0, 100, 1000)
    
    reg1 = time.time()
    sorted_array = recursive_merge_sort(array)
    reg2 = time.time()


    thr1 = time.time()
    thread_sorted_array = threaded_sort(array)
    thr2 = time.time()


    print(reg2-reg1, thr2 - thr1)


if __name__ == "__main__":
    main()

