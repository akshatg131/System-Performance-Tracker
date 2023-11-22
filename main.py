import streamlit as st
import psutil
import GPUtil
import time

# Function to get system performance metrics
def get_process_cpu_usage():
    process_list = psutil.process_iter(attrs=['pid', 'name', 'cpu_percent'])
    process_info = [{'PID': process.info['pid'], 'Name': process.info['name'], 'CPU Usage': process.info['cpu_percent']} for process in process_list]
    return [info for info in process_info if info['CPU Usage'] > 0.5]

def get_cpu_perf():
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)

def get_chart():
    cpu_chart = st.line_chart()
    gpu_chart = st.line_chart()

    for i in range(100):  # Update graphs for 100 iterations
        # Get system metrics
        metrics_cpu = get_cpu_perf()
        metrics_gpu = get_gpu_stats()
        # Update graphs
        cpu_chart.add_rows([metrics_cpu['CPU Usage']])
        gpu_chart.add_rows([metrics_gpu['GPU Usage']])
        time.sleep(0.1)  # Wait before next update

    # Get CPU core count
    cpu_count = psutil.cpu_count(logical=False)  # Physical cores
    logical_cpu_count = psutil.cpu_count(logical=True)  # Logical cores

    # Get CPU frequency
    cpu_freq = psutil.cpu_freq()

    # Get CPU temperature (works on some systems)
    try:
        cpu_temp = psutil.sensors_temperatures()['coretemp'][0].current
    except Exception as e:
        cpu_temp = "N/A"

    # Get CPU voltage (works on some systems)
    try:
        cpu_voltage = psutil.cpu_voltage()
    except Exception as e:
        cpu_voltage = "N/A"

    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    return {
        "CPU Usage": cpu_usage,
        "Physical Cores": cpu_count,
        "Logical Cores": logical_cpu_count,
        "CPU Frequency": cpu_freq.current,
        "CPU Temperature": cpu_temp,
        "CPU Voltage": cpu_voltage,
        'Memory Usage (%)': memory_info.percent,
        'Disk Usage (%)': disk_info.percent
    }

def get_gpu_stats():
    try:
        gpus = GPUtil.getGPUs()
        gpu = gpus[0]  # Assuming you have only one GPU
        gpu_usage = gpu.load * 100  # GPU usage percentage
        gpu_temp = gpu.temperature  # GPU temperature in Celsius
    except Exception as e:
        gpu_usage = "N/A"
        gpu_temp = "N/A"
    
    return {
        "GPU Usage": gpu_usage,
        "GPU Temperature": gpu_temp,
    }

# Streamlit app
def main():
    st.title("System Performance Tracker")

    # Get system metrics
    metrics_cpu = get_cpu_perf()
    metrics_gpu = get_gpu_stats()
    process_cpu_usage = get_process_cpu_usage()

    # Display metrics in Streamlit
    st.header("CPU Metrics")
    for metric, value in metrics_cpu.items():
        st.write(f"{metric}: {value}")

    st.header("GPU Metrics")
    for metric, value in metrics_gpu.items():
        st.write(f"{metric}: {value}")

    st.header("Process CPU Usage")
    for process in process_cpu_usage:
        st.write(f"PID: {process['PID']}, Name: {process['Name']}, CPU Usage: {process['CPU Usage']}%")

if __name__ == "__main__":
    main()
