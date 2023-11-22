import streamlit as st
import psutil
import GPUtil
import time

# Function to get system performance metrics
def get_cpu_perf():
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    return {"CPU Usage": cpu_usage}

def get_gpu_stats():
    try:
        gpus = GPUtil.getGPUs()
        gpu = gpus[0]  # Assuming you have only one GPU
        gpu_usage = gpu.load * 100  # GPU usage percentage
        gpu_temp = gpu.temperature  # GPU temperature in Celsius
    except Exception as e:
        gpu_usage = "N/A"
        gpu_temp = "N/A"
    
    return {"GPU Usage": gpu_usage, "GPU Temperature": gpu_temp}

# Function to get system performance metrics for charts
def get_chart_metrics():
    metrics_cpu = get_cpu_perf()
    metrics_gpu = get_gpu_stats()
    return metrics_cpu, metrics_gpu

# Streamlit app
def main():
    st.title("System Performance Tracker")

    # Get initial system metrics
    metrics_cpu, metrics_gpu = get_chart_metrics()

    # Create Streamlit line charts
    cpu_chart = st.line_chart(metrics_cpu["CPU Usage"])
    gpu_chart = st.line_chart(metrics_gpu["GPU Usage"])

    for i in range(100):  # Update graphs for 100 iterations
        # Get updated metrics
        metrics_cpu, metrics_gpu = get_chart_metrics()

        # Update graphs
        cpu_chart.line_chart(metrics_cpu["CPU Usage"])
        gpu_chart.line_chart(metrics_gpu["GPU Usage"])

        time.sleep(0.1)  # Wait before next update

    st.write("Chart update complete")

if __name__ == "__main__":
    main()
