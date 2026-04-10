"""
Class:   CS-510
Author:  Sharie Rhea
Date:    04.02.2026
"""

from datetime import datetime
import os
import psutil  # requires pip install
import stat
import sys
import threading


# UTILITY FUNCTIONS
def printBlankLines(lines: int):
    for _ in range(lines):
        print("")


def printMsg1(num):
    id = threading.get_ident()

    print(f"\t{id}: native ID: {threading.get_native_id()}")
    print(f"\t{id}: active thread count: {threading.active_count()}")

    print(f"\t{id}: {num} cubed: {num * num * num}")
    print(f"\t{id}: printMsg1 finished!")


def printMsg2(num):
    id = threading.get_ident()

    print(f"\t{id}: native ID: {threading.get_native_id()}")
    print(f"\t{id}: active thread count: {threading.active_count()}")

    print(f"\t{id}: {num} squared: {num * num}")
    print(f"\t{id}: printMsg2 finished!")


# STATS FUNCTIONS
def getFileDiskUsageStatistics() -> None:
    """
    This function displays information about the disk partitions and a sample file. size and file information.
    For each partition: name, mount point, filesystem type, used/free space, percent space used.
    For the sample file: name, size, mode.
    """
    print("Getting Disk Statistics")

    BYTES_PER_GB = 1024**3

    # system disk statistics
    for partition in psutil.disk_partitions():
        print(f"\tStats for: {partition.device}")
        print(f"\t\tMount point: {partition.mountpoint}")
        print(f"\t\tFilesystem type: {partition.fstype}")

        # retrieve usage info for the partition
        total, used, _, percent = psutil.disk_usage(partition.mountpoint)
        # display in GB for readability if either value is larger than 1 GB
        if used > BYTES_PER_GB or total > BYTES_PER_GB:
            used /= BYTES_PER_GB
            total /= BYTES_PER_GB
            print(f"\t\tUsage: {used:.2f} / {total:.2f} GB, {percent}%")
        else:
            print(f"\t\tUsage: {used} / {total} bytes, {percent}%")
    printBlankLines(2)

    print("Getting File Statistics")
    file_name = "./projecttwo.txt"
    try:
        file_stats = os.stat(file_name)

        print(f"\tAbsolute path: {os.path.abspath(file_name)}")
        print(f"\tFile size: {file_stats.st_size} bytes")
        print(f"\tLast modified: {datetime.fromtimestamp(file_stats.st_mtime)}")
        print(f"\tFile mode: {stat.filemode(file_stats.st_mode)}")
    except FileNotFoundError:
        print(f"\tERROR: missing file 'projecttwo.txt'!")
    printBlankLines(2)


def getMemoryStatistics() -> None:
    """
    Display the total memory, available memory, and memory in use.
    Values are shown in gigabytes for readability.
    """
    print("Getting Memory Statistics")

    BYTES_PER_GB = 1024**3

    virtual_memory = psutil.virtual_memory()
    # retrieve desired stats and convert from bytes to GB
    mem_total = virtual_memory.total / BYTES_PER_GB
    mem_used = virtual_memory.used / BYTES_PER_GB
    mem_available = virtual_memory.available / BYTES_PER_GB

    print(f"\tTotal Memory: {mem_total:.2f} GB")
    print(f"\tMemory Usage: {mem_used:.2f} GB")
    print(f"\tMemory Available: {mem_available:.2f} GB")

    printBlankLines(2)


def getCpuStatistics() -> None:
    """
    Retrieve CPU statistics, including usage percentage and cores.
    Also display information on processes.
    """
    print("Getting CPU Statistics")

    # interval of at least 0.1 seconds as recommended in the psutil docs
    cpu_percent = psutil.cpu_percent(interval=0.1)
    print(f"\tCPU Usage: {cpu_percent:.1f}%")

    cores = psutil.cpu_count()
    if cores:
        print(f"\tCPU Cores: {cores}")
    else:
        print("\tCPU Cores: ERROR, unable to determine the number of cores!")

    printBlankLines(2)

    print("Displaying Process Info")
    display_process_info()

    printBlankLines(2)


def display_process_info() -> None:
    """
    Retrieves and displays information about all active system processes.
    Output includes PID, process name, and memory usage %.
    """

    # define column headers with consistent spacing
    header = f"\t{'PID':<10} {'Name':<40} {'Memory %':<10}"
    print(header)
    print("\t" + "-" * len(header))

    # iterate through all running processes and extract/cache relevant info
    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            # retrieve each component from the info dict
            pid = process.info["pid"]
            name = process.info["name"]
            memory = process.info["memory_percent"]

            # print formatted process details
            print(f"\t{pid:<10} {name:<40} {memory:<10.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # skip processes that can't be accessed or no longer exist
            continue


def showThreadingExample() -> None:
    """
    Demonstrates multithreading. Two threads are spawned, one calling printMsg1 and the other printMsg2.
    """
    print("Demonstrating Threading")

    # keep track of all our threads so we can join them later
    threads = []

    # create each thread
    threads.append(threading.Thread(target=printMsg1, args=[13]))
    threads.append(threading.Thread(target=printMsg2, args=[5]))

    # start each thread
    for thread in threads:
        thread.start()

    # wait for all threads to finish executing
    for thread in threads:
        thread.join()

    print("Done With Threading!")

    printBlankLines(2)


def showErrorHandling() -> None:
    """
    Demonstrate system error handling.
    Since out of memory, or out of disk space errors are difficult to create,
    we will use a divide by zero error and show the error handling being executed.
    """

    print("Demonstrating Error Handling")
    try:
        result = 100 / 0
    except ZeroDivisionError:
        print("\tERROR: You can't divide by zero!")
    except MemoryError:
        print("\tERROR: Memory Error!")
    else:
        print(f"\tResult is: {result}")
    finally:
        print("\tAll threads complete.")

    printBlankLines(2)


def main() -> int:
    """
    Main entry point, calls the other statistics functions.
    """
    print("Starting Program")
    print("=============================")

    getFileDiskUsageStatistics()

    getCpuStatistics()

    getMemoryStatistics()

    showThreadingExample()

    showErrorHandling()

    print("=============================")
    print("Terminating Program")

    return 0


if __name__ == "__main__":
    sys.exit(main())
