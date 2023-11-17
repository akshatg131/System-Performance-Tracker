import psutil

# Function to get system performance metrics
def get_system_perf():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    return {
        'CPU Usage (%)': cpu_percent,
        'Memory Usage (%)': memory_info.percent,
        'Disk Usage (%)': disk_info.percent
    }

# Example usage
if __name__ == "__main__":
    metrics = get_system_perf()
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
