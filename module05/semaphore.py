"""
Class:   CS-510
Author:  Sharie Rhea
Date:    02.28.2026

This program demonstrates how a semaphore limits how many threads can enter a shared section at once.
10 processes are created to download random webpages, but the number of concurrent downloads is limited to 4.
Feel free to change the total number of concurrent processes to see the execution time change.
"""

import multiprocessing
import random
import time
import urllib.request

# set number of max processes that can run at a time
max_concurrrent_processes = 4
# set total number of processes being run
total_processes = 10

# a list of potential urls to download from
urls = [
    "http://www.python.org",
    "https://www.snhu.edu/",
    "https://www.google.com/",
    "https://www.youtube.com/",
    "https://weather.com/",
    "https://ocaml.org/",
    "https://www.man7.org/linux/man-pages/",
]

# seed random
random.seed()

# initialize semaphore
semaphore = multiprocessing.Semaphore(max_concurrrent_processes)


def current_time():
    """Display the current time."""
    curr_time = time.localtime()
    current_time = time.strftime("%H:%M:%S", curr_time)
    return current_time


def choose_url() -> str:
    """Return a random url from a list of potential options."""
    return random.choice(urls)


# create function that would use semaphore to manage processess
def processing(process_id: int, url: str):
    print(
        f"{current_time()} [WAIT] Process {process_id} is waiting for the semaphore. Available: {semaphore.get_value()}"
    )

    # the `with` block automatically handles semaphore.acquire and semaphore.release
    with semaphore:
        print(
            f"{current_time()} [ACQUIRED] Process {process_id} has acquired the semaphore. Available {semaphore.get_value()}"
        )

        print(f"\tDownloading {url}...")

        # download something from the internet
        response = urllib.request.urlopen(url)
        _ = response.read()

        print(f"\tFinished downloading {url}")

    print(
        f"{current_time()} [RELEASE] Process {process_id} has released the semaphore. Available: {semaphore.get_value()}"
    )


if __name__ == "__main__":
    # note the start time so we can calculate execution time later
    start_time = time.time()

    # print how many processes the semaphore will run at one time
    print(f"Semaphore has been initialized with the value of: {max_concurrrent_processes}")

    # create multiprocess list to store all processes
    multiprocess = []
    for i in range(total_processes):
        m = multiprocessing.Process(target=processing, args=(i, choose_url()))
        multiprocess.append(m)
        m.start()

    # wait for all processes to finish
    for m in multiprocess:
        m.join()

    print("All processes are done!")
    print()
    print(f"Execution time: {time.time() - start_time:.3} seconds")
