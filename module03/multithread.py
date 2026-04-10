"""
Class:   CS-510
Author:  Sharie Rhea
Date:    02.20.2026

A multithreading demonstration program.
Creates 3 threads in total:
    1 & 2 - sum first and second half of an array of ints
    3 - display thread info
Each print message is prefixed with the thread's ID so that the interleaved
execution can be seen. Run multiple times to see the execution order change.
"""

import threading
import random


def sum_array(array: list[int], lock: threading.Lock, return_value: list[int]):
    """
    Sums the elements of the given array and returns the sum using the return_value list.
    Acquires a lock before entering the critical section (mutating the list).
    """

    id = threading.get_ident()

    print(f"{id}: starting function sum_array...")

    # naive sum implementation to keep thread running longer
    sum = 0
    for number in array:
        sum += number
    print(f"{id}: sum of {len(array)} values = {sum}")

    # critical section
    with lock:
        print(f"{id}: acquiring lock...")
        return_value.append(sum)
        print(f"{id}: releasing lock...")

    print(f"{id}: sum_array finished!")


def display_thread_info():
    """
    Displays basic information about the running thread: ID, native ID, running, and active thread count.
    """

    id = threading.get_ident()

    print(f"{id}: starting function display_thread_info...")
    print(f"{id}: native ID: {threading.get_native_id()}")
    print(f"{id}: is running: {threading.current_thread().is_alive()}")
    print(f"{id}: active thread count: {threading.active_count()}")
    print(f"{id}: display_thread_info finished!")


if __name__ == "__main__":
    # keep track of all our threads so we can join them later
    threads = []

    # generate an array of random, unique integers to sum
    random.seed()
    count = 100
    array = random.sample(range(0, 1000), count)
    # this list is used so that threads can return values back by mutating the list
    return_value = []
    # create a lock so that only one thread can mutate the list at a time!
    lock = threading.Lock()

    # data parallelization, use two threads to sum separate halves of the array
    # explicitly use integer division for slice indices
    threads.append(threading.Thread(target=sum_array, args=(array[: ((count // 2))], lock, return_value)))
    threads.append(threading.Thread(target=sum_array, args=(array[count // 2 :], lock, return_value)))

    # add a third thread to increase complexity
    threads.append(threading.Thread(target=display_thread_info))

    # start each thread
    for thread in threads:
        thread.start()

    # wait for all threads to finish executing
    for thread in threads:
        thread.join()

    print()
    print(f"Total sum (threaded): {sum(return_value)}")
    print(f"Check sum (serial)  : {sum(array)}")
