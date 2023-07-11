import psutil
import datetime
import time


def get_disk_usage():
    partitions = psutil.disk_partitions()
    disk_usage = []

    for partition in partitions:
        if 'rw' in partition.opts:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage.append({
                'device': partition.device,
                #'disk' : partition,
                'mountpoint': partition.mountpoint,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
    
    return disk_usage

'''
# 獲取磁碟使用率
disk_usage = get_disk_usage()
for usage in disk_usage:
    print(f"Device: {usage['device']}")
    #print(f"Disk: {usage['disk']}")
    print(f"Mountpoint: {usage['mountpoint']}")
    print(f"Total: {usage['total']} bytes")
    print(f"Used: {usage['used']} bytes")
    print(f"Free: {usage['free']} bytes")
    print(f"Percent: {usage['percent']}%")
    print()
'''



def get_disk_usage_time():
    disk_counters = psutil.disk_io_counters(perdisk=True)
    disk_usage_time = {}

    for device, counters in disk_counters.items():
        usage_time = counters.read_time + counters.write_time
        disk_usage_time[device] = usage_time
    

    return disk_usage_time




duration = datetime.timedelta(days=1)

# 計算程式的結束時間
end_time = datetime.datetime.now() + duration

# 每1分鐘執行一次程式
while datetime.datetime.now() < end_time:
    
    '''
    # 獲取磁碟使用時間
    disk_usage_time = get_disk_usage_time()
    for disk, usage_time in disk_usage_time.items():
        print(f"Disk: {disk}")
        print(f"Usage Time: {usage_time} ms")
        print()
    '''
    disk_usage = get_disk_usage()
    disk_usage_time = get_disk_usage_time()

    now = datetime.datetime.now()
    combine = list(zip(disk_usage,disk_usage_time.items()))
    
    with open(f'./record/log/Cpu/disk_usage_python_{now.strftime("%Y-%m-%d")}.log', 'a') as file:
        file.write("========================="+now.strftime("%Y-%m-%d %H:%M:%S")+"=========================\n")
        for usage,(disk, usage_time) in combine:
            file.write(f"Device: {usage['device']}\n")
            file.write(f"Mountpoint: {usage['mountpoint']}\n")
            file.write(f"Total: {usage['total']} bytes\n")
            file.write(f"Used: {usage['used']} bytes\n")
            file.write(f"Free: {usage['free']} bytes\n")
            file.write(f"Percent: {usage['percent']}%\n")
            file.write('\n')
            #file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            file.write(f"Disk: {disk}\n")
            file.write(f"Usage Time: {usage_time} ms\n")
            file.write('===================================\n')
            file.write('\n')
    """
    # 將磁碟使用率輸出到檔案
    with open('./record/log/Cpu/disk_usage.txt', 'a') as file:
        for usage in disk_usage:
            file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            file.write(f"Device: {usage['device']}\n")
            file.write(f"Mountpoint: {usage['mountpoint']}\n")
            file.write(f"Total: {usage['total']} bytes\n")
            file.write(f"Used: {usage['used']} bytes\n")
            file.write(f"Free: {usage['free']} bytes\n")
            file.write(f"Percent: {usage['percent']}%\n")
            file.write('\n')

    # 獲取磁碟使用時間
        

        # 將磁碟使用時間輸出到檔案
        #with open('./record/log/Cpu/disk_usage_time.txt', 'a') as file:
        for disk, usage_time in disk_usage_time.items():
            file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            file.write(f"Disk: {disk}\n")
            file.write(f"Usage Time: {usage_time} ms\n")
            file.write('\n')
    """
    time.sleep(5)
    
    #nohup python your_script.py &
    #pythonw.exe your_script.py