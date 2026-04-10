"""
Class:   CS-510
Author:  Sharie Rhea
Date:    02.26.2026

A program that prints basic CPU and memory details using the psutil library.
"""

import psutil


def get_cpu_usage() -> float:
    """Return the current CPU usage percentage."""
    # interval of at least 0.1 seconds as recommended in the psutil docs
    return psutil.cpu_percent(interval=0.1)


def get_cpu_count() -> int:
    """Return the number of logical CPU cores detected on the system."""
    cores = psutil.cpu_count()
    if cores:
        return cores
    print("Error: unable to determine the number of cores!")
    return 0


def get_memory_stats() -> tuple[float, float, float]:
    """
    Return the total memory, available memory, and memory in use.
    Values returned are in gigabytes for readability.
    """
    BYTES_PER_GB = 1024**3

    virtual_memory = psutil.virtual_memory()
    # retrieve desired stats and convert from bytes to GB
    stats = (
        virtual_memory.total / BYTES_PER_GB,
        virtual_memory.used / BYTES_PER_GB,
        virtual_memory.available / BYTES_PER_GB,
    )

    return stats


def display_resource_report():
    """
    Display a nicely formatted report of the CPU and memory info.
    """
    mem_total, mem_used, mem_available = get_memory_stats()

    print("\n===== System Resource Report =====")
    print(f"CPU Usage: {get_cpu_usage():>21.1f}%")
    print(f"CPU Cores: {get_cpu_count():>22}")
    print(f"Total Memory: {mem_total:>16.2f} GB")
    print(f"Memory Usage: {mem_used:>16.2f} GB")
    print(f"Memory Available: {mem_available:>12.2f} GB")
    print("==================================\n")


def main():
    # entry point
    display_resource_report()


if __name__ == "__main__":
    main()
