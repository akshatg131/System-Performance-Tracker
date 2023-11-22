import streamlit as st
import time
from auth import authenticate
from main import get_cpu_perf,get_gpu_stats ,get_process_cpu_usage

# Streamlit app


def show_system_performance():         
    # Get system metrics
    metrics_cpu = get_cpu_perf()
    metrics_gpu = get_gpu_stats()
    process_cpu_usage = get_process_cpu_usage()

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

def main():
    
    st.title("System Performance Tracker")

    # Add a sign-in section
    st.header("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check if the sign-in button is pressed
    if st.button("Sign In"):
        if authenticate(username, password):
            # If authentication is successful, clear the page and show system performance
            st.balloons()
            st.success("Logged in successfully!")
              # This will clear the entire page
            show_system_performance()
    # Create a placeholder for the sign-in section
    # sign_in_container = st.empty()
    # with sign_in_container:
    #     # Add a sign-in section
    #     st.header("Sign In")
    #     username = st.text_input("Username")
    #     password = st.text_input("Password", type="password")

    #     # Check if the sign-in button is pressed
    #     if st.button("Sign In"):
    #         if authenticate(username, password):
    #             # If authentication is successful, clear the page and show system performance
    #             st.balloons()
    #             st.success("Logged in successfully!")
    #             sign_in_container.empty()  # This will clear the entire page
    #             time.sleep(2)
    #             show_system_performance()
    #         else:
    #             st.error("Invalid username or password") 

if __name__ == "__main__":
    main()
