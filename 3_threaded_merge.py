import numpy as np
import time
import matplotlib.pyplot as plt

import threading

# Based on https://medium.com/karuna-sehgal/a-simplified-explanation-of-recursive_merge-sort-77089fe03bb2
class sorterThead(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)

        self.array = args[0]

    def run(self):
        self.array = recursive_merge_sort(self.array)


    def get(self):
        self.join()
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
    if max_threads > 1:
        
        for sub_array in np.array_split(array, min(max_threads, array.size)):
            new_thread = sorterThead([sub_array])
            threads.append(new_thread)
            new_thread.start()
            

        result_array = threads[0].get()
        for thread in threads[1:]:
            thread.join()
            result_array = merge(result_array, thread.get())
    else:
        result_array = recursive_merge_sort(array)
    return result_array

def test_time():
    print(time.time())
    arrays = [np.random.randint(0, 100, 10000) for i in range(100)]
    for threads in [1, 2, 4, 8]:
        temp_times = []
        for array in arrays:
            thr1 = time.time()
            thread_sorted_array = threaded_sort(array, max_threads=threads)
            thr2 = time.time()
            temp_times.append(thr2-thr1)

        temp_times_array = np.array(temp_times)
        average_time = np.average(temp_times_array)
        std_time = np.std(temp_times_array)
        
        
        plt.scatter(threads, average_time, label=f"Threads: {threads}; Avg Time: {average_time} +/- {std_time}")
    plt.legend()
    plt.show()
    print(time.time())


def main():
    test_time()


if __name__ == "__main__":
    main()

