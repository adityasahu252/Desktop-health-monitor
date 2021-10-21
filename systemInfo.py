import psutil  # for fetching cpu, disk, memory data
import platform  # for fetching sysmtem data
import GPUtil  # for fetching gpu data
from tabulate import tabulate  # for aligning everything in table form
import threading
import csv
import json
from pprint import pprint
interval = 1


class process:
    def __init__(self) -> None:
        pass

    def get_size(self, bytes, suffix="B"):
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

    # def create_csv_data(self, data):
    #     f = open("data.csv", "w")
    #     writer = csv.writer(f)
    #     writer.writerow(['CPU', 'Memory', 'Disk', 'GPU'])
    #     record = []
    #     record.append(data)
    #     for i in record:
    #         pprint(i)

    #     f.close()

    def cpu(self):

        print("="*20, "CPU Info", "="*20, '\n')
        self.list_cpu = []
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

        cores = cores.replace("\n", "")

        cpu_usage = str(psutil.cpu_percent()) + '%'

        self.list_cpu.append((maxfq, minfq, currentfq, cores, cpu_usage))

        # self.record.append(self.list_cpu)
        print(tabulate(self.list_cpu, headers=('Max Frequency', 'Min Frequency',
                                               'Current Frequency', 'CPU per core usage %', 'CPU usage %')))

        print('\n')

        return self.list_cpu

    def memory(self):

        print("="*20, "Memory Information", "="*20, '\n')
        self.list_memory = []
        # get the memory details
        svmem = psutil.virtual_memory()
        # total = get_size(svmem.total)
        total = self.get_size(svmem.total)
        available = self.get_size(svmem.available)
        used = self.get_size(svmem.used)
        percentage = str(svmem.percent) + "%"

        self.list_memory.append((total, available, used, percentage))

        print(tabulate(self.list_memory, headers=(
            'Total memory', 'Available', 'Used', 'Precentage %')))
        # self.record.append(self.list_memory)

        print('\n')
        return self.list_memory

    def disk(self):
        print("="*20, "Disk Information", "="*20, '\n')
        self.list_disks = []
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
            total_size = self.get_size(partition_usage.total)
            used = self.get_size(partition_usage.used)
            free = self.get_size(partition_usage.free)
            percentage = partition_usage.percent

            self.list_disks.append((device, mountpoint, file_system_type,
                                    total_size, used, free, percentage))
            # self.record.append(self.list_disks)

        print(tabulate(self.list_disks, headers=("Device", "Mountpoint", "File System Type", "Total Size", "Used", "Free",
                                                 "Percentage %")))

        print('\n')

        return self.list_disks

    def gpu(self):
        print("="*20, "GPU Information", "="*20, '\n')
        gpus = GPUtil.getGPUs()

        self.list_gpus = []
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
            self.list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature
            ))

            # self.record.append(self.list_gpus)

        print(tabulate(self.list_gpus, headers=("GPU Id", "GPU Name", "Load %", "Free memory", "Used memory", "Total memory",
                                                "Temperature")))

        print('\n')
        return self.list_gpus

    def startTimer(self):

        threading.Timer(interval, self.startTimer).start()
        data = {
            "CPU": self.cpu(),
            "Memory": self.memory(),
            "Disk": self.disk(),
            "GPU": self.gpu(),
        }

        return data


if __name__ == "__main__":
    p = process()
    record = p.startTimer()
    json_object = json.dumps(record, indent=4)

with open("sample.json", "w") as outfile:
    outfile.write(json_object)
