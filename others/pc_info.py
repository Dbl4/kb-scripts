import os
import platform

import psutil


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_pc_info():
    data = {}
    try:
        devices_hdd = []
        fstype_hdd = []
        total_mem_hdd = []
        used_mem_hdd = []
        used_hdd_percent = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            devices_hdd.append(partition.device)
            fstype_hdd.append(partition.fstype)
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            total_mem_hdd.append(get_size(partition_usage.total))
            used_mem_hdd.append(get_size(partition_usage.used))
            used_hdd_percent.append(partition_usage.percent)
        data['status'] = 1
        data['cpu_utilization'] = psutil.cpu_percent(interval=1)
        data['ram_usage'] = psutil.virtual_memory().percent
        data['processor'] = platform.processor()
        data['os'] = platform.system()
        data['os_version'] = platform.version()
        data['max_cpu_frec'] = psutil.cpu_freq().max
        data['total_ram'] = round(psutil.virtual_memory().total / 1000000000, 2)
        data['devices_hdd'] = devices_hdd
        data['fstype_hdd'] = fstype_hdd
        data['total_mem_hdd'] = total_mem_hdd
        data['used_mem_hdd'] = used_mem_hdd
        data['used_hdd_percent'] = used_hdd_percent
        data['status'] = 1
    except:
        data['status'] = 0
    return data


if __name__ == '__main__':
    # print(get_pc_info())
    base_name = 'Analytics'
    print(os.path)
    print(os.path.join('C:', os.sep, base_name))
    print(os.path)