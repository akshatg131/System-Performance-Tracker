import streamlit as st
from main import get_cpu_perf,get_gpu_stats ,get_process_cpu_usage,get_chart
from login import login, user_dashboard

# Streamlit app
def main():
    
    st.title("System Performance Tracker")
   
    # Get system metrics
    metrics_cpu = get_cpu_perf()
    metrics_gpu = get_gpu_stats()
    process_cpu_usage = sorted(get_process_cpu_usage(), key=lambda x: x['CPU Usage'], reverse=True)

    cpu_container = st.container()

    col1, col2 = st.columns(2)

    st.sidebar.write("APPS")
    col1_sidebar, col2_sidebar = st.sidebar.columns(2)

    with col1_sidebar:
        st.write("Name")
        for process_info in process_cpu_usage:
            process_name = process_info['Name'].split(".exe")[0]  # Remove ".exe" suffix
            st.write(process_name)

    with col2_sidebar:
        st.write("CPU Usage")
        for process_info in process_cpu_usage:
            st.write(f"{process_info['CPU Usage']}%")
            
    get_chart()
    
    with col1:
        cpu_progress_bar = st.progress(metrics_cpu['CPU Usage'] / 100)
        st.write(f"CPU Usage: {metrics_cpu['CPU Usage']}%")

        gpu_progress_bar = st.progress(metrics_gpu['GPU Usage'] / 100)
        st.write(f"GPU Usage: {metrics_gpu['GPU Usage']}%")

    
    # Display metrics in Streamlit
    with col2:
        with st.expander("CPU Stats"):
            for metric, value in metrics_cpu.items():
                st.write(f"{metric}: {value}")

        with st.expander("GPU Stats"):
            for metric, value in metrics_gpu.items():
                st.write(f"{metric}: {value}")

    if st.button("Refresh"):
        st.experimental_rerun()

if __name__ == "__main__":
    username = login()
    if username:
        main()
