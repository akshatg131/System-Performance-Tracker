import streamlit as st
from main import get_cpu_perf,get_gpu_stats  

# Streamlit app
def main():
    
    st.title("System Performance Tracker")
   
    # Get system metrics
    metrics_cpu = get_cpu_perf()
    
    st.sidebar.write(f"CPU Usage: {metrics_cpu['CPU Usage']}%")
    cpu_progress_bar = st.sidebar.progress(metrics_cpu['CPU Usage']/100)

    metrics_gpu = get_gpu_stats()
    st.sidebar.write(f"GPU Usage: {metrics_gpu['GPU Usage']}%")
    gpu_progress_bar = st.sidebar.progress(metrics_gpu['GPU Usage']/100)
    # Display metrics in Streamlit
    with st.expander("CPU Stats"):
        for metric, value in metrics_cpu.items():
            st.write(f"{metric}: {value}")

    with st.expander("GPU Stats"):
        for metric, value in metrics_gpu.items():
            st.write(f"{metric}: {value}")
if __name__ == "__main__":
    main()
