from collections import defaultdict
from math import ceil
from collections import deque

def counting_sort(array, key_fn):
    """Counting sort algorithm.
    ref: https://en.wikipedia.org/wiki/Counting_sort
    
    Sort the array according to the values of a key function computed on the 
    items in a stable way.
    It is only suitable in situations where the variation in keys is not 
    significantly greater than the number of items.
    Can be used as a subroutine in other sorting algorithm, such as radix sort.
    
    k := integer such that key_fn(x) <= k, for each x in array
    
    Time complexity analysis:
    Best: O(n+k)
    Average: O(n+k)
    Worst: O(n+k)
    
    Space complexity analysis:
    Best: O(n+k)
    Average: O(n+k)
    Worst: O(n+k)
    """
    
    counts = defaultdict(int)  # frequencies histogram
    k = 0
    for i in array:
        key_value = key_fn(i)
        counts[key_value] += 1
        k = max(k, key_value)
    
    total = 0
    for i in range(k + 1):
        old_count = counts[i]
        counts[i] = total
        total += old_count
        
    sorted_array = array.copy()
    for i in array:
        key_value = key_fn(i)
        sorted_array[counts[key_value]] = i
        counts[key_value] += 1
        
    return sorted_array


def merge_sort(array, start=None, end=None):
    """Merge sort algorithm.
    ref: https://en.wikipedia.org/wiki/Merge_sort
    
    In-place sort the items of the array in the range [start, end] by 
    recursively partitioning and sorting them in two subgroups of equal size.
    
    Time complexity analysis:
    Best: O(n * log n)
    Average: O(n * log n)
    Worst: O(n * log n)
    
    Space complexity analysis:
    Best: O(n) + additional space required by merge_adjacent_runs
    Average: O(n) + additional space required by merge_adjacent_runs
    Worst: O(n) + additional space required by merge_adjacent_runs
    """
    
    start = 0 if start is None else start
    end = len(array) - 1 if end is None else end
    
    if start == end:
        return
    
    half = (start + end) // 2
    merge_sort(array, start, half)
    merge_sort(array, half + 1, end)
    merge_adjacent_runs(array, start, half, end)


def merge_adjacent_runs(array, start, half, end):
    """In-place merge two sorted adjacent sub-arrays (runs) in the ranges 
    [start, half] and [half + 1, end] by using a temporary deque as buffer.
    
    In the best case (all the items in the first sub-array are smaller than 
    those in the second one) the auxiliary deque will contain at most 1 item.
    
    In the worst case (all the items in the first sub-array are greater or 
    equal than those in the second one) the auxiliary deque will contain all 
    the first sub-array.
    
    Time complexity analysis:
    Best: O(n)
    Average: O(n)
    Worst: O(n)
    
    Space complexity analysis:
    Best: O(n) + O(1)
    Average: O(n) + O(l/2)
    Worst: O(n) + O(l)
    
    where n = end - start, l = half - start 
    """
    
    # this deque will act as a buffer for the items in the range [start, half]
    # items will be moved from the first sub-array to the deque only if needed
    aux = deque()
    # rather than comparing the first sub-array with the second one, we will 
    # compare the deque and the second sub-array
    aux.append(array[start])
    
    i, j = start, half + 1
    curr = start
    while len(aux) > 0 and j <= end:
        if aux[0] <= array[j]:
            # an item from the first sub-array is placed back into the array
            array[curr] = aux.popleft()
        else:
            # an item from the second sub-array is placed into the array in a 
            # smaller position
            array[curr] = array[j]
            j += 1
        # an item from the first sub-array must always be pushed to deque to
        # make room for the next ordered item
        if i < half:
            # items to be pushed must belong to the first sub-array
            i += 1
            aux.append(array[i])
        curr += 1
    
    # process remaining (first sub-array) items in the deque
    while len(aux) > 0:
        array[curr] = aux.popleft()
        curr += 1
    
    # process remaining items in the second sub-array
    for j in range(j, end):
        array[curr] = array[j]
        curr += 1
