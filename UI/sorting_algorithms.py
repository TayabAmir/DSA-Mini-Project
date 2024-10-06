import random

# Bubble Sort
def bubble_sort(arr, start, end, column_no):
    for i in range(start, end):
        for j in range(start, end - i - 1):
            if arr[j][column_no] > arr[j + 1][column_no]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# Insertion Sort
def insertion_sort(arr, start, end, column_no):
    for i in range(start + 1, end):
        key = arr[i]
        j = i - 1
        while j >= start and arr[j][column_no] > key[column_no]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# Selection Sort
def selection_sort(arr, start, end, column_no):
    for i in range(start, end - 1):
        min_index = i
        for j in range(i + 1, end):
            if arr[j][column_no] < arr[min_index][column_no]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]


# Merge Sort
def merge_sort(arr, start, end, column_no):
    if start < end - 1:
        mid = (start + end) // 2
        merge_sort(arr, start, mid, column_no)
        merge_sort(arr, mid, end, column_no)
        merge(arr, start, mid, end, column_no)


def merge(arr, start, mid, end, column_no):
    left = arr[start:mid]
    right = arr[mid:end]
    i = j = 0
    k = start

    while i < len(left) and j < len(right):
        if left[i][column_no] <= right[j][column_no]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


# Hybrid Merge Sort
def hybrid_merge_sort(arr, start, end, column_no):
    threshold = 32
    if end - start <= threshold:
        insertion_sort(arr, start, end, column_no)
    else:
        mid = (start + end) // 2
        hybrid_merge_sort(arr, start, mid, column_no)
        hybrid_merge_sort(arr, mid, end, column_no)
        merge(arr, start, mid, end, column_no)

# Quick Sort
def quick_sort(arr, start, end, column_no):
    if start < end:
        pivot_index = random.randint(start, end)
        arr[pivot_index], arr[end] = arr[end], arr[pivot_index]

        pivot_index = partition(arr, start, end, column_no)
        
        quick_sort(arr, start, pivot_index - 1, column_no)
        quick_sort(arr, pivot_index + 1, end, column_no)

def partition(arr, start, end, column_no):
    pivot = arr[end][column_no]
    i = start - 1
    for j in range(start, end):
        if arr[j][column_no] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    i += 1
    arr[i], arr[end] = arr[end], arr[i]
    return i

# Bucket Sort
def bucket_sort(arr, start, end, column_no):
    if start >= end:
        return
    max_value = max(arr[i][column_no] for i in range(start, end))
    size = (max_value + 1) // len(arr) + 1
    buckets = [[] for _ in range(len(arr))]

    for i in range(start, end):
        index = arr[i][column_no] // size
        buckets[min(index, len(buckets) - 1)].append(arr[i])

    result = []
    for bucket in buckets:
        insertion_sort(bucket, 0, len(bucket), column_no)
        result.extend(bucket)

    for i in range(start, end):
        arr[i] = result[i - start]



# Radix Sort
def radix_sort(arr, start, end, column_no):
    max_val = max(arr[i][column_no] for i in range(start, end))
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(arr, start, end, column_no, exp)
        exp *= 10


def counting_sort_for_radix(arr, start, end, column_no, exp):
    output = [0] * (end - start)
    count = [0] * 10

    for i in range(start, end):
        index = (arr[i][column_no] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(end - 1, start - 1, -1):
        index = (arr[i][column_no] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    for i in range(start, end):
        arr[i] = output[i - start]


# Counting Sort
def counting_sort(arr, start, end, column_no):
    max_val = max(arr[i][column_no] for i in range(start, end))
    count = [0] * (max_val + 1)

    for i in range(start, end):
        count[arr[i][column_no]] += 1

    index = start
    for i in range(len(count)):
        while count[i] > 0:
            arr[index][column_no] = i
            index += 1
            count[i] -= 1


# Heap Sort
def heap_sort(arr, start, end, column_no):
    for i in range((end - start) // 2 - 1, start - 1, -1):
        heapify(arr, end, i, column_no)

    for i in range(end - 1, start, -1):
        arr[i], arr[start] = arr[start], arr[i]
        heapify(arr, i, start, column_no)


def heapify(arr, n, i, column_no):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left][column_no] > arr[largest][column_no]:
        largest = left

    if right < n and arr[right][column_no] > arr[largest][column_no]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, column_no)


# Shell Sort
def shell_sort(arr, start, end, column_no):
    gap = (end - start) // 2
    while gap > 0:
        for i in range(start + gap, end):
            temp = arr[i]
            j = i
            while j >= start + gap and arr[j - gap][column_no] > temp[column_no]:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2


# Tim Sort
def tim_sort(arr, start, end, column_no):
    min_run = 32
    for i in range(start, end, min_run):
        insertion_sort(arr, i, min(i + min_run, end), column_no)

    size = min_run
    while size < end - start:
        for left in range(start, end, 2 * size):
            mid = min(left + size, end)
            right = min(left + 2 * size, end)
            merge(arr, left, mid, right, column_no)
        size *= 2