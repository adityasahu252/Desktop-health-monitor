import psutil  # for fetching cpu, disk, memory data
import platform  # for fetching sysmtem data
import GPUtil  # for fetching gpu data
from tabulate import tabulate  # for aligning everything in table form
import threading
interval = 1


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


print("="*20, "System Information", "="*20)
user_name = platform.uname()
print(f"System: {user_name.system}")
print(f"Node Name: {user_name.node}")
print(f"Release: {user_name.release}")
print(f"Version: {user_name.version}")
print(f"Machine: {user_name.machine}")
print(f"Processor: {user_name.processor}")
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))

print('\n\n')


def cpu():

    print("="*20, "CPU Info", "="*20, '\n')
    list_cpu = []
    # CPU frequencies
    cpufreq = psutil.cpu_freq()

    maxfq = str(cpufreq.max) + 'Mhz'
    minfq = str(cpufreq.min) + 'Mhz'
    currentfq = str(cpufreq.current) + 'Mhz'

    # # CPU usage
    cpu_core_usage = {}

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_core_usage[f'Core {i + 1}'] = f'{percentage}%'

    cores = str(cpu_core_usage).replace(
        ',', '\n').replace("'", '').replace('{', '').replace('}', '').replace(' C', 'C')

    cpu_usage = str(psutil.cpu_percent()) + '%'

    list_cpu.append((maxfq, minfq, currentfq, cores, cpu_usage))

    print(tabulate(list_cpu, headers=('Max Frequency', 'Min Frequency',
          'Current Frequency', 'CPU per core usage %', 'CPU usage %')))

    print('\n')


def memory():

    print("="*20, "Memory Information", "="*20, '\n')
    list_memory = []
    # get the memory details
    svmem = psutil.virtual_memory()
    total = get_size(svmem.total)
    available = get_size(svmem.available)
    used = get_size(svmem.used)
    percentage = str(svmem.percent) + "%"

    list_memory.append((total, available, used, percentage))

    print(tabulate(list_memory, headers=(
        'Total memory', 'Available', 'Used', 'Precentage %')))

    print('\n')


def disk():
    print("="*20, "Disk Information", "="*20, '\n')
    list_disks = []
    # print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        device = partition.device
        mountpoint = partition.mountpoint
        file_system_type = partition.fstype
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        total_size = get_size(partition_usage.total)
        used = get_size(partition_usage.used)
        free = get_size(partition_usage.free)
        percentage = partition_usage.percent

        list_disks.append((device, mountpoint, file_system_type,
                          total_size, used, free, percentage))

    print(tabulate(list_disks, headers=("Device", "Mountpoint", "File System Type", "Total Size", "Used", "Free",
                                        "Percentage %")))

    print('\n')


def gpu():
    print("="*20, "GPU Information", "="*20, '\n')
    gpus = GPUtil.getGPUs()

    list_gpus = []
    for gpu in gpus:
        # get the GPU id
        gpu_id = gpu.id
        # name of GPU
        gpu_name = gpu.name
        # get % percentage of GPU usage of that GPU
        gpu_load = f"{gpu.load*100}%"
        # get free memory in MB format
        gpu_free_memory = f"{gpu.memoryFree}MB"
        # get used memory
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        # get total memory
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} °C"
        list_gpus.append((
            gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
            gpu_total_memory, gpu_temperature
        ))

    print(tabulate(list_gpus, headers=("GPU Id", "GPU Name", "Load %", "Free memory", "Used memory", "Total memory",
                                       "Temperature")))
    print('\n')


def startTimer():
    threading.Timer(interval, startTimer).start()
    cpu()
    memory()
    disk()
    gpu()
    print("\n")


if __name__ == "__main__":
    startTimer()
