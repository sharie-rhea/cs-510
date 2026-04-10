import psutil


def display_process_info():
    """
    Retrieves and displays information about all active system processes.
    Output includes PID, process name, memory usage %, and CPU usage %.
    """

    # define column headers with consistent spacing
    header = f"{'PID':<10} {'Name':<40} {'Memory %':<10} {'CPU %':<10}"
    print(header)
    print("-" * len(header))

    # iterate through all running processes and extract/cache relevant info
    for process in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
        try:
            # retrieve each component from the info dict
            pid = process.info["pid"]
            name = process.info["name"]
            memory = process.info["memory_percent"]
            cpu = process.info["cpu_percent"]

            # print formatted process details
            print(f"{pid:<10} {name:<40} {memory:<10.2f} {cpu:<10.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # skip processes that can't be accessed or no longer exist
            continue


if __name__ == "__main__":
    # entry point
    display_process_info()
