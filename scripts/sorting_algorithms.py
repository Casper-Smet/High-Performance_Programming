from typing import List


def selection_sort(data: List[int]) -> None:
    """Sort an array using selection sort"""
    # loop over len(data) -1 elements
    for index1 in range(len(data)-1):
        smallest = index1 # first index of remaining array

        # loop to find index of smallest element
        for index2 in range(index1 + 1, len(data)):
            if data[index2] < data[index1]:
                smallest = index2

        # swap smallest element into position
        data[smallest], data[index1] = data[index1], data[smallest]


def recursive_selection_sort(data: List[int]) -> None:
    # Lists with less than one element are sorted
    if len(data) <= 1:
        return data
    else:
        smallest = min(data)    # find the smallest element in the list
        data.remove(smallest)   # remove from the list
        return [smallest] + recursive_selection_sort(data) # put on front of to be sorted remainder


def insertion_sort(data: List[int]) -> None:
    """Sorting an array in place using insertion sort."""
    # loop over len(data) - 1 elements
    for next in range(1, len(data)):
        insert = data[next] # value to insert
        move_item = next    # location to place element

        # search for place to put current element
        while move_item > 0 and data[move_item - 1] > insert:
            # shift element right one slot
            data[move_item] = data[move_item - 1]
            move_item -= 1

        data[move_item] = insert # place inserted element


def recursive_insertion_sort(toSort: List[int], sorted: List[int] = []) -> List[int]:
    """Recursive implementation of insertion sort"""
    if len(toSort) == 0: # empty lists are sorted
        return sorted
    else:
        head, *tail = toSort
        sorted = recursive_insertion(head, sorted) # insert the head into the sorted list
        return recursive_insertion_sort(tail, sorted) # recursive call to sort the remainder


def recursive_insertion(element: int, data: List[int]) -> List[int]:
    """Assistant function to recursive insertion sort; recursively insert into a list"""
    if len(data) == 0: # if the list is empty, the element should be place there anyway
        return [element]
    else:
        head, *tail = data
        if element < head: # when the element is smaller than the head of the insertion list
            return [element, head] + tail # place it on the front
        else:
            return [head] + recursive_insertion(element, tail) # else, keep the head separate, and recursively insert into the tail

def merge_sort(data: List[int]) -> None:
    merge_sort2(data, 0, len(data)-1)
def merge_sort(xs: List[int]) -> None:
    """In place merge sort of array without recursive. The basic idea
    is to avoid the recursive call while using iterative solution.
    The algorithm first merge chunk of length of 2, then merge chunks
    of length 4, then 8, 16, .... , until 2^k where 2^k is large than
    the length of the array
    """

    unit = 1
    while unit <= len(xs):
        h = 0
        for h in range(0, len(xs), unit * 2):
            l, r = h, min(len(xs), h + 2 * unit)
            mid = h + unit
            # merge xs[h:h + 2 * unit]
            p, q = l, mid
            while p < mid and q < r:
                # use <= for stable merge merge
                if xs[p] <= xs[q]:
                    p += 1
                else:
                    tmp = xs[q]
                    xs[p + 1: q + 1] = xs[p:q]
                    xs[p] = tmp
                    p, mid, q = p + 1, mid + 1, q + 1

        unit *= 2
def merge_arrays(array1: List[int], array2: List[int]) -> List[int]:
    """Recursively merge two arrays into one sorted array"""
    if len(array1) == len(array2) == 0: # done when both arrays are empty
        return []
    else:
        if len(array1) == 0: # if either array is empty
            head, *tail = array2
            return [head] + merge_arrays(array1, tail) # merge the remainder of the non-empty list
        elif len(array2) == 0: # idem for the other array
            head, *tail = array1
            return [head] + merge_arrays(tail, array2)
        else: # when both still have elements
            head1, *tail1 = array1
            head2, *tail2 = array2
            if head1 < head2: # select the smallest
                return [head1] + merge_arrays(tail1, array2) # and merge with the remainder
            else:
                return [head2] + merge_arrays(array1, tail2) # idem for when array 2 had the smaller element


def recursive_merge_sort(data: List[int]) -> List[int]:
    """Recursive merge sort implementation for sorting arrays"""
    if len(data) == 1: # arrays with 1 element are sorted
        return data
    else:
        middle = int(len(data)/2) # find the middle (round down if len(data) is odd)
        first, second = data[:middle], data[middle:] # split the list in half
        return merge_arrays(recursive_merge_sort(first), recursive_merge_sort(second)) # merge_sort both arrays, and merge them into the result