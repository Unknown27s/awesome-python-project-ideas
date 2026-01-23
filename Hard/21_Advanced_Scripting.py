import psutil
import datetime
import time

def monitor():
    print("Starting System Monitor...")
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage("/")
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"[{timestamp}]")
            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory: {memory_info.percent}% used of {round(memory_info.total / (1024**3), 2)} GB")
            print(f"Disk: {disk_info.percent}% used of {round(disk_info.total / (1024**3), 2)} GB")
            print("-" * 30)

    except KeyboardInterrupt:
        print("\nStopping Monitor.")

if __name__ == "__main__":
    monitor()
